## Arduino VHF Beacon

> [!IMPORTANT]
> Depending on your jurisdiction, you may require licensing and certification to operate this equipment.

This is some example code that runs on an Arduino UNO R2 compatible that uses Windows as a host machine to transmit various forms of data.  So far, plugins are written for voice, WWV style time signals, and RTTY data transmission.

#### Setup:

 1. Attach an antenna to the PWM Pin 9. Do not ground it unless absolutely necessary.
 2. On your windows machine, run `pip install -r requirements.txt`.
 3. Compile and send the `Beacon.ino` file to your Arduino.
 4. Run the Python script in the folder for the signal you wish to emit. Modify the serial port to match where your Arduino is connected. Mine was on COM7, but it may be different for you.
 5. Tune into anywhere between 144-145Mhz, and see if you can hear your transmission. 144.175Mhz, 144.200Mhz, and 144.250Mhz did work with varying levels of success.
 6.  OPTIONAL: For voice transmission, compile and flash the special Arduino sketch in the folder, and use the special `broadcast.py` to initialize your mic.

You can get a longer antenna and broadcast on HF frequencies possibly, but that has yet to be tested. If you have an idea for a plugin to be added, feel free to add an issue, and I'll get back to you.






