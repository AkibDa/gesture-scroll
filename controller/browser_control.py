# controller/browser_control.py

import pyautogui

# Fail-safe
pyautogui.FAILSAFE = False

def move_mouse(points, frame_shape):
  if not points or len(points) < 9:
    return

  screen_w, screen_h = pyautogui.size()
  frame_h, frame_w = frame_shape

  x, y = points[8]

  screen_x = int(x / frame_w * screen_w)
  screen_y = int(y / frame_h * screen_h)

  pyautogui.moveTo(screen_x, screen_y, _pause=False)

def click_mouse():
  pyautogui.click()

def perform_action(action):
  """Executes keyboard commands for Reels/Shorts."""

  # --- 1. Video Navigation ---
  if action == "SWIPE_UP":
    # Swiping UP usually means "pushing" the current video away to see the NEXT one
    pyautogui.press('down')
  elif action == "SWIPE_DOWN":
    # Swiping DOWN brings the PREVIOUS video back
    pyautogui.press('up')

  # --- 2. Interaction ---
  elif action == "THUMBS_UP":
    # 'L' is common for Like on YouTube/TikTok
    pyautogui.press('l')

  elif action == "OPEN_COMMENTS":  # Swipe Right
    # 'C' often toggles captions or comments depending on platform
    pyautogui.press('c')

  elif action == "SHARE_VIDEO":  # Swipe Left
    # 'S' is a guess; varies by platform (sometimes opens Share menu)
    pyautogui.press('s')

  # --- 3. Playback ---
  elif action == "PAUSE_VIDEO":  # Fist
    pyautogui.press('space')
