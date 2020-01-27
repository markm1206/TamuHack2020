import cv2
import numpy as np

import serial as sl
import cv2
import numpy as np
import time 

#ar = sl.Serial('/dev/ttyACM0',9600)

try :
    ar = sl.Serial('/dev/ttyACM0',9600)
except:
    print("the board is not connected")
    runVal = False


def stop():
    ar.write(b'1')

def start():
    ar.write(b'0')

runVal = True



video = cv2.VideoCapture(0)

while True:
    try :
        ar = sl.Serial('/dev/ttyACM0',9600)
    except:
        print("the board is not connected")
    runVal = False
    (grabbed, frame) = video.read()
    if not grabbed:
        break

    blur = cv2.GaussianBlur(frame, (21,21) ,0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [122,150,50]
    upper = [180,255,255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)

    imgYCC = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)#convert to YCC 

    #split color space into individual colors 
    Y , Cb , Cr = cv2.split(imgYCC)

    mean, stdD = cv2.meanStdDev(imgYCC)

    R1 = np.greater(Y,Cb)
    
    #Rule1 = cv2.bitwise_and(frame,frame,mask = R1)

    #R1 = cv2.inRange(frame, lower, upper)

    #print(Rule1)


    output = cv2.bitwise_and(frame, hsv, mask=mask)

    no_red = cv2.countNonZero(mask)
    cv2.imshow("original", frame)
    cv2.imshow("masked", mask)
    #cv2.imshow("YCC", imgYCC)

    if int(no_red) > 15000:
        print ('Fire')
        stop()

    else:
        print("_______")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    key = cv2.waitKey(20)
    if key == 114: # reset on r
        start()

cv2.destroyAllWindows()
video.release()