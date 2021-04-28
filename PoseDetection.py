import cv2
import sys
import time
import argparse
import mediapipe as mp


class PoseDetector():
    
    def __init__(
        self,
        static_image_mode=False,
        upper_body_only=False,
        smooth_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ):
        self.static_image_mode = static_image_mode
        self.upper_body_only = upper_body_only
        self.smooth_landmarks = smooth_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            self.static_image_mode,
            self.upper_body_only,
            self.smooth_landmarks,
            self.min_detection_confidence,
            self.min_tracking_confidence
        )
        self.results = None

    def findPose(self, img, draw_on_image=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw_on_image:
                self.mp_draw.draw_landmarks(
                    img,
                    self.results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS
                )

        return img


    def findLandmarkPositions(self, img, draw_on_image=True):
        landmark_values = []      
        if self.results.pose_landmarks: 
            img_height, img_width, img_channels = img.shape
            landmarks = self.results.pose_landmarks.landmark
            for index, landmark in enumerate(landmarks):
                landmark_values.append(
                    {
                        index : [
                                    landmark.x,
                                    landmark.y,
                                    landmark.z,
                                    landmark.visibility
                                ]
                    }
                )
                if draw_on_image:
                    cv2.circle(
                        img,
                        (int(landmark.x * img_width), int(landmark.y * img_height)),
                        3,
                        (0, 0, 255),
                        cv2.FILLED
                    )

        return landmark_values

    

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
        # print(landmark_values)

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


if __name__ == '__main__':
    main()