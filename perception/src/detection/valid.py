from ultralytics import YOLO
import torch

def valid_yolov8(model_path='runs/train/uatrac/weights/best.pt', data='datasets/UATRAC/data.yaml', batch=16, imgsz=640):
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    print(f"Using device: {device}")

    model = YOLO(model_path)

    results = model.val(
        data=data,
        split='val',
        batch=batch,
        imgsz=imgsz,
        device=device
    )

    print("\nValidation complete!")
    print("Metrics:", results.metrics)

if __name__ == "__main__":
    valid_yolov8()