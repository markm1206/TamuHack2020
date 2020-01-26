import serial as sl
import cv2
import numpy as np
import time 


def stop():
    ar.write(b'1')

def start():
    ar.write(b'0')

runVal = True

try :
    ar = sl.Serial('/dev/ttyACM0',9600)
except:
    print("the board is not connected")
    runVal = False

while runVal:

    #stop()
    text = input("1 starts 0 stops, anything else is invalid\n")  # Python 3

    if text == '1':
        print("start")
        start()
    elif text == '0':
        print("stop")
        stop()
    else:
        print("only 1 or 0 plz")




