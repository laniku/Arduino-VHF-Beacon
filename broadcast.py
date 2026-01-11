import serial
import numpy as np
import time

PORT = 'COM7' 
BAUD = 250000 
FS = 8000

ser = serial.Serial(PORT, BAUD, timeout=0)

def broadcast_wave(wave_array):

    limited_wave = np.tanh(wave_array * 7.0)
    
    out_data = ((limited_wave * 120) + 128).astype(np.uint8)
    
    ser.write(out_data.tobytes())

if __name__ == "__main__":
    print("Base Station Online. Sending test pulses...")
    try:
        while True:
            # Create 0.1 seconds of a 440Hz tone
            t = np.linspace(0, 0.1, int(FS * 0.1), endpoint=False)
            test_tone = np.sin(2 * np.pi * 440 * t)
            
            broadcast_wave(test_tone)
            time.sleep(1.0) # Send a beep every second
    except KeyboardInterrupt:
        ser.close()