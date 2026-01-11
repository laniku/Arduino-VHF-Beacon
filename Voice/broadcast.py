import serial
import sounddevice as sd
import numpy as np

PORT = 'COM7' 
BAUD = 250000 
FS = 8000  

ser = serial.Serial(PORT, BAUD, timeout=0)

def callback(indata, frames, time_info, status):
    audio_slice = indata[:, 0]
    
    audio_slice = np.tanh(audio_slice * 7.0) 
    
    out_data = ((audio_slice * 120) + 128).astype(np.uint8)
    
    ser.write(out_data.tobytes())

with sd.InputStream(samplerate=FS, channels=1, callback=callback, blocksize=256):
    print("Broadcasting... Keep talking to fill the buffer.")
    while True:
        pass
