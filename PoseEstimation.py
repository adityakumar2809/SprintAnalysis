import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture('data/video_1.mp4')
pTime = 0
while True:
    success, img = cap.read()
    if not success:
        break
    
    
    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    resize_ratio = 3
    resized_width = int(width/resize_ratio)
    resized_height = int(height/resize_ratio)
    img = cv2.resize(img, (resized_width, resized_height))

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    
    
    cv2.imshow('Image', img)
    cv2.waitKey(1)