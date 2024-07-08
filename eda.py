# Module: eda.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_entry_exit_times(metadata):
    metadata['vehicle_timestamp'] = pd.to_datetime(metadata['vehicle_timestamp'], format='%Y%m%d_%H%M%S')
    metadata['hour'] = metadata['vehicle_timestamp'].dt.hour
    sns.histplot(metadata['hour'], bins=24, kde=False)
    plt.title('Vehicle Entry/Exit Times')
    plt.xlabel('Hour of Day')
    plt.ylabel('Frequency')
    plt.show()

def plot_parking_occupancy(metadata):
    metadata['vehicle_timestamp'] = pd.to_datetime(metadata['vehicle_timestamp'])
    metadata['date'] = metadata['vehicle_timestamp'].dt.date
    occupancy = metadata.groupby('date').size()
    occupancy.plot(kind='bar')
    plt.title('Parking Occupancy by Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Vehicles')
    plt.show()

if __name__ == "__main__":
    from dataset_load import load_metadata

    data_dir = "data/vehicle_images"
    metadata = load_metadata(data_dir)

    if not metadata.empty:
        plot_entry_exit_times(metadata)
        plot_parking_occupancy(metadata)
    else:
        print("No metadata found.")
