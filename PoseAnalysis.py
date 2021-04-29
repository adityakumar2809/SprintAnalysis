import cv2
import sys
import time
import math
import argparse
import numpy as np
from PoseDetection import PoseDetector


def getAngleBetweenVectors(vector_1, vector_2):
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = (np.arccos(dot_product) * 180 / math.pi)

    return angle


def findJointFlexAngle(landmark_values, extension_1, joint, extension_2, frame_dimensions):
    '''Find the angle being formed at the joint'''

    extension_1 = list(
        landmark_values[PoseDetector.LANDMARK_DICT[extension_1]].values()
    )[0]
    joint = list(
        landmark_values[PoseDetector.LANDMARK_DICT[joint]].values()
    )[0]
    extension_2 = list(
        landmark_values[PoseDetector.LANDMARK_DICT[extension_2]].values()
    )[0]

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
    parser = argparse.ArgumentParser(description='Detect human pose')
    parser.add_argument('--video', default=None, help='Path to input video')
    parser.add_argument('--live', action='store_true', help='Flag for livestream')
    args = parser.parse_args()
    
    if args.live and args.video:
        print('Cannot use --video and --live together')
        sys.exit()

    if args.live:
        cap = cv2.VideoCapture(0)
    elif args.video:
        cap = cv2.VideoCapture(args.video)
    else:
        print('Specify exactly one from --video and --live')
        sys.exit()

    pTime = 0
    pose_detector = PoseDetector()
    while True:
        success, img = cap.read()
        if not success:
            break

        width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        resize_ratio = 1
        resized_width = int(width/resize_ratio)
        resized_height = int(height/resize_ratio)
        img = cv2.resize(img, (resized_width, resized_height))

        img = pose_detector.findPose(img)
        landmark_values = pose_detector.findLandmarkPositions(img)
        
        angle = findJointFlexAngle(
            landmark_values,
            'left_shoulder',
            'left_elbow',
            'left_wrist',
            [resized_width, resized_height]
        )
        print(angle)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(
            img,
            str(int(fps)),
            (70, 50),
            cv2.FONT_HERSHEY_PLAIN,
            3,
            (255, 0, 0),
            3
        )
        
        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


    # img = cv2.imread('data/image_4.jpg')
    # img_height, img_width, img_channels = img.shape

    # resize_ratio = 7
    # resized_width = int(img_width/resize_ratio)
    # resized_height = int(img_height/resize_ratio)
    # img = cv2.resize(img, (resized_width, resized_height))

    # pose_detector = PoseDetector()
    # img = pose_detector.findPose(img, draw_on_image=False)
    # landmark_values = pose_detector.findLandmarkPositions(img, draw_on_image=False)

    # left_hip = list(landmark_values[PoseDetector.LANDMARK_DICT['left_hip']].values())[0]
    # left_knee = list(landmark_values[PoseDetector.LANDMARK_DICT['left_knee']].values())[0]
    # left_ankle = list(landmark_values[PoseDetector.LANDMARK_DICT['left_ankle']].values())[0]
    
    # angle = findJointFlexAngle(left_hip, left_knee, left_ankle, [resized_width, resized_height])
    # print(angle)
    
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)


if __name__ == '__main__':
    main()
