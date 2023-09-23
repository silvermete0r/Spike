################################
# Project: MousifAI            #
# Event: InnovateX Hackathon   #
# Environment: Python = 3.7.0  #
################################


######################################
# Importing Libraries & Dependencies #
######################################

import cv2
import numpy as np
import mediapipe as mp
from Modules import HandTrackingModule as htm
import autopy
import time

###########################
# Main System Definitions #
###########################
wCam, hCam = 640, 480
pTime = 0
frameR = 100 # Frame Reduction
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1, detectionCon=0.7, trackCon=0.7)
wScr, hScr = autopy.screen.size()
print(wScr, hScr)

########################
# Computer Vision Loop #
########################
while True:
    # 1) Find Hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2) Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:] # Index Finger
        x2, y2 = lmList[12][1:] # Middle Finger

        # 3) Check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)

        # Virtial Touchpad Zone
        cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), 
                          (255,0,255), 2)

        # 4) Only Index Finger: Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            
            # 5) Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            # 6) Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7) Move Mouse
            autopy.mouse.move(wScr-clocX, clocY)
            cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8) Both Index and thumb fingers are up: Clicking Modeq
        if fingers[1] == 1 and fingers[2] == 1:
            
            # 9) Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            
            # 10) Click mouse if distance short
            print(length)
            if length < 30:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0,255,0), cv2.FILLED)
                autopy.mouse.click()


    # 11) Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    # 12) Display
    cv2.imshow("Image", img)

    # 13) Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 14) Destroy all windows
cv2.destroyAllWindows()