import numpy as np
from typing import List, Sequence

def detect(model, frame: np.ndarray, conf: float = 0.25) -> List[Sequence[float]]:
    if model is None:
        raise ImportError("YOLO model not available.")
    results = model(frame)
    res = results[0] if isinstance(results, (list, tuple)) else results

    boxes = getattr(res, "boxes", None)
    if boxes is None:
        return []

    xyxy = getattr(boxes, "xyxy", None)
    confs = getattr(boxes, "conf", None)
    clss = getattr(boxes, "cls", None)

    if hasattr(xyxy, "cpu"):
        xyxy = xyxy.cpu().numpy()
    if hasattr(confs, "cpu"):
        confs = confs.cpu().numpy()
    if hasattr(clss, "cpu"):
        clss = clss.cpu().numpy()

    dets: List[Sequence[float]] = []
    if xyxy is None:
        return dets

    for i, box in enumerate(xyxy):
        score = float(confs[i]) if confs is not None else 1.0
        if score < conf:
            continue
        cls = int(clss[i]) if clss is not None else -1
        x1, y1, x2, y2 = map(float, box[:4])
        dets.append([x1, y1, x2, y2, score, cls])

    return dets