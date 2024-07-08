# Module: app.py
from flask import Flask, render_template, request
import os
from dataset_load import load_metadata
from dataset_preprocess import preprocess_image
from eda import plot_entry_exit_times, plot_parking_occupancy
from comparing_vehicles import recognize_license_plate, match_vehicle
from generate_insights import generate_insights

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Load and preprocess dataset
    data_dir = "data/vehicle_images"
    metadata = load_metadata(data_dir)
    
    # Generate insights
    insights = generate_insights(metadata)

    # Debug print statements
    print("Metadata loaded:")
    print(metadata.head())
    
    print("Insights generated:")
    for key, value in insights.items():
        print(f"{key}:\n{value}\n")    

    return render_template('results.html', insights=insights)

if __name__ == '__main__':
    app.run(debug=True)
