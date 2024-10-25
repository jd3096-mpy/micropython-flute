import random
import utime
import st7789
import tft_config

import fonts.font32 as font
import fonts.font64 as fontbig


GREEN=st7789.color565(70,150,170)
BLUE=st7789.color565(33,33,50)


class SCREEN():
    def __init__(self):
        self.tft=tft_config.config(2)
        self.tft.init()
    def play(self,pic,name,trans):
        self.tft.jpg("/pics/bg.jpg",0,0,st7789.FAST)
        self.tft.png("/pics/%s.png"%(pic),36,48,True)
        self.tft.write(font, trans,130,100,GREEN,BLUE)
#         self.tft.write(font, ins,130,35,BLUE,GREEN)
        strlen = self.tft.write_len(font,name)
        self.tft.write(font,name, int((240-strlen)/2),166,st7789.WHITE,BLUE)
    def ble_pair(self):
        self.play("ble","090403","pair")
    def ble_play(self):
        self.play("ble","ble midi","#1")
    


