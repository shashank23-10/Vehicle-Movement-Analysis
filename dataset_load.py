# Module: dataset-load.py
import os
import pandas as pd
import cv2

def load_metadata(data_dir):
    records = []
    for filename in os.listdir(data_dir):
        if filename.endswith("_metadata.txt"):
            with open(os.path.join(data_dir, filename), 'r') as f:
                metadata = {}
                for line in f:
                    try:
                        key, value = line.strip().split(": ")
                        metadata[key.strip()] = value.strip()
                    except ValueError:
                        continue  # Handle lines that don't split correctly

                if 'vehicle_timestamp' in metadata:
                    try:
                        # Convert timestamp to datetime format explicitly
                        metadata['vehicle_timestamp'] = pd.to_datetime(metadata['vehicle_timestamp'], format="%Y%m%d_%H%M%S")
                        records.append(metadata)
                    except ValueError:
                        print(f"Error parsing timestamp in file: {filename}")
                else:
                    print(f"Warning: 'vehicle_timestamp' not found in file: {filename}")

    return pd.DataFrame(records)

def display_sample_image(image_path):
    if not os.path.exists(image_path):
        print(f"Error: The file {image_path} does not exist.")
        return
    
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Failed to load image {image_path}.")
        return
    
    cv2.imshow('Sample Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Usage
if __name__ == "__main__":
    data_dir = "data/vehicle_images"
    metadata = load_metadata(data_dir)
    
    if not metadata.empty:
        print(metadata.head())
        display_sample_image(metadata.iloc[0]['vehicle_image_path'])
    else:
        print("No metadata found.")
