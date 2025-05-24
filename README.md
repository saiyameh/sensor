**about:** an interactive proximity‐based art & counter display that uses an ultrasonic sensor to detect people passing by, shows dynamic animations on an 8×8 LED matrix, logs counts to the console, and displays contextual messages on a 16×2 I²C LCD <br>
**hardware:** Raspberry Pi Pico, Ultrasonic Sensor HC-SR04, 8×8 LED Matrix with MAX7219 driver, 16×2 I²C LCD (PCF8574 backpack), Jumper wires <br><img height="300" width="350" alt="Screenshot 2025-02-13 at 16 23 21" src="https://github.com/user-attachments/assets/da0d8a18-3116-400f-a503-226a12782a41"/> <br>
**setup:**
1. install MicroPython on your Pico (copy UF2 in BOOTSEL mode) 
2. using Thonny, create a `/lib/` folder on the Pico and upload:  
   - `pico_i2c_lcd.py`  
   - `max7219.py`  
   - `framebuf.py`  
3. upload the sensor sketch as `main.py` to the Pico root

**usage:**
1. power the Pico via USB
2. open the Thonny console to view debug logs and count updates  
3. wave your hand under the ultrasonic sensor to trigger “far→near” crossings—each crossing increments the on-screen counter & plays a celebration animation
4. when no count event is active, the display reverts to zone‐based animations:  
   - “far” (>100 cm): breathing dot + distance readout  
   - “mid” (50–100 cm): expanding circle + “i see you”  
   - “near” (20–50 cm): bar-graph + “you're trespassing”  
   - “close” (<20 cm): full-matrix flash + “stay away”
