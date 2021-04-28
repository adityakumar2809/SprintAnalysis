import cv2
import mediapipe as mp

cap = cv2.VideoCapture('data/video_1.mp4')

while True:
    success, img = cap.read()
    if not success:
        break
    
    
    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    resize_ratio = 5
    resized_width = int(width/resize_ratio)
    resized_height = int(height/resize_ratio)
    img = cv2.resize(img, (resized_width, resized_height))
    
    
    cv2.imshow('Image', img)
    cv2.waitKey(1)