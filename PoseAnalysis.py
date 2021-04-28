import cv2
from PoseDetection import PoseDetector


def main():
    img = cv2.imread('data/image_4.jpg')
    img_height, img_width, img_channels = img.shape
    
    resize_ratio = 7
    resized_width = int(img_width/resize_ratio)
    resized_height = int(img_height/resize_ratio)
    img = cv2.resize(img, (resized_width, resized_height))

    pose_detector = PoseDetector()
    
    cv2.imshow('Image', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
