import cv2
import numpy as np

def drawBox(frame: np.ndarray, bbox, track_id=None, color=(0, 255, 0), thickness=2):
    x1, y1, x2, y2 = map(int, bbox)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

    if track_id is not None:
        cv2.putText(
            frame,
            str(int(track_id)),
            (x1, max(0, y1 - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            1
        )

    return frame
