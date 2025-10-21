from drawBox import drawBox
from detect import detect
from track import track

import json, os, cv2

def process_video_tracking(video_path, model, tracker, conf, save_dir, show_video):
    cap = cv2.VideoCapture(video_path)
    mapping = []

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        detections = detect(model, frame, conf)
        tracks = track(tracker, detections, frame)

        frame_tracks = [
            {str(t["track_id"]): [round(x, 2) for x in t["bbox"]]} for t in tracks
        ]
        mapping.append(frame_tracks)

        if show_video:
            for t in tracks:
                drawBox(frame, t["bbox"], track_id=t["track_id"])
            cv2.imshow("det", frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_data = {
        "video_index": video_name,
        "detections": mapping,
    }

    os.makedirs(save_dir, exist_ok=True)
    output_path = os.path.join(save_dir, f"{video_name}.json")
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=4)

    print(f"[INFO] Wrote {output_path}")


def batch_process_videos(video_dir, model, tracker, conf, save_dir, show_video):
    for video_file in os.listdir(video_dir):
        if video_file.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
            video_path = os.path.join(video_dir, video_file)
            print(f"[INFO] Processing {video_path}...")
            process_video_tracking(video_path, model, tracker, conf, save_dir, show_video)