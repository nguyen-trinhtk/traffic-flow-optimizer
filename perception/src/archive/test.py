from detect import *

if __name__ == "__main__":
    model_path = "perception/models/yolov8s.pt"
    images_path = "datasets/UATRAC/test/images"
    labels_path = "datasets/UATRAC/test/labels"
    results_path = "results/perception/detection/test"
    os.makedirs(results_path, exist_ok=True)

    results = run_detection(model_path, images_path, results_path)
    
    metrics = compare_against_label(results_path, labels_path)

    print("\nEvaluation complete.")
    print(f"Metrics: {metrics}")
