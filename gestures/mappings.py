# gestures/mappings.py

import cv2
import time
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),       # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),       # Index finger
    (0, 9), (9, 10), (10, 11), (11, 12),  # Middle finger
    (0, 13), (13, 14), (14, 15), (15, 16),# Ring finger
    (0, 17), (17, 18), (18, 19), (19, 20) # Pinky
]

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

detector = HandLandmarker.create_from_options(options)

def process_frame(frame):
    frame = cv2.flip(frame, 1)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=frameRGB
    )

    timestamp = int(time.time() * 1000)
    result = detector.detect_for_video(mp_image, timestamp)

    points = None

    if result.hand_landmarks:
        h, w, _ = frame.shape
        points = []

        for lm in result.hand_landmarks[0]:
            cx, cy = int(lm.x * w), int(lm.y * h)
            points.append((cx, cy))

        for x, y in points:
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

        for connection in HAND_CONNECTIONS:
          start_idx, end_idx = connection
          x1, y1 = points[start_idx]
          x2, y2 = points[end_idx]
          cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return frame, points
