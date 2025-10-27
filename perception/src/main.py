import sys
import logging
from process import *
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

if __name__ == "__main__":
    WEIGHTS_PATH = "perception/model/best.pt"
    VIDEO_DIR = "dataset/yt"
    CONF_THRESHOLD = 0.25
    OUTPUT_DIR = "perception/results"
    SHOW_VIDEO = False

    # Suppress YOLO logging
    logging.getLogger("ultralytics").setLevel(logging.ERROR)

    # Load YOLO model
    model = YOLO(WEIGHTS_PATH)

    # Suppress DeepSort prints
    class DummyFile(object):
        def write(self, x): pass
        def flush(self): pass

    save_stdout = sys.stdout
    sys.stdout = DummyFile()
    tracker = DeepSort(max_age=30)
    sys.stdout = save_stdout

    batch_process_videos(VIDEO_DIR, model, tracker, CONF_THRESHOLD, OUTPUT_DIR, SHOW_VIDEO)