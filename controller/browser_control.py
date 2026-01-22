# controller/browser_control.py

import pyautogui

def move_mouse(points, frame_shape):
    screen_w, screen_h = pyautogui.size()
    frame_h, frame_w = frame_shape

    x, y = points[8]
    pyautogui.moveTo(
        int(x / frame_w * screen_w),
        int(y / frame_h * screen_h)
    )
