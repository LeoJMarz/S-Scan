import sqlite3
import json
from datetime import datetime

DB_PATH = "shoe_scans.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Scans table: basic metadata and results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            shoe_brand TEXT,
            grade_score REAL,
            condition_tier TEXT,
            full_response_json TEXT
        )
    """)
    
    # Images table: binary data linked to scans
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id INTEGER,
            image_blob BLOB,
            mime_type TEXT,
            FOREIGN KEY (scan_id) REFERENCES scans(id)
        )
    """)
    
    conn.commit()
    conn.close()

def save_scan(data, images):
    """
    Saves analysis data and images to the database.
    :param data: Dictionary of parsed AI results
    :param images: List of dicts with 'data' (bytes) and 'mime_type'
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Insert metadata
        cursor.execute("""
            INSERT INTO scans (shoe_brand, grade_score, condition_tier, full_response_json)
            VALUES (?, ?, ?, ?)
        """, (
            data.get('shoe_brand', 'Unknown'),
            data.get('grade_score', 0.0),
            data.get('condition_tier', 'Unknown'),
            json.dumps(data)
        ))
        
        scan_id = cursor.lastrowid
        
        # Insert images
        for img in images:
            cursor.execute("""
                INSERT INTO scan_images (scan_id, image_blob, mime_type)
                VALUES (?, ?, ?)
            """, (scan_id, img['data'], img['mime_type']))
        
        conn.commit()
        return scan_id
    except Exception as e:
        conn.rollback()
        print(f"Error saving to database: {e}")
        raise
    finally:
        conn.close()

def get_recent_scans(limit=10):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, timestamp, shoe_brand, grade_score, condition_tier 
        FROM scans 
        ORDER BY timestamp DESC LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
