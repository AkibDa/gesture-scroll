# gestures/detect.py

from learning import util
import config

def get_finger_state(points):
  """
  Returns a boolean list [Thumb, Index, Middle, Ring, Pinky]
  True = Extended/Up, False = Folded/Down
  """
  wrist = points[0]
  fingers_extended = [False] * 5

  # Reference size (Wrist to Middle Base)
  hand_size = util.get_distance([points[0], points[9]])

  # 1. Thumb (Check if extended away from index base)
  thumb_dist = util.get_distance([points[4], points[5]])
  if thumb_dist > (hand_size * 0.5):
    fingers_extended[0] = True

  # 2. Other Fingers (Check distance from wrist vs "folded" threshold)
  # Tips: 8(Index), 12(Middle), 16(Ring), 20(Pinky)
  tips = [8, 12, 16, 20]
  for i, tip in enumerate(tips):
    dist = util.get_distance([wrist, points[tip]])
    # If tip is far from wrist, it's extended
    if dist > (hand_size * config.FIST_THRESHOLD):
      fingers_extended[i + 1] = True  # i+1 because 0 is thumb

  return fingers_extended

def detect_gestures(points, current_depth, history=None):
  if len(points) < 21:
    return None, 0.0

  # Get state of all fingers: [Thumb, Index, Middle, Ring, Pinky]
  fingers = get_finger_state(points)

  # Unpack for clarity
  thumb_out = fingers[0]
  index_up = fingers[1]
  middle_up = fingers[2]
  ring_up = fingers[3]
  pinky_up = fingers[4]

  click_progress = 0.0

  # --- 1. SAFETY / BLOCKING ---
  # "If other fingers (Ring/Pinky) are detect then there should be no movement"
  if ring_up or pinky_up:
    # Exception: Allow "Standby" (Thumb out) check, but block cursor/swipes
    if thumb_out and not (index_up or middle_up):
      return "STANDBY", 0.0
    return None, 0.0  # Strict block for any open hand that isn't specific

  # --- 2. THUMBS UP (Like) ---
  # Fist (Index/Middle/Ring/Pinky down) + Thumb Up
  if thumb_out and not (index_up or middle_up or ring_up or pinky_up):
    # Direction check (Thumb tip above joint)
    if points[4][1] < points[3][1]:
      return "THUMBS_UP", 0.0

  # --- 3. PAUSE (Fist) ---
  # All fingers down + Thumb tucked
  if not any(fingers):
    return "PAUSE_VIDEO", 0.0

  # --- 4. SCROLL MODE (Index + Middle UP) ---
  # "Swipe should happen if movement by index and middle fingers"
  if index_up and middle_up and not thumb_out:

    # We track the MIDPOINT of Index and Middle fingers for stability
    curr_x = (points[8][0] + points[12][0]) / 2
    curr_y = (points[8][1] + points[12][1]) / 2

    if history and len(history) > 3:
      # Get old midpoint
      old_p = history[0][0]  # points from history
      start_x = (old_p[8][0] + old_p[12][0]) / 2
      start_y = (old_p[8][1] + old_p[12][1]) / 2

      diff_x = curr_x - start_x
      diff_y = curr_y - start_y

      # Use sensitive SCROLL_THRESHOLD
      hand_width = util.get_distance([points[5], points[17]])
      thresh = hand_width * config.SCROLL_THRESHOLD

      if abs(diff_x) > abs(diff_y):
        if abs(diff_x) > thresh:
          return "OPEN_COMMENTS" if diff_x > 0 else "SHARE_VIDEO", 0.0
      else:
        if abs(diff_y) > thresh:
          return "SWIPE_DOWN" if diff_y > 0 else "SWIPE_UP", 0.0

    return "SCROLL_MODE", 0.0  # State indicator

  # --- 5. CURSOR MOVE (Only Index UP) ---
  if index_up and not middle_up and not thumb_out:

    # Check Pinch for Clicking
    pinch_dist = util.get_distance([points[4], points[8]])
    hand_scale = util.get_distance([points[0], points[5]])

    max_dist = hand_scale * 0.4
    trigger_dist = hand_scale * 0.1

    if pinch_dist < max_dist:
      click_progress = (max_dist - pinch_dist) / (max_dist - trigger_dist)
      click_progress = min(1.0, max(0.0, click_progress))

    if click_progress >= 1.0:
      return "PINCH_CLICK", 1.0

    return "MOVE", click_progress

  return None, 0.0
