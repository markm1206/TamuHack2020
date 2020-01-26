import cv2
import numpy as np

video = cv2.VideoCapture(0)

while True:
    (grabbed, frame) = video.read()
    if not grabbed:
        breakq

    blur = cv2.GaussianBlur(frame, (21,21) ,0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [100,150,50]
    upper = [180,255,255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)

    imgYCC = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)#convert to YCC 

    #split color space into individual colors 
    Y , Cb , Cr = cv2.split(imgYCC)

    mean, stdD = cv2.meanStdDev(imgYCC)

    R1 = np.greater(Y,Cb)
    
    Rule1 = cv2.bitwise_and(frame,frame,mask = R1)

    #R1 = cv2.inRange(frame, lower, upper)

    print(Rule1)


    output = cv2.bitwise_and(frame, hsv, mask=mask)

    no_red = cv2.countNonZero(mask)
    cv2.imshow("original", frame)
    cv2.imshow("masked", mask)
    cv2.imshow("YCC", imgYCC)

    if int(no_red) > 10000:
        print ('Fire')
    else:
        print("_______")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video.release()