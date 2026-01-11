import serial
import numpy as np
import time

PORT = 'COM7'
BAUD_SERIAL = 250000
FS = 8000 
TONE_FREQ = 700
WPM = 12
UNIT_DUR = 1.2 / WPM

ser = serial.Serial(PORT, BAUD_SERIAL, timeout=0)

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ' ': '/'
}

def play_element(duration, is_tone=True):
    if is_tone:
        t = np.linspace(0, duration, int(FS * duration), endpoint=False)
        wave = np.tanh(np.sin(2 * np.pi * TONE_FREQ * t) * 5.0)
        ser.write(((wave * 120) + 128).astype(np.uint8).tobytes())
    else:
        silence = np.full(int(FS * duration), 128, dtype=np.uint8)
        ser.write(silence.tobytes())
    
    time.sleep(duration)

def transmit_morse(text):
    print(f"TX Morse: {text.upper()}")
    for char in text.upper():
        if char in MORSE_CODE:
            code = MORSE_CODE[char]
            if code == '/':
                play_element(UNIT_DUR * 7, is_tone=False)
            else:
                for symbol in code:
                    if symbol == '.':
                        play_element(UNIT_DUR)
                    elif symbol == '-':
                        play_element(UNIT_DUR * 3)
                    play_element(UNIT_DUR, is_tone=False)
                play_element(UNIT_DUR * 2, is_tone=False)

print("--- CW TERMINAL ---")
try:
    while True:
        msg = input("\nEnter message to key: ")
        transmit_morse(msg)
except KeyboardInterrupt:
    ser.close()
