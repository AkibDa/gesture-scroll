# gestures/detect.py

from learning import util

def is_fist(points):
  """
  Detects if the hand is in a fist state.
  Logic: Fingertips are close to the wrist (landmark 0).
  """
  wrist = points[0]
  # Fingertips: Index(8), Middle(12), Ring(16), Pinky(20)
  fingertips = [8, 12, 16, 20]

  count_folded = 0
  for tip_idx in fingertips:
    # Check distance between wrist and fingertip
    dist = util.get_distance([wrist, points[tip_idx]])
    # Threshold for 'folded' finger (relative to frame size usually,
    # but generic pixel value ~100 works for standard webcams)
    if dist < 100:
      count_folded += 1

  return count_folded >= 3  # If 3 or more fingers are folded

def detect_gestures(points, history=None):
  """
  Detects static poses (Pinch, Fist) and dynamic swipes.
  """
  if len(points) < 21:
    return None

  # 1. Detect FIST (Lock/Unlock trigger)
  if is_fist(points):
    return "FIST"

  # 2. Detect PINCH (Mouse Movement)
  thumb_tip = points[4]
  index_tip = points[8]
  dist = util.get_distance([thumb_tip, index_tip])

  # Check for Pinch (Index and Thumb close, Index knuckle 'up')
  if dist < 50 and util.get_angle(points[5], points[6], points[8]) > 90:
    return "PINCH"

  # 3. Detect SWIPES (Dynamic)
  # Requires history of the Index Finger Tip (point 8)
  if history and len(history) > 5:
    # Get x-coordinates of index tip from start and end of history
    start_x = history[0][8][0]
    end_x = history[-1][8][0]

    diff = end_x - start_x

    # Threshold for swipe speed/distance
    if diff > 100:
      return "SWIPE_RIGHT"
    elif diff < -100:
      return "SWIPE_LEFT"

  return None
