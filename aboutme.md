▶️ Running the Program

Connect Arduino via USB

Flash the Arduino code (in /arduino/solenoid_braille.ino)

Run the Raspberry Pi main script:

python3 main.py


Press GPIO17 to capture text

Press GPIO27 to step through Braille output

🔡 Braille Encoding

Each Braille character is represented with a 6-bit dot pattern:

1 4
2 5
3 6


Encrypted into a binary string like:

100100   = "c"
111000   = "l"
000000   = space


The Pi sends 12 bits at a time (2 cells).

🔌 Serial Protocol

Baud: 115200

12-character string of 0 and 1

Ends with newline \n

Example:

101000110000\n


Arduino:

Activates each corresponding solenoid for a 200ms pulse

Prints status back for debugging

🛠 Arduino GPIO Usage

Pins 2–13 → 12 solenoids
Not using 0 and 1 (Serial RX/TX).

📚 Project Structure
project/
│
├── main.py                # Raspberry Pi text capture + OCR + Braille
├── braille_map.py         # Braille definitions
├── arduino/
│   └── solenoid_braille.ino
├── image.jpg
├── image_boxed.jpg
├── text.txt
└── braille.txt

🧭 Notes

Make sure no other program opens /dev/ttyACM0

Use an external power supply for solenoids

Add flyback diodes to prevent damage

Arduino prints debug info so you can monitor communication

💡 Future Improvements

Multi-cell braille line

Speech output

Offline dictionary enhancements

Better image preprocessing under glare

Auto-cropping and perspective correction
