import cv2
import time
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

    def findPose(self, img, draw_on_image=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(imgRGB)

        if results.pose_landmarks:
            if draw_on_image:
                self.mp_draw.draw_landmarks(
                    img,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS
                )

        return img
        
        # for index, landmark in enumerate(results.pose_landmarks.landmark):
        #     landmark_x_coord = int(landmark.x * resized_width)
        #     landmark_y_coord = int(landmark.y * resized_height)
        #     cv2.circle(img, (landmark_x_coord, landmark_y_coord), 10, (255, 0, 0), cv2.FILLED)

    

def main():
    cap = cv2.VideoCapture('data/video_1.mp4')
    pTime = 0
    pose_detector = PoseDetector()
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

        img = pose_detector.findPose(img)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        
        cv2.imshow('Image', img)
        cv2.waitKey(1)



if __name__ == '__main__':
    main()