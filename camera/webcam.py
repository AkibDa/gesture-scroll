# camera/webcam.py

import cv2
import time
from collections import deque
from gestures.mappings import process_frame, detector
from gestures.detect import detect_gestures
from controller.browser_control import move_mouse, perform_action

# Configuration
COOLDOWN_TIME = 1.0  # Seconds between actions
SWIPE_HISTORY_LEN = 10  # Frames to track for swipes

def main():
  cap = cv2.VideoCapture(0)

  # State Variables
  is_locked = False
  last_action_time = 0
  hud_message = "Active"
  hud_color = (0, 255, 0)

  # Stores the last N frames of landmarks for swipe detection
  point_history = deque(maxlen=SWIPE_HISTORY_LEN)

  try:
    prev_time = 0
    fps = 0

    while cap.isOpened():
      ret, frame = cap.read()
      if not ret:
        break

      # Process frame
      frame, points, depth = process_frame(frame)

      # FPS Calculation
      curr_time = time.time()
      delta = curr_time - prev_time
      if delta > 0:
        current_fps = 1 / delta
        fps = int(0.9 * fps + 0.1 * current_fps)
      prev_time = curr_time

      # --- GESTURE LOGIC ---
      if points:
        point_history.append(points)
        gesture = detect_gestures(points, list(point_history))

        # 1. Handle LOCK/UNLOCK (Fist)
        if gesture == "FIST":
          if curr_time - last_action_time > COOLDOWN_TIME:
            is_locked = not is_locked
            last_action_time = curr_time
            hud_message = "LOCKED" if is_locked else "UNLOCKED"
            hud_color = (0, 0, 255) if is_locked else (0, 255, 0)

        # 2. Handle Actions (only if NOT locked)
        if not is_locked:
          if gesture == "PINCH":
            # Continuous action, no cooldown needed usually,
            # or small cooldown if clicking
            move_mouse(points, frame.shape[:2])
            hud_message = "Mouse Moving"

          elif gesture in ["SWIPE_LEFT", "SWIPE_RIGHT"]:
            if curr_time - last_action_time > COOLDOWN_TIME:
              perform_action(gesture)
              last_action_time = curr_time
              hud_message = gesture
              # Clear history to prevent double swipe detection
              point_history.clear()
      else:
        # Clear history if hand is lost
        point_history.clear()

      # --- HUD & DRAWING ---

      # 1. Status Bar Background
      cv2.rectangle(frame, (0, 0), (frame.shape[1], 80), (30, 30, 30), -1)

      # 2. FPS
      cv2.putText(frame, f"FPS: {fps}", (frame.shape[1] - 120, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)

      # 3. Hand Depth (if available)
      if depth is not None:
        cv2.putText(frame, f"Depth: {depth:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)

      # 4. Main HUD Message (Lock status / Action)
      cv2.putText(frame, f"STATUS: {hud_message}", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, hud_color, 2)

      # 5. Cooldown Indicator (Visual Feedback)
      if curr_time - last_action_time < COOLDOWN_TIME:
        cv2.circle(frame, (frame.shape[1] - 30, 60), 10, (0, 0, 255), -1)

      cv2.imshow("Webcam", frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  finally:
    cap.release()
    cv2.destroyAllWindows()
    detector.close()
