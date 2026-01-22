# gestures/detect.py

from learning import util

def is_fist(points):
  """Detects if the hand is in a fist state."""
  wrist = points[0]
  fingertips = [8, 12, 16, 20]

  count_folded = 0
  for tip_idx in fingertips:
    dist = util.get_distance([wrist, points[tip_idx]])
    # Using a relative threshold based on hand size (wrist to index MCP) would be better,
    # but a fixed pixel value works for general webcams.
    hand_size = util.get_distance([points[0], points[9]])  # wrist → middle MCP

    if dist < hand_size * 0.5:
      count_folded += 1

  return count_folded >= 3

def detect_gestures(points, current_depth, history=None):
  if len(points) < 21:
    return None

  # --- 1. System Lock (Fist) ---
  if is_fist(points):
    return "FIST"

  # --- 2. Depth Click (Push) ---
  # We check if the hand moved closer to the camera significantly
  if history and len(history) > 3:
    recent = history[-5:]
    prev_depths = [entry[1] for entry in recent]
    avg_prev_depth = sum(prev_depths) / len(prev_depths)

    # Lowered threshold to 0.015 for easier clicking
    # If (Previous Depth - Current Depth) is positive, the hand got closer (Z is smaller)
    if (avg_prev_depth - current_depth) > 0.015:
      return "PUSH_CLICK"

  # --- 3. Swipes (Dynamic) ---
  if history and len(history) > 5:
    start_x = history[0][0][8][0]
    end_x = history[-1][0][8][0]
    start_y = history[0][0][8][1]
    end_y = history[-1][0][8][1]

    diff_x = end_x - start_x
    diff_y = end_y - start_y

    hand_span = util.get_distance([points[5], points[17]])  # palm width
    threshold = hand_span * 1.2

    if abs(diff_x) > abs(diff_y):
      if diff_x > threshold:
        return "SWIPE_RIGHT"
      elif diff_x < -threshold:
        return "SWIPE_LEFT"
    else:
      if diff_y > threshold:
        return "SWIPE_DOWN"
      elif diff_y < -threshold:
        return "SWIPE_UP"

  # --- 4. Cursor Movement (Conditional) ---
  # Check if Index finger is extended (Angle > 90)
  if util.get_angle(points[5], points[6], points[8]) > 90:

    # NEW: Check if Thumb is Visible/Extended
    # We compare distance of Thumb Tip(4) to Index Base(5)
    # against a reference distance (Wrist(0) to Index Base(5))
    thumb_tip_dist = util.get_distance([points[4], points[5]])
    hand_size_ref = util.get_distance([points[0], points[5]])

    # If thumb tip is far from the hand ( > 60% of palm size), it's "Visible"
    if thumb_tip_dist > (hand_size_ref * 0.6):
      return "PAUSE_CURSOR"  # Thumb is out -> Stop moving
    else:
      return "MOVE"  # Thumb is tucked -> Move

  return None
