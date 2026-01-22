# camera/webcam.py

import cv2
import time
import config
from collections import deque
from gestures.mappings import process_frame, detector
from gestures.detect import detect_gestures
from controller.browser_control import perform_action, click_mouse, move_mouse
from learning import util

def main():
  cap = cv2.VideoCapture(0)

  hud_message = "Ready"
  hud_color = (100, 100, 100)

  history = deque(maxlen=config.HISTORY_LEN)
  heatmap = deque(maxlen=config.HEATMAP_LEN)

  last_action_time = 0
  last_click_time = 0

  try:
    prev_time = 0
    fps = 0
    gesture = None

    while cap.isOpened():
      ret, frame = cap.read()
      if not ret: break

      frame, points, depth = process_frame(frame)
      h, w, _ = frame.shape

      # FPS
      curr_time = time.time()
      delta = curr_time - prev_time
      if delta > 1e-6: fps = int(0.9 * fps + 0.1 * (1 / delta))
      prev_time = curr_time

      click_depth_val = 0.0

      if points:

        if gesture in ["MOVE", "SCROLL_MODE"]:
          heatmap.append(points[8])

        history.append((points, depth))

        gesture, click_depth_val = detect_gestures(points, depth, list(history))

        # --- GESTURE MAPPING ---

        # 1. SCROLL / SWIPE ACTIONS
        if gesture in ["SWIPE_UP", "SWIPE_DOWN", "OPEN_COMMENTS", "SHARE_VIDEO"]:
          if curr_time - last_action_time > config.COOLDOWN_TIME:
            perform_action(gesture)
            last_action_time = curr_time
            hud_message = gesture
            hud_color = config.COLOR_SCROLL
            history.clear()
            heatmap.clear()


        # 2. MODE INDICATORS
        elif gesture == "SCROLL_MODE":
          hud_message = "2-Finger Scroll"
          hud_color = config.COLOR_SCROLL

        elif gesture == "STANDBY":
          hud_message = "STANDBY"
          hud_color = config.COLOR_LOCK
          history.clear()
          heatmap.clear()


        # 3. CLICKS & MOVES
        elif gesture == "PINCH_CLICK":
          if curr_time - last_click_time > config.CLICK_COOLDOWN:
            click_mouse()
            last_click_time = curr_time
            hud_message = "CLICK"
            history.clear()
            heatmap.clear()


        elif gesture == "MOVE":
          move_mouse(points, frame.shape[:2])
          hud_message = "Active"
          hud_color = config.COLOR_ACTIVE

        # 4. MEDIA CONTROLS
        elif gesture == "PAUSE_VIDEO":
          if curr_time - last_action_time > config.COOLDOWN_TIME:
            perform_action(gesture)
            last_action_time = curr_time
            hud_message = "PAUSED"
            hud_color = (0, 0, 255)

        elif gesture == "THUMBS_UP":
          if curr_time - last_action_time > config.COOLDOWN_TIME:
            perform_action(gesture)
            last_action_time = curr_time
            hud_message = "LIKED!"
            hud_color = (0, 255, 255)

        else:
          # If Ring/Pinky detected or undefined state
          hud_message = "Blocked"
          hud_color = (100, 100, 100)

      else:
        history.clear()
        hud_message = "No Hand"
        if len(heatmap) > 0: heatmap.popleft()

      # --- DRAW UI ---
      cv2.rectangle(frame, (0, 0), (w, 70), (30, 30, 30), -1)
      cv2.putText(frame, hud_message, (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, hud_color, 2)

      if points and gesture != "SCROLL_MODE" and gesture != "STANDBY":
        util.draw_bar(frame, w - 30, 100, 15, 150, click_depth_val, (0, 255, 255))

      if config.DEBUG_MODE:
        for pt in heatmap:
          cv2.circle(frame, pt, 3, config.COLOR_HEATMAP, -1)

      cv2.imshow("Webcam", frame)
      if cv2.waitKey(1) & 0xFF == ord('q'): break

  finally:
    cap.release()
    cv2.destroyAllWindows()
    detector.close()
