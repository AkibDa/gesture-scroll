# camera/webcam.py

import cv2
import time
from gestures.mappings import process_frame, detector
from gestures.detect import detect_gestures
from controller.browser_control import move_mouse

def main():
    cap = cv2.VideoCapture(0)

    try:
      prev_time = 0
      fps = 0
      while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame, points, depth = process_frame(frame)
            curr_time = time.time()
            delta = curr_time - prev_time

            if delta > 0:
              current_fps = 1 / delta
              fps = int(0.9 * fps + 0.1 * current_fps)

            prev_time = curr_time

            cv2.putText(
              frame,
              f"FPS: {fps}",
              (frame.shape[1] - 120, 30),
              cv2.FONT_HERSHEY_SIMPLEX,
              0.7,
              (0, 255, 0),
              2
            )

            if depth is not None:
              cv2.putText(
                frame,
                f"Hand Depth: {depth:.2f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
              )

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
