from drawBox import drawBox
from detect import detect
from track import track
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

import json, os, cv2

def process_single_video(video_path, model, tracker, conf, save_dir, show_video=True):
    cap = cv2.VideoCapture(video_path)
    mapping = []

    if not cap.isOpened():
        print(f"[ERROR] Cannot open video: {video_path}")
        return

    print(f"[INFO] Processing video: {video_path}")

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
            cv2.imshow("Tracking", frame)

        # Press 'q' to stop early
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("[INFO] Stopped by user.")
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save results
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_data = {
        "vid_id": video_name,
        "detections": mapping,
    }

    os.makedirs(save_dir, exist_ok=True)
    output_path = os.path.join(save_dir, f"{video_name}.json")
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=4)

    print(f"[INFO] Wrote {output_path}")


if __name__ == "__main__":
    
    video_path = "dataset/ucsd_video/1.avi"
    model = YOLO("perception/model/best.pt")
    tracker = DeepSort(max_age=30)
    conf = 0.5
    save_dir = "./results"

    process_single_video(video_path, model, tracker, conf, save_dir, show_video=True)