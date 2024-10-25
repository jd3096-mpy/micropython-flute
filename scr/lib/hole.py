from machine import Pin,ADC
import time

C4 = 60
CS4 = 61
D4 = 62
DS4 = 63
E4 = 64
F4 = 65
FS4 = 66
G4 = 67
GS4 = 68
A4 = 69
AS4 = 70
B4 = 71
C5 = 72
CS5 = 73
D5 = 74
DS5 = 75
E5 = 76
F5 = 77
FS5 = 78
G5 = 79
GS5 = 80
A5 = 81
AS5 = 82
B5 = 83
C6 = 84

# key_map={
#     '11111111':C4,
#     '11111110':D4,
#     '11111100':E4,
#     '11111000':F4,
#     '11110000':G4,
#     '11100000':A4,
#     '10000000':B4,
#     '01000000':C5,
#     }

key_map={
    '11111111':C4,
    '11111101':D4,
    '11111001':E4,
    '11110001':F4,
    '11100001':G4,
    '11000001':A4,
    '10000001':B4,
    '01000001':C5,
    '11111110':C5,
    '01000000':D5,
    '11111100':D5,
    '11111000':E5,
    '11110000':F5,
    '11100000':G5,
    '11000000':A5,
    '10000000':B5,
    '01000000':C6,
    }

class HOLES():
    def __init__(self,k1,k2,k3,k4,k5,k6,k7,k8,k9):
        self.keys=[k1,k2,k3,k4,k5,k6,k7,k8]
        self.ll=Pin(k9,Pin.IN,Pin.PULL_DOWN)
        self.x = self.x=ADC(Pin(4))
        self.x.atten(ADC.ATTN_11DB)
        for k in self.keys:
            key=Pin(k,Pin.IN,Pin.PULL_UP)
    def check(self):
        check_key=''
        for k in self.keys:
            check_key+=str(int(not Pin(k).value()))
        #print(check_key)
        try:
            l=0
            if self.ll.value():
                l=12
            re=key_map[check_key]-l
            x = self.x.read()
            if x!=0:
                if x<666:
                    re -= 1
                elif x>3333:
                    re += 1
            return re
        except:
            return 0
            
