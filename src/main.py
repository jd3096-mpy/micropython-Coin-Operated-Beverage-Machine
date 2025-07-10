'''
By jd3096
For The M5Stack Global Innovation Contest 2025
Firmware : https://github.com/russhughes/st7789_mpy/blob/master/firmware/GENERIC_S3_7789/firmware.bin
'''

from machine import Pin, SPI ,PWM ,Timer
import st7789
from encoder import Rotary
import time
import arcade as arcade_font
import duck as big_font
import _thread

#-------------------------HARDWARE INIT-------------------------

#SCREEN
tft = st7789.ST7789(
    SPI(1, baudrate=40000000, sck=Pin(6), mosi=Pin(5), miso=None),
    135,
    240,
    reset=Pin(8, Pin.OUT),
    cs=Pin(7, Pin.OUT),
    dc=Pin(4, Pin.OUT),
    backlight=Pin(9, Pin.OUT),
    rotation=1,
    options=0,
    buffer_size= 0)
tft.init()
BG = st7789.color565(22,22,22)

#ROTARY
def rotary_changed(change):
    global val,program
    if program == 1:
        if change == Rotary.ROT_CW:
            val = val + 10
        elif change == Rotary.ROT_CCW:
            val = val - 10
        if val<0:
            val = 0
        _thread.start_new_thread(beep_val, (val,))
        tft.fill_rect(36, 25, 120, 52, BG)
        tft.write(big_font, str(val) + 'ml', 36, 5, st7789.WHITE, BG)
        
rotary = Rotary(40,41,42)
rotary.add_handler(rotary_changed)

#GPIO
coin_pin = Pin(2,Pin.IN,Pin.PULL_UP)
button = Pin(15,Pin.IN,Pin.PULL_UP)

#BEEPER
beep=PWM(Pin(3))
beep.duty(0)
bump=Pin(1,Pin.OUT)

#--------------------------------PROGRAM----------------------------

#PUBLIC
coins = 0
val = 0
program = 0

def coin_calc(t):
    global coins,val
    if coin_pin.value()!=1:
        while 1:
            time.sleep_ms(30)
            if coin_pin.value()==1:
                break
        if coins<5:
            coins+=1
            val+=100
        print(coins)
        
tim=Timer(-1)
tim.init(mode=Timer.PERIODIC, freq=200, callback=coin_calc)

def beep_val(sound):
    global val
    beep.duty(555)
    beep.freq(1000 + sound*5)
    time.sleep_ms(10)
    beep.duty(0)
    
def beep_coin():
    beep.duty(555)
    beep.freq(4444)
    time.sleep_ms(100)
    beep.freq(5555)
    time.sleep_ms(100)
    beep.freq(6666)
    time.sleep_ms(100)
    beep.duty(0)

def title_ui():
    global coins,program
    program = 0
    tft.fill(BG)
    tft.jpg('bg.jpg',0,0)
    while 1:
        tft.write(arcade_font, 'INSERT COINS', 48, 102, st7789.WHITE, BG)
        time.sleep_ms(600)
        if coins!=0:
            break
        tft.fill_rect(0, 102, 240, 30, BG)
        time.sleep_ms(600)
        if coins!=0:
            break
    coins = 1
    
def select_ui():
    global val,coins,program
    program = 1
    val = 100
    tft.fill(BG)
    tft.png('coins.png', 44, 84, True)
    tft.png('alcohol.png', 166, 40, True)
    tft.write(big_font, '100ml', 36, 5,st7789.WHITE, BG)
    tft.write(arcade_font, 'X 1', 90, 97,st7789.WHITE, BG)
    now_coins = coins
    while 1:
        if now_coins != coins:
            beep_coin()
            tft.fill_rect(90, 97, 20, 24, BG)
            tft.write(arcade_font, 'X' + '  '+ str(coins), 90, 97,st7789.WHITE, BG)
            tft.fill_rect(36, 25, 120, 52, BG)
            tft.write(big_font, str(val) + 'ml', 36, 5, st7789.WHITE, BG)
            now_coins = coins
        if button.value()!=1:
            break
        
def pour_ui(): 
    global val,coins,program
    print(val)
    program = 2
    tft.fill(st7789.color565(248,228,201))
    tft.jpg('end.jpg', 66, 0)
    bump.on()
    sleep_time = int(val * 1000 / 35)
    print(sleep_time)
    time.sleep_ms(sleep_time)
    bump.off()
    time.sleep(0.6)
            
#---------------------------MAIN APP----------------------------------
while 1:
    print('start')
    title_ui()
    beep_coin()
    select_ui()
    pour_ui()
    coins = 0
    val = 1000



