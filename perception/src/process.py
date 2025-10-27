from drawBox import drawBox
from detect import detect
from track import track

import json, os, cv2

def process_video_tracking(video_path, model, tracker, conf, save_dir, show_video, frame_skip=30):
    """
    frame_skip: process every 'frame_skip'-th frame
    """
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    mapping = []
    frame_idx = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        # Skip frames
        if frame_idx % frame_skip != 0:
            frame_idx += 1
            continue

        # Optional: resize frame for faster YOLO inference
        frame_resized = cv2.resize(frame, (640, 360))  # adjust size if needed

        detections = detect(model, frame_resized, conf)
        tracks = track(tracker, detections, frame_resized)

        frame_tracks = [
            {str(t["track_id"]): [round(x, 2) for x in t["bbox"]]} for t in tracks
        ]
        mapping.append(frame_tracks)

        if show_video:
            for t in tracks:
                # Scale bounding boxes back to original frame if resized
                x_scale = frame.shape[1] / frame_resized.shape[1]
                y_scale = frame.shape[0] / frame_resized.shape[0]
                bbox_scaled = [
                    t["bbox"][0]*x_scale, t["bbox"][1]*y_scale,
                    t["bbox"][2]*x_scale, t["bbox"][3]*y_scale
                ]
                drawBox(frame, bbox_scaled, track_id=t["track_id"])
            cv2.imshow("det", frame)
        print(f"Processing frame {frame_idx}/{total_frames}", end='\r')

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        frame_idx += 1

    cap.release()
    cv2.destroyAllWindows()

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_data = {
        "vid_id": video_name,
        "detections": mapping,
    }

    os.makedirs(save_dir, exist_ok=True)
    output_path = os.path.join(save_dir, f"{video_name}.json")
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=4)

    print(f"[INFO] Wrote {output_path} | Processed {len(mapping)} frames")


def batch_process_videos(video_dir, model, tracker, conf, save_dir, show_video, frame_skip=30):
    video_files = [
        f for f in os.listdir(video_dir)
        if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))
    ]
    total_videos = len(video_files)

    for idx, video_file in enumerate(video_files, start=1):
        video_path = os.path.join(video_dir, video_file)
        print(f"[INFO] Processing video {idx}/{total_videos}: {video_file}")
        process_video_tracking(video_path, model, tracker, conf, save_dir, show_video, frame_skip)

    print(f"[INFO] Finished processing {total_videos} videos.")
