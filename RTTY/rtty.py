import serial
import numpy as np
import time

PORT, BAUD_SERIAL, FS = 'COM7', 250000, 8000 
MARK, SPACE = 1200, 1425
BIT_DUR = 1 / 45.45

ser = serial.Serial(PORT, BAUD_SERIAL, timeout=0)

def send_tone(freq, duration):
    t = np.linspace(0, duration, int(FS * duration), endpoint=False)
    wave = np.tanh(np.sin(2 * np.pi * freq * t) * 5.0) 
    ser.write(((wave * 120) + 128).astype(np.uint8).tobytes())
    time.sleep(duration)

def transmit_rtty(text):
    print(f"Sending RTTY...")
    for _ in range(2): send_tone(MARK, BIT_DUR * 5) 
    for char in text.upper():
        send_tone(SPACE, BIT_DUR) # Start
        bits = format(ord(char) % 32, '05b')
        for bit in bits[::-1]:
            send_tone(MARK if bit == '1' else SPACE, BIT_DUR)
        send_tone(MARK, BIT_DUR * 1.5) # Stop

print("--- RTTY INTERACTIVE TERMINAL ---")
try:
    while True:
        msg = input("Enter RTTY Message: ")
        transmit_rtty(msg + "\r\n")
except KeyboardInterrupt:
    ser.close()
