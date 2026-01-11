import serial
import numpy as np
import time

PORT = 'COM7' 
BAUD = 250000 
FS = 8000

ser = serial.Serial(PORT, BAUD, timeout=0)

def generate_wwv_pulse(freq, duration_ms):
    t = np.linspace(0, duration_ms/1000, int(FS * (duration_ms/1000)), endpoint=False)
    
    wave = np.sin(2 * np.pi * freq * t)
    
    wave = np.tanh(wave * 8.0)
    
    return ((wave * 120) + 128).astype(np.uint8).tobytes()

print("--- TIME STATION ACTIVE ---")
print("Broadcasting ticks every second...")

try:
    while True:
        now = time.localtime()
        
        # Tone Logic:
        # 1. Start of Minute: 1000Hz pulse for 800ms
        # 2. Standard Second: 800Hz tick for 45ms
        # 3. 59th Second: Silent (Gap before the minute mark)
        
        if now.tm_sec == 0:
            print(f"[{time.strftime('%H:%M:%S')}] MINUTE MARK")
            pulse = generate_wwv_pulse(1000, 800)
        elif now.tm_sec == 59:
            pulse = b'' # Silence gap
        else:
            pulse = generate_wwv_pulse(800, 45)
            
        if pulse:
            ser.write(pulse)
            
        # Wait until the start of the next second
        time.sleep(1.0 - (time.time() % 1.0))
        
except KeyboardInterrupt:
    print("\nStation Offline.")
    ser.close()
