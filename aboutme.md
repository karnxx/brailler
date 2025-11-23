```md
# 🔵 Braille OCR → Solenoid Display System  
Raspberry Pi + Arduino Project

A system that captures text using a Raspberry Pi camera, performs OCR, converts characters to Braille, and drives solenoids on an Arduino to physically display the Braille cells.

---

## ▶️ Running the Program

### **1. Connect Arduino via USB**

### **2. Flash the Arduino code**
Located at:

```

/arduino/solenoid_braille.ino

````

### **3. Run the Raspberry Pi main script**

```bash
python3 main.py
````

### **4. Buttons**

* **GPIO17** → Capture text
* **GPIO27** → Step through Braille output (next 2-cell block)

---

## 🔡 Braille Encoding

Each Braille character uses 6 dots:

```
1 4
2 5
3 6
```

Encoded into a 6-bit sequence:

| Character | Dots  | Binary   |
| --------- | ----- | -------- |
| **c**     | 1-4   | `100100` |
| **l**     | 1-2-3 | `111000` |
| **space** | none  | `000000` |

The Raspberry Pi sends **12 bits at a time** (2 Braille cells).

Example:

```
101000110000\n
```

---

## 🔌 Serial Protocol

* **Baud:** 115200
* **Data:** 12 characters (`0` or `1`)
* **Terminated with:** newline `\n`

Arduino behavior:

* Activates each selected solenoid for **200ms**
* Prints status text for debugging in Serial Monitor

---

## 🛠 Arduino GPIO Usage

* Pins **2–13** → 12 solenoids
* Pins **0 and 1 are NOT used** (reserved for USB Serial RX/TX)

Hardware notes:

* Use external power for solenoids
* Add flyback diodes
* Ensure correct wiring for each channel

---

## 📚 Project Structure

```
project/
│
├── main.py                # Raspberry Pi OCR + Braille output controller
├── braille_map.py         # Braille character → bit pattern map
├── arduino/
│   └── solenoid_braille.ino
├── image.jpg              # Last captured camera photo
├── image_boxed.jpg        # OCR bounding box overlay
├── text.txt               # Cleaned text
└── braille.txt            # Braille bitstrings
```

---

## 🧭 Notes

* Ensure **no other program** is using `/dev/ttyACM0`
* Arduino prints debug output to help validate communication
* Solenoids require **external power**, not USB power
* Protect everything with **flyback diodes**
* Good lighting improves OCR accuracy dramatically

---

## 💡 Future Improvements

* Multi-cell continuous Braille line
* Speech output (TTS)
* Smarter dictionary + grammar correction
* Advanced image preprocessing to reduce glare
* Auto-cropping + rotation correction
* Interface for multiple pages or paragraph navigation

---

```
```
