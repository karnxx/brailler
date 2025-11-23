# Braille Camera Reader – Raspberry Pi + Arduino

A real-time Braille output device that uses a Raspberry Pi and a USB camera to read printed text and convert it into raised Braille using solenoids controlled by an Arduino.

---

##  Features

- Capture text using a USB camera  
- Automatic sharp-frame detection  
- OCR using EasyOCR  
- Grammar + spelling correction  
- Converts characters to 6-dot Braille  
- Sends 12-bit patterns to an Arduino  
- Arduino drives a 12-solenoid Braille cell  
- Physical buttons:
  - **GPIO17** → Capture image
  - **GPIO27** → Cycle next Braille characters

---

##  Hardware Used

### **Raspberry Pi Side**
- Raspberry Pi 5  
- USB camera  
- Two physical buttons (GPIO17, GPIO27)  
- 3.3V logic for button input  
- USB to Arduino connection  

### **Arduino Side**
- Arduino Uno / Nano  
- 12 output pins (2–13 recommended)  
- 12-solenoid braille cell  
- External power supply for solenoids  
- Flyback diodes + driver transistors or MOSFET board

---

##  Software Dependencies

Install on the Raspberry Pi:

```bash
sudo apt update
sudo apt install python3-opencv python3-pip
pip install easyocr gpiozero pyserial pyspellchecker numpy
