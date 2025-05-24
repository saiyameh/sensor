**about:** an interactive proximity‐based art & counter display that uses an ultrasonic sensor to detect people passing by, shows dynamic animations on an 8×8 LED matrix, logs counts to the console, and displays contextual messages on a 16×2 I2C LCD <br>
**hardware:** Raspberry Pi Pico, Ultrasonic Sensor HC-SR04, 8×8 LED Matrix with MAX7219 driver, 16×2 I²C LCD (PCF8574 backpack), Jumper wires <br>
**setup:** <br>
<img height="300" width="350" alt="Screenshot 2025-02-13 at 16 23 21" src="https://github.com/user-attachments/assets/da0d8a18-3116-400f-a503-226a12782a41"/> <br>
upload `main.py`, `pico_i2c_lcd.py` & `max7219.py` to the pico <br>
**usage:** wave your hand under the ultrasonic sensor to trigger “far→near” crossings—each crossing increments the on-screen counter & plays a celebration animation & when no count event is active, the display reverts to zone‐based animations: “far” (>100 cm): breathing dot + distance readout, “mid” (50–100 cm): expanding circle + “i see you”, “near” (20–50 cm): bar-graph + “you're trespassing” & “close” (<20 cm): full-matrix flash + “stay away”
