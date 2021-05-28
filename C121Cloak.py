import numpy as np
import time
import cv2

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
cap = cv2.VideoCapture(0)
time.sleep(3)

count = 0
bg = 0

#Reading Background
for i in range(60):
    ret, bg = cap.read()

#Flipping background
bg = np.flip(bg, axis = 1)

while(cap.isOpened()):
    #Reading the video
    ret, img = cap.read()
    if not ret:
        break
    count = count + 1
    #Converting the colors from bgr to HSV
    img = np.flip(img, axis = 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #Generating masks to red color
    lowerRed = np.array([0, 120, 50])
    upperRed = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lowerRed, upperRed)
    lowerRed2 = np.array([170, 120, 70])
    upperRed2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lowerRed2, upperRed2)
    mask = mask1 + mask2
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    #Segment the red color part out of the frame
    mask2 = cv2.bitwise_not(mask)
    #Segment the red color part out of the frame using bitwise and with the inverted mask
    res1 = cv2.bitwise_and(img, img, mask = mask2)
    res2 = cv2.bitwise_and(bg, bg, mask = mask)
    finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)
    out.write(finalOutput)
    cv2.imshow("Magic Cloak", finalOutput)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()