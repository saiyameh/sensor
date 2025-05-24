import utime, math, machine
from machine import Pin, I2C, SPI
from pico_i2c_lcd import I2cLcd
import max7219

# ——— HARDWARE SETUP ———————————————————
lcd_i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)
lcd     = I2cLcd(lcd_i2c, 0x27, 2, 16)

spi     = SPI(0, baudrate=10_000_000, polarity=1, phase=0,
              sck=Pin(2), mosi=Pin(3))
cs      = Pin(5, Pin.OUT)
matrix  = max7219.Matrix8x8(spi, cs, 1)
matrix.brightness(5)

trig    = Pin(4, Pin.OUT)
echo    = Pin(20, Pin.IN)

def read_distance_cm():
    trig.low(); utime.sleep_us(2)
    trig.high(); utime.sleep_us(10); trig.low()
    try:
        pulse = machine.time_pulse_us(echo, 1, 30000)
        dist = (pulse / 29.1) / 2
        print(f"[DEBUG] Distance: {dist:.1f} cm")
        return dist
    except OSError:
        print("[DEBUG] Distance: out of range")
        return None

# ——— ANIMATIONS ————————————————————
def breathing_dot():
    print("[DEBUG] Zone: FAR – breathing dot")
    for b in list(range(1,8)) + list(range(8,0,-1)):
        matrix.brightness(b)
        matrix.fill(0)
        matrix.pixel(3,3,1)
        matrix.show()
        utime.sleep_ms(40)
    matrix.brightness(5)

def expanding_circle():
    print("[DEBUG] Zone: MID – expanding circle")
    for r in range(1,4):
        matrix.fill(0)
        for a in range(0,360,30):
            x = int(3 + r*math.cos(math.radians(a)))
            y = int(3 + r*math.sin(math.radians(a)))
            matrix.pixel(x,y,1)
        matrix.show()
        utime.sleep_ms(80)

def bar_graph(dist):
    print(f"[DEBUG] Zone: NEAR – bar graph ({dist:.1f} cm)")
    matrix.fill(0)
    bars = int((50-dist)/10)
    bars = max(0, min(5, bars))
    for row in range(bars):
        for col in range(8):
            matrix.pixel(col,7-row,1)
    matrix.show()

def full_flash():
    print("[DEBUG] Zone: CLOSE – full flash")
    for _ in range(3):
        matrix.fill(1); matrix.show()
        utime.sleep_ms(120)
        matrix.fill(0); matrix.show()
        utime.sleep_ms(120)

def celebration():
    print("[DEBUG] Event: COUNT INCREMENT – celebration")
    coords = [(3,3),(4,3),(4,4),(3,4),
              (2,2),(5,2),(5,5),(2,5),
              (1,1),(6,1),(6,6),(1,6)]
    for x,y in coords:
        matrix.fill(0); matrix.pixel(x,y,1); matrix.show()
        utime.sleep_ms(60)
    matrix.fill(1); matrix.show()
    utime.sleep_ms(200)
    matrix.fill(0); matrix.show()

def show_count_bar(count):
    print(f"[DEBUG] Displaying count: {count}")
    matrix.fill(0)
    n = count % 8 or 8
    for c in range(n):
        for r in range(8):
            matrix.pixel(c,7-r,1)
    matrix.show()

# ——— MAIN LOOP WITH COUNT LOGIC ———————————————————
count = 0
prev_far = True
displaying_count = False
count_display_until = 0

print("=== Proximity Counter Started ===")
while True:
    d = read_distance_cm()
    now = utime.ticks_ms()

    if displaying_count:
        if utime.ticks_diff(now, count_display_until) < 3000:
            show_count_bar(count)
            lcd.clear()
            lcd.putstr(f"Count: {count}")
            utime.sleep_ms(200)
            continue
        else:
            print("[DEBUG] Returning to ambient mode")
            displaying_count = False

    if d is not None:
        is_far  = d > 80
        is_near = d < 40

        if prev_far and is_near:
            count += 1
            print(f"[INFO] Person counted! Total = {count}")
            celebration()
            displaying_count = True
            count_display_until = utime.ticks_add(now, 3000)
        prev_far = is_far

    lcd.clear()
    if d is None or d > 100:
        breathing_dot()
        lcd.putstr(f"D:{(d or 0):>3.0f}cm")
    elif d > 50:
        expanding_circle()
        lcd.putstr("i see you")
    elif d > 20:
        bar_graph(d)
        lcd.putstr("you're trespassing")
    else:
        full_flash()
        lcd.putstr("stay away")

    utime.sleep_ms(150)
