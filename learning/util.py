# learning/util.py

import numpy as np
import cv2

def get_angle(a, b, c):
  radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
  angle = np.abs(np.degrees(radians))
  return angle

def get_distance(landmark_list):
  if len(landmark_list) < 2:
    return 0
  (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]
  return np.hypot(x2 - x1, y2 - y1)


def draw_bar(frame, x, y, w, h, value, color, label=""):
  """Draws a vertical progress bar."""
  # Background
  cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 50), -1)
  cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 200, 200), 1)

  # Fill
  fill_h = int(h * value)
  if fill_h > 0:
    cv2.rectangle(frame, (x, y + h - fill_h), (x + w, y + h), color, -1)

  # Label
  if label:
    cv2.putText(frame, label, (x - 10, y + h + 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

def draw_lock_icon(frame, center_x, center_y, is_locked):
  """Draws a vector lock icon."""
  color = (0, 0, 255) if is_locked else (0, 255, 0)

  # Lock Body
  cv2.rectangle(frame, (center_x - 15, center_y), (center_x + 15, center_y + 25), color, -1)

  # Lock Shackle
  if is_locked:
    # Closed shackle
    cv2.ellipse(frame, (center_x, center_y), (10, 15), 0, 180, 360, color, 3)
  else:
    # Open shackle (shifted slightly)
    cv2.ellipse(frame, (center_x + 8, center_y - 5), (10, 15), 0, 180, 360, color, 3)
