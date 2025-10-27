import os
import json

def count_total_unique_vehicles(json_dir):
    """
    Count total unique vehicle IDs across all JSON files in a directory.

    Parameters:
        json_dir (str): Path to the directory containing JSON files.

    Returns:
        int: Total number of unique vehicle IDs across all files.
    """
    total_vehicle_ids = set()
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    
    for file in json_files:
        file_path = os.path.join(json_dir, file)
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        for detection_list in data.get('detections', []):
            for detection in detection_list:
                for vid in detection.keys():
                    total_vehicle_ids.add(vid)
    
    print(f"Total unique vehicle IDs across all JSON files: {len(total_vehicle_ids)}")
    return len(total_vehicle_ids)

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    json_directory = "perception/results"
    total_count = count_total_unique_vehicles(json_directory)
