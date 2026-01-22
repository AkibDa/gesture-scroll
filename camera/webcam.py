# camera/webcam.py

import cv2
from gestures.mappings import process_frame, detector
from gestures.detect import detect_gestures
from controller.browser_control import move_mouse

def main():
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame, points = process_frame(frame)

            if points:
                gesture = detect_gestures(points)
                if gesture == "PINCH":
                    move_mouse(points, frame.shape[:2])

            cv2.imshow("Webcam", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        detector.close()
