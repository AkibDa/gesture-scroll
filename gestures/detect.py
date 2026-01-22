# gestures/detect.py

from learning import util

def detect_gestures(points):
    if len(points) < 21:
        return None

    thumb_tip = points[4]
    index_tip = points[8]

    dist = util.get_distance([thumb_tip, index_tip])

    if dist < 50 and util.get_angle(points[5], points[6], points[8]) > 90:
        return "PINCH"

    return None
