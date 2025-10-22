from process import *
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

if __name__ == "__main__":
    WEIGHTS_PATH = "perception/model/best.pt"
    VIDEO_DIR = "dataset/ucsd_video"
    CONF_THRESHOLD = 0.25
    OUTPUT_DIR = "perception/results"
    SHOW_VIDEO = False

    model = YOLO(WEIGHTS_PATH)
    tracker = DeepSort(max_age=30)

    batch_process_videos(VIDEO_DIR, model, tracker, CONF_THRESHOLD, OUTPUT_DIR, SHOW_VIDEO)
