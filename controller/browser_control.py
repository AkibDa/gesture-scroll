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
  """Triggers a single left click."""
  pyautogui.click()

def perform_action(action):
  """Executes keyboard/mouse commands based on gestures."""
  if action == "SWIPE_LEFT":
    pyautogui.hotkey('ctrl', 'shift', 'tab')
  elif action == "SWIPE_RIGHT":
    pyautogui.hotkey('ctrl', 'tab')

  # Scrolling
  elif action == "SWIPE_UP":
    pyautogui.scroll(500)  # Scroll Up
  elif action == "SWIPE_DOWN":
    pyautogui.scroll(-500)  # Scroll Down
