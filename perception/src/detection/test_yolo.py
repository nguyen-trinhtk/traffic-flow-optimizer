from ultralytics import YOLO
import torch
import pandas as pd

PATH_TO_MODEL = "perception/model/yolov8s.pt"
DATASET_PATH = "perception/dataset/test"

# Pick MPS on Apple Silicon if available
device = "mps" if torch.backends.mps.is_available() else "cpu"
print("Using device:", device)

# Load model
model = YOLO(PATH_TO_MODEL)

# Run inference on UA-DETRAC dataset
results = model(DATASET_PATH, device=device, save=False, save_txt=True)

# Verify results against labels (basic check) 
n_imgs = len(results)
n_detected = sum(len(r.boxes) for r in results)
print(f"Processed {n_imgs} images, total detections: {n_detected}")

# Log CSV
rows = []
for r in results:
    for box in r.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = box
        rows.append({
            "image": r.path,
            "x1": x1, "y1": y1, "x2": x2, "y2": y2,
            "conf": conf, "class": int(cls)
        })
pd.DataFrame(rows).to_csv("perception/results/detection/detections.csv", index=False)

# Optional: show results
model.show()

# Save results
model.save("perception/results/detection/yolo_inference")