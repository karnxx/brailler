import cv2
import easyocr
import numpy as np
from gpiozero import Button
from time import sleep
from spellchecker import SpellChecker
import serial
import time

CAPTURE_BUTTON_PIN = 17
CYCLE_BUTTON_PIN = 27

IMAGE_PATH = "/home/brailler/project/image.jpg"
BOXED_PATH = "/home/brailler/project/image_boxed.jpg"
TEXT_PATH = "/home/brailler/project/text.txt"
BRAILLE_PATH = "/home/brailler/project/braille.txt"

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

BRAILLE_MAP = {
    'a': [1,0,0,0,0,0], 'b': [1,1,0,0,0,0], 'c': [1,0,0,1,0,0],
    'd': [1,0,0,1,1,0], 'e': [1,0,0,0,1,0], 'f': [1,1,0,1,0,0],
    'g': [1,1,0,1,1,0], 'h': [1,1,0,0,1,0], 'i': [0,1,0,1,0,0],
    'j': [0,1,0,1,1,0], 'k': [1,0,1,0,0,0], 'l': [1,1,1,0,0,0],
    'm': [1,0,1,1,0,0], 'n': [1,0,1,1,1,0], 'o': [1,0,1,0,1,0],
    'p': [1,1,1,1,0,0], 'q': [1,1,1,1,1,0], 'r': [1,1,1,0,1,0],
    's': [0,1,1,1,0,0], 't': [0,1,1,1,1,0], 'u': [1,0,1,0,0,1],
    'v': [1,1,1,0,0,1], 'w': [0,1,0,1,1,1], 'x': [1,0,1,1,0,1],
    'y': [1,0,1,1,1,1], 'z': [1,0,1,0,1,1], ' ': [0,0,0,0,0,0],
    '.': [0,1,0,0,1,1], ',': [0,1,0,0,0,0], '!':[0,1,1,0,1,0],
    '?':[0,1,1,0,0,1], ';':[0,1,1,0,0,0]
}

reader = easyocr.Reader(['en'], gpu=False)
spell = SpellChecker()

capture_button = Button(CAPTURE_BUTTON_PIN)
cycle_button = Button(CYCLE_BUTTON_PIN)

braille_sets = []
current_set_index = 0

def capture_sharpest(num_frames=5):
    cap = cv2.VideoCapture(0)
    best_frame = None
    max_var = 0
    for _ in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if var > max_var:
            max_var = var
            best_frame = frame
    cap.release()
    if best_frame is None:
        raise RuntimeError("No valid frame captured")
    return best_frame

def ocr_process(frame):
    results = reader.readtext(frame)
    filtered = []
    for bbox, text, conf in results:
        if conf < 0.4:
            continue
        text_clean = ''.join(c.lower() for c in text if c.isalnum() or c in ' .,!?;')
        if text_clean:
            filtered.append((bbox, text_clean))
    return filtered

def correct_text(text):
    corrected = []
    for word in text.split():
        prefix = ''
        suffix = ''
        core = word
        while core and not core[0].isalnum():
            prefix += core[0]
            core = core[1:]
        while core and not core[-1].isalnum():
            suffix = core[-1] + suffix
            core = core[:-1]
        if core:
            corrected_word = spell.correction(core.lower()) or core
        else:
            corrected_word = core
        corrected.append(prefix + corrected_word + suffix)
    return ' '.join(corrected)

def draw_boxes(frame, results):
    boxed = frame.copy()
    for bbox, text in results:
        pts = np.array(bbox, np.int32).reshape((-1,1,2))
        cv2.polylines(boxed,[pts],True,(0,255,0),2)
        cv2.putText(boxed, text, (int(bbox[0][0]), int(bbox[0][1]-5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    return boxed

def text_to_braille(text):
    braille = []
    for char in text:
        braille.append(BRAILLE_MAP.get(char, [0,0,0,0,0,0]))
    return braille

def send_to_arduino(braille_pair):
    """Send 12-bit pattern (two characters) to Arduino"""
    if len(braille_pair) == 1:
        braille_pair.append([0,0,0,0,0,0])
    binary_str = ''.join(str(dot) for char in braille_pair for dot in char)
    print("Sending to Arduino:", binary_str)
    arduino.write((binary_str + '\n').encode())
    time.sleep(0.05)

def save_all(normal_img, boxed_img, results):
    cv2.imwrite(IMAGE_PATH, normal_img)
    cv2.imwrite(BOXED_PATH, boxed_img)
    normal_text = ' '.join(t[1] for t in results)
    normal_text = correct_text(normal_text)
    with open(TEXT_PATH, 'w', encoding='utf-8') as f:
        f.write(normal_text)
    braille_list = text_to_braille(normal_text.replace(' ', ''))
    with open(BRAILLE_PATH, 'w', encoding='utf-8') as f:
        for b in braille_list:
            f.write(''.join(str(dot) for dot in b)+'\n')

def show_current_set():
    global current_set_index
    if not braille_sets:
        print("No braille data yet.")
        return
    subset = braille_sets[current_set_index:current_set_index+2]
    print(f"Current set index {current_set_index}:")
    for i, s in enumerate(subset):
        print(f"Char {i+1}: {s}")
    send_to_arduino(subset)

print("Ready. Press GPIO17 to capture text, GPIO27 to cycle braille.")

capturing = False
while True:
    if capture_button.is_pressed and not capturing:
        capturing = True
        print("Capture button pressed.")
        try:
            frame = capture_sharpest()
            results = ocr_process(frame)
            boxed_frame = draw_boxes(frame, results)
            save_all(frame, boxed_frame, results)
            normal_text = ' '.join(t[1] for t in results)
            normal_text = correct_text(normal_text)
            braille_sets = text_to_braille(normal_text)
            current_set_index = 0
            show_current_set()
        except Exception as e:
            print("Error during capture:", e)
        capturing = False
        sleep(0.5)

    if cycle_button.is_pressed:
        if braille_sets:
            current_set_index += 2
            if current_set_index > len(braille_sets)-1:
                current_set_index = 0
            print("Cycle button pressed. Showing next braille set:")
            show_current_set()
        else:
            print("No braille data to cycle through.")
        sleep(0.5)
