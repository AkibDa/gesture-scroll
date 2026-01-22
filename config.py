# config.py

# --- Timings ---
COOLDOWN_TIME = 0.6       # Faster reaction for scrolling
CLICK_COOLDOWN = 0.5
MOVE_DELAY = 0.1

# --- Thresholds ---
CLICK_THRESHOLD = 0.02
FIST_THRESHOLD = 0.6
SWIPE_THRESHOLD = 0.5     # General Swipe threshold
SCROLL_THRESHOLD = 0.3    # NEW: Lower threshold for 2-finger flicks
THUMB_EXTEND_THRESHOLD = 0.7

# --- Visuals ---
HISTORY_LEN = 16
HEATMAP_LEN = 50
DEBUG_MODE = True

# --- Colors ---
COLOR_LOCK = (0, 0, 255)
COLOR_ACTIVE = (0, 255, 0)
COLOR_SCROLL = (255, 0, 255) # Magenta for Scrolling
COLOR_HEATMAP = (0, 255, 255)
