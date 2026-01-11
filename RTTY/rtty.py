import serial
import numpy as np
import time

PORT = 'COM7' 
BAUD = 250000 
FS = 8000

MARK_FREQ = 1200   # Frequency for a digital '1'
SPACE_FREQ = 1500  # Frequency for a digital '0'
RTTY_BAUD = 45.45  # Standard RTTY speed
BIT_DURATION = 1 / RTTY_BAUD

ser = serial.Serial(PORT, BAUD, timeout=0)

def generate_rtty_bit(freq, duration):
    t = np.linspace(0, duration, int(FS * duration), endpoint=False)
    wave = np.sin(2 * np.pi * freq * t)
    wave = np.tanh(wave * 8.0) 
    return ((wave * 120) + 128).astype(np.uint8).tobytes()

def send_rtty_string(text):
    print(f"Sending: {text}")
    for char in text:
        ser.write(generate_rtty_bit(SPACE_FREQ, BIT_DURATION))
        
        bits = format(ord(char) % 32, '05b') 
        for bit in bits:
            f = MARK_FREQ if bit == '1' else SPACE_FREQ
            ser.write(generate_rtty_bit(f, BIT_DURATION))
            
        ser.write(generate_rtty_bit(MARK_FREQ, BIT_DURATION * 2))

try:
    print("--- RTTY DIGITAL STATION ---")
    while True:
        send_rtty_string("TEST STRING ")
        time.sleep(2)
except KeyboardInterrupt:
    ser.close()
