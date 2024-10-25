"""Generic ESP32 with ST7789 240x320 display"""

from machine import Pin, SPI
import st7789

TFA = 0
BFA = 0

def config(rotation=0, buffer_size=0, options=0):
    return st7789.ST7789(
        SPI(1,baudrate=40000000, polarity=1, phase=1, sck=Pin(12), mosi=Pin(11)),
        240,
        240,
        cs=Pin(10, Pin.OUT),
        dc=Pin(14, Pin.OUT),
        rotation=rotation,
        options=options,
        buffer_size=buffer_size)

# ss=config(1)
# ss.init()
# ss.fill(st7789.RED)