import sqlite3
import json
from database import save_scan, get_recent_scans, init_db

def test_db():
    init_db()
    
    mock_data = {
        "shoe_brand": "Test Nike",
        "grade_score": 9.5,
        "condition_tier": "PADS",
        "detected_materials": [{"material": "Leather", "location": "Upper", "description": "White"}]
    }
    
    mock_images = [
        {"data": b"fake_image_data_1", "mime_type": "image/png"},
        {"data": b"fake_image_data_2", "mime_type": "image/jpeg"}
    ]
    
    print("Saving mock scan...")
    scan_id = save_scan(mock_data, mock_images)
    print(f"Saved with ID: {scan_id}")
    
    print("\nVerifying retrieval...")
    recent = get_recent_scans(1)
    if recent and recent[0]['shoe_brand'] == "Test Nike":
        print("SUCCESS: metadata retrieved.")
    else:
        print("FAILURE: metadata mismatch.")
        
    # Verify images
    conn = sqlite3.connect("shoe_scans.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM scan_images WHERE scan_id = ?", (scan_id,))
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 2:
        print("SUCCESS: 2 images stored.")
    else:
        print(f"FAILURE: expected 2 images, found {count}")

if __name__ == "__main__":
    test_db()
