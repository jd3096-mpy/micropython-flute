from lib.midi_ble import MIDI_BLE
from lib.midi_device import MIDI_DEVICE
from lib.hole import HOLES
from lib.scr import SCREEN
import bluetooth
from machine import Pin,ADC
import time

    
instruments = {
    50: "Synth Strings",  # 合成弦乐合奏音色1
    51: "Synth Strings",  # 合成弦乐合奏音色2
    52: "Choir Aahs",       # 人声合唱“啊”
    53: "Voice Oohs",       # 人声“嘟”
    54: "Synth Voice",      # 合成人声
    55: "Orchestra",    # 管弦乐敲击齐奏
    56: "Trumpet",          # 小号
    57: "Trombone",         # 长号
    58: "Tuba",             # 大号
    59: "Trumpet",     # 加弱音器小号
    60: "French Horn",      # 法国号（圆号）
    61: "Brass Section",    # 铜管组（铜管乐器合奏音色）
    62: "Synth Brass",    # 合成铜管音色1
    63: "Synth Brass",    # 合成铜管音色2
    64: "Soprano",      # 高音萨克斯风
    65: "Alto",         # 次中音萨克斯风
    66: "Tenor",        # 中音萨克斯风
    67: "Baritone",     # 低音萨克斯风
    68: "Oboe",             # 双簧管
    69: "Horn",     # 英国管
    70: "Bassoon",          # 巴松（大管）
    71: "Clarinet",         # 单簧管（黑管）
    72: "Piccolo",          # 短笛
    73: "Flute",            # 长笛
    74: "Recorder",         # 竖笛
    75: "Pan Flute",        # 排箫
    76: "Bottle Blow",      # 芦笛
    77: "Shakuhachi",       # 日本尺八
    78: "Whistle",          # 口哨声
    79: "Ocarina",          # 奥卡雷那
    80: "(square)",  # 合成主音1（方波）
    81: "(sawtooth)",# 合成主音2（锯齿波）
    82: "(caliope lead)",  # 合成主音3
    83: "(chiff lead)",    # 合成主音4
    84: "(charang)",       # 合成主音5
    85: "(voice)",         # 合成主音6（人声）
    86: "(fifths)",        # 合成主音7（平行五度）
    87: "(bass+lead)",     # 合成主音8（贝司加主音）
    88: "(new age)",       # 合成音色1（新世纪）
    89: "(warm)",          # 合成音色2 （温暖）
    90: "(polysynth)"      # 合成音色3
}
ble = bluetooth.BLE()
p = MIDI_BLE(ble)

class BLE_FLUTE():
    def __init__(self):
        self.sam2695 = MIDI_DEVICE("ble",p)  
        self.scr = SCREEN()
        self.power = ADC(Pin(7))
        self.power.atten(ADC.ATTN_11DB)
        self.key = HOLES(1,2,42,41,40,39,8,21,6)
        self.set_key = Pin(0,Pin.IN,Pin.PULL_UP)
        self.x=ADC(Pin(4))
        self.y=ADC(Pin(5))
        self.x.atten(ADC.ATTN_11DB)
        self.y.atten(ADC.ATTN_11DB)
        self.mute = False
        
        self.last_key = 0
        self.pause = False
        
        self.MIN_AIR = 550
        self.MAX_AIR = 1600
        self.MIN_VOL = 88
        self.XS = 20
        self.keys = 0     #升降调
        self.ins = 56     #音色号
        self.half = 0     #半音
        
        self.sam2695.set_instrument(0,self.ins)
        
        
    def play(self):
        value = self.power.read()     #ADC原始值
        key = self.key.check()
        if value > self.MIN_AIR:      #触发演奏的最小气流
            y = flute.y.read()
            if y!=0:
                if y<500:
                    self.sam2695.set_vibrate(0, 0, 0, 0)
                elif y>2500:
                    self.sam2695.set_vibrate(0, 55, 77, 33)

            if value > self.MAX_AIR:  #限制最大气流
                value = self.MAX_AIR
            volume = self.MIN_VOL+int((value-self.MIN_AIR)/self.XS)    #折算成MIDI的volume MIN-128
            if volume > 126:                            #VOL最大126
                volume = 126 
            print('KEY:',str(key),'VOLUME:',str(volume))
            if key != 0:                                #如果按键有效则继续
                if key != self.last_key:
                    self.sam2695.set_all_notes_off(0)
                    self.sam2695.set_note_on(0,key+self.keys+self.half,volume)
                    self.mute = False
                    self.last_key = key
                else:
                    if self.pause:
                        self.sam2695.set_note_on(0,key+self.keys+self.half,volume)
                        self.pause = False
                        self.mute = False
                    else:
                        self.sam2695.set_volume(0,volume)
            else:
                if self.mute == False:
                    self.sam2695.set_all_notes_off(0)
                    self.sam2695.set_all_notes_off(0)
                    self.mute = True
            
        else:
            if self.mute == False:
                self.sam2695.set_all_notes_off(0)
                self.mute = True
                self.pause = True
            

flute=BLE_FLUTE()
flute.scr.play("flute",instruments[flute.ins],str(flute.keys))

while 1:
    if p.is_connected():
        if flute.set_key.value() == 0:
            x = flute.x.read()
            y = flute.y.read()
            print(x,y)
            if y!=0:
                if y<200 :
                    flute.keys += 1
                    flute.scr.play("flute",instruments[flute.ins],str(flute.keys))
                elif y>3600:
                    flute.keys -= 1
                    flute.scr.play("flute",instruments[flute.ins],str(flute.keys))
            if x!=0:
                if x<200 :
                    flute.ins -= 1
                    flute.sam2695.set_instrument(0,flute.ins)
                    flute.scr.play("flute",instruments[flute.ins],str(flute.keys))
                elif x>3600:
                    flute.ins += 1
                    flute.sam2695.set_instrument(0,flute.ins)
                    flute.scr.play("flute",instruments[flute.ins],str(flute.keys))
        flute.play()
    time.sleep(0.1)
