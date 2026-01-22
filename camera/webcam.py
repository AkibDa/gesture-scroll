# camera/webcam.py

import cv2
import time
from collections import deque
from gestures.mappings import process_frame, detector
from gestures.detect import detect_gestures
from controller.browser_control import move_mouse, perform_action, click_mouse

# Configuration
COOLDOWN_TIME = 1.0
CLICK_COOLDOWN = 0.5
HISTORY_LEN = 10

def main():
  cap = cv2.VideoCapture(0)

  # State Variables
  is_locked = False
  last_action_time = 0
  last_click_time = 0

  hud_message = "Active"
  hud_color = (0, 255, 0)

  history = deque(maxlen=HISTORY_LEN)

  try:
    prev_time = 0
    fps = 0
    last_gesture = None

    while cap.isOpened():
      ret, frame = cap.read()
      if not ret:
        break

      frame, points, depth = process_frame(frame)

      curr_time = time.time()
      delta = curr_time - prev_time
      if delta > 1e-6:
        fps = int(0.9 * fps + 0.1 * (1 / delta))
      prev_time = curr_time

      if points:
        history.append((points, depth))
        gesture = detect_gestures(points, depth, list(history))

        # 1. LOCK/UNLOCK
        if gesture == "FIST" and last_gesture != "FIST":
          if curr_time - last_action_time > COOLDOWN_TIME:
            is_locked = not is_locked
            last_action_time = curr_time
            hud_message = "SYSTEM LOCKED" if is_locked else "Active"
            hud_color = (0, 0, 255) if is_locked else (0, 255, 0)
            history.clear()

        if not is_locked:

          # 2. CLICK
          if gesture == "PUSH_CLICK":
            if curr_time - last_click_time > CLICK_COOLDOWN:
              click_mouse()
              last_click_time = curr_time
              hud_message = "CLICK!"
              history.clear()

          # 3. SWIPES
          elif gesture in ["SWIPE_LEFT", "SWIPE_RIGHT", "SWIPE_UP", "SWIPE_DOWN"]:
            if curr_time - last_action_time > COOLDOWN_TIME:
              perform_action(gesture)
              last_action_time = curr_time
              hud_message = gesture
              history.clear()

          # 4. MOVE MOUSE (Only if gesture is explicit MOVE)
          elif gesture == "MOVE" and curr_time - last_action_time > 0.1:
            move_mouse(points, frame.shape[:2])
            hud_message = "Moving"

          # 5. PAUSE (Thumb is out)
          elif gesture == "PAUSE_CURSOR":
            hud_message = "Paused (Thumb)"

        last_gesture = gesture

      else:
        history.clear()

      # --- HUD ---
      cv2.rectangle(frame, (0, 0), (frame.shape[1], 80), (30, 30, 30), -1)

      cv2.putText(frame, f"FPS: {fps}", (frame.shape[1] - 120, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)

      # Show Z-depth for debugging clicks
      if depth is not None:
        cv2.putText(frame, f"Z: {depth:.3f}", (frame.shape[1] - 120, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)

      cv2.putText(frame, f"STATUS: {hud_message}", (10, 40),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, hud_color, 2)

      if curr_time - last_action_time < COOLDOWN_TIME:
        cv2.circle(frame, (10, 70), 8, (0, 0, 255), -1)

      cv2.imshow("Webcam", frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  finally:
    cap.release()
    cv2.destroyAllWindows()
    detector.close()
