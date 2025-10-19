# train_yolov8.py
from ultralytics import YOLO
import torch

def train_yolov8(model_name='yolov8s.pt', data='datasets/UATRAC/data.yaml', epochs=100, imgsz=640, batch=16, project='runs/train', name='uatrac'):
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    print(f"Using device: {device}")

    model = YOLO(model_name)

    results = model.train(
        data=data,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        device=device,
        project=project,
        name=name,
        exist_ok=True,
        workers=4,
        optimizer='SGD',
    )

    print("\nTraining complete!")
    print("Results saved to:", results.save_dir)

if __name__ == "__main__":
    train_yolov8()
