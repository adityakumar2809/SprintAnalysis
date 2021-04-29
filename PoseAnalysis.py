import cv2
import math
import numpy as np
from PoseDetection import PoseDetector


def getAngleBetweenVectors(vector_1, vector_2):
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = (np.arccos(dot_product) * 180 / math.pi)

    return angle


def findJointFlexAngle(extension_1, joint, extension_2, frame_dimensions):
    '''Find the angle being formed at the joint'''
    # Consider only x and y coordinate
    extension_1 = [extension_1[0], extension_1[1]]
    joint = [joint[0], joint[1]]
    extension_2 = [extension_2[0], extension_2[1]]

    # Convert ratios into absolute length
    extension_1 = [extension_1[i] * frame_dimensions[i] for i in range(2)]
    joint = [joint[i] * frame_dimensions[i] for i in range(2)]
    extension_2 = [extension_2[i] * frame_dimensions[i] for i in range(2)]

    vector_1 = [x - y for (x, y) in zip(extension_1, joint)]
    vector_2 = [x - y for (x, y) in zip(extension_2, joint)]

    angle = getAngleBetweenVectors(vector_1, vector_2)

    return angle


def main():
    img = cv2.imread('data/image_4.jpg')
    img_height, img_width, img_channels = img.shape

    resize_ratio = 7
    resized_width = int(img_width/resize_ratio)
    resized_height = int(img_height/resize_ratio)
    img = cv2.resize(img, (resized_width, resized_height))

    pose_detector = PoseDetector()
    img = pose_detector.findPose(img, draw_on_image=False)
    landmark_values = pose_detector.findLandmarkPositions(img, draw_on_image=False)

    left_hip = list(landmark_values[PoseDetector.LANDMARK_DICT['left_hip']].values())[0]
    left_knee = list(landmark_values[PoseDetector.LANDMARK_DICT['left_knee']].values())[0]
    left_ankle = list(landmark_values[PoseDetector.LANDMARK_DICT['left_ankle']].values())[0]
    
    angle = findJointFlexAngle(left_hip, left_knee, left_ankle, [resized_width, resized_height])
    print(angle)
    
    cv2.imshow('Image', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
