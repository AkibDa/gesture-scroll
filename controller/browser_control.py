# controller/browser_control.py

import pyautogui

def move_mouse(points, frame_shape):
  screen_w, screen_h = pyautogui.size()
  frame_h, frame_w = frame_shape

  # Index finger tip is at index 8
  x, y = points[8]

  # Smooths the movement slightly or maps directly
  pyautogui.moveTo(
    int(x / frame_w * screen_w),
    int(y / frame_h * screen_h)
  )


def perform_action(action):
  """Executes keyboard commands based on gestures."""
  if action == "SWIPE_LEFT":
    # Example: Switch to previous tab or go back
    # Windows/Linux: Alt + Left, Mac: Command + Left
    pyautogui.hotkey('ctrl', 'shift', 'tab')
  elif action == "SWIPE_RIGHT":
    # Example: Switch to next tab
    pyautogui.hotkey('ctrl', 'tab')
