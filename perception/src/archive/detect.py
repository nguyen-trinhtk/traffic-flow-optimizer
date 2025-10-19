from ultralytics import YOLO
import torch, os, numpy as np

def load_yolo_labels(label_path):
    if not os.path.exists(label_path):
        return []
    try:
        data = np.loadtxt(label_path, ndmin=2)
    except ValueError:
        return []
    return [[float(x), float(y), float(w), float(h), int(cls)] for cls, x, y, w, h in data]

def iou(b1, b2):
    def to_corners(b):
        x1, y1 = b[0] - b[2] / 2, b[1] - b[3] / 2
        x2, y2 = b[0] + b[2] / 2, b[1] + b[3] / 2
        return x1, y1, x2, y2

    b1_x1, b1_y1, b1_x2, b1_y2 = to_corners(b1)
    b2_x1, b2_y1, b2_x2, b2_y2 = to_corners(b2)

    inter_x1, inter_y1 = max(b1_x1, b2_x1), max(b1_y1, b2_y1)
    inter_x2, inter_y2 = min(b1_x2, b2_x2), min(b1_y2, b2_y2)
    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

    area1, area2 = b1[2]*b1[3], b2[2]*b2[3]
    union = area1 + area2 - inter_area
    return inter_area / union if union > 0 else 0

def compute_metrics(tp, fp, fn, eps=1e-9):
    precision = tp / (tp + fp + eps)
    recall = tp / (tp + fn + eps)
    f1 = 2 * precision * recall / (precision + recall + eps)
    return precision, recall, f1

def run_detection(model_path, images_path, save_path):
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    print("Using device:", device)

    model = YOLO(model_path)
    results = model.predict(
        source=images_path,
        device=device,
        save_txt=True,
        save_conf=False,
        project=save_path,
        exist_ok=True,
    )
    return results

def compare_against_label(detection_results_path, path_to_labels, iou_threshold=0.5):
    tp = fp = fn = 0
    if not os.path.isdir(detection_results_path):
        print("Not a valid directory!")
        return None

    pred_files = []
    for root, _, files in os.walk(detection_results_path):
        for f in files:
            if f.endswith(".txt"):
                pred_files.append(os.path.join(root, f))

    for pred_path in pred_files:
        pred_name = os.path.basename(pred_path)
        gt_path = os.path.join(path_to_labels, pred_name)

        preds = load_yolo_labels(pred_path)
        gts = load_yolo_labels(gt_path)
        matched_gt = set()

        for pb in preds:
            best_iou, best_idx = 0, None
            for i, gb in enumerate(gts):
                if pb[4] != gb[4]:
                    continue
                iou_val = iou(pb, gb)
                if iou_val > best_iou:
                    best_iou, best_idx = iou_val, i

            if best_iou >= iou_threshold and best_idx not in matched_gt:
                tp += 1
                matched_gt.add(best_idx)
            else:
                fp += 1

        fn += len(gts) - len(matched_gt)

    precision, recall, f1 = compute_metrics(tp, fp, fn)
    print(f"\nPrecision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1 Score:  {f1:.3f}")
    return {"precision": precision, "recall": recall, "f1": f1}