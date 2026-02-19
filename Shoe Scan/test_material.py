import json
from model_call import grade
import os

def test_grade():
    image_path = "imgs/1.png"
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        return

    with open(image_path, "rb") as f:
        image_data = f.read()

    images_to_process = [{
        "data": image_data,
        "mime_type": "image/png"
    }]

    print("Running analysis...")
    raw_response = grade(images_to_process)
    print("Raw Response received.")
    
    try:
        data = json.loads(raw_response)
        print("JSON parsed successfully.")
        print(f"Shoe Brand: {data.get('shoe_brand')}")
        print(f"Materials: {data.get('detected_materials')}")
        
        if 'detected_materials' in data:
            print("SUCCESS: detected_materials field found.")
        else:
            print("FAILURE: detected_materials field missing.")
            
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw response: {raw_response}")

if __name__ == "__main__":
    test_grade()
