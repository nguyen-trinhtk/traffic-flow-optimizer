from calc_metrics import *
import os
import csv
import json

def process_file(input_file, output_dir):
    with open(input_file, 'r') as f:
        data = json.load(f)

    vid_id, processed_frames = process_vid_data(data)

    csv_path = os.path.join(output_dir, f"{vid_id}.csv")

    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['avg_speed', 'density', 'flow']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for frame_data in processed_frames:
            writer.writerow(frame_data)

    print(f"Processed {input_file} -> {csv_path}")


def main():
    input_dir = "perception/results"
    output_dir = "flow_prediction/results/df"

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            input_file = os.path.join(input_dir, filename)
            process_file(input_file, output_dir)


if __name__ == "__main__":
    main()
