# Module: comparing_vehicles.py
import cv2
import pytesseract
from pytesseract import Output

# Set the path to the Tesseract executable if it's not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def recognize_license_plate(image_path):
    try:
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        binary_plate = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        license_plate_text = pytesseract.image_to_string(binary_plate, config='--psm 8')  # PSM 8 for single word recognition
        return license_plate_text.strip()
    except Exception as e:
        print(f"Error recognizing license plate from {image_path}: {e}")
        return None

def match_vehicle(license_plate_text, approved_db):
    return approved_db.get(license_plate_text, "Unauthorized")

if __name__ == "__main__":
    import pandas as pd
    from dataset_load import load_metadata
    
    # Load metadata and initialize approved database
    data_dir = "data/vehicle_images"
    metadata = load_metadata(data_dir)
    approved_db = {"ABC123": "Authorized", "XYZ789": "Unauthorized"}  # Example approved database
    
    if not metadata.empty:
        image_path = metadata.iloc[0]['vehicle_image_path']
        license_plate_text = recognize_license_plate(image_path)
        
        if license_plate_text:
            status = match_vehicle(license_plate_text, approved_db)
            print(f"License Plate: {license_plate_text}, Status: {status}")
        else:
            print("License plate recognition failed.")
    else:
        print("No metadata found.")