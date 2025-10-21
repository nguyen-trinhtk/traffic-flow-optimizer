import numpy as np

def track(deepsort, detections, frame: np.ndarray):
    if deepsort is None:
        raise ValueError("DeepSort instance is None")

    ds_dets = [
        ([float(d[0]), float(d[1]), float(d[2]), float(d[3])], float(d[4]), int(d[5]))
        for d in detections
    ]

    tracks_out = []
    tracks = deepsort.update_tracks(ds_dets, frame=frame)

    for tr in tracks:
        if not tr.is_confirmed():
            continue

        tid = tr.track_id
        bbox = list(map(int, tr.to_ltrb()))

        tracks_out.append({"track_id": int(tid), "bbox": bbox})

    return tracks_out
