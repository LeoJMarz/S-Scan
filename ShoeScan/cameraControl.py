import cv2
import os

def capture_image(camera_index=0, save_path="captured_image.jpg"):
    """
    Captures an image from the specified camera.
    
    Args:
        camera_index (int): The index of the camera to use (default is 0).
        save_path (str): The path to save the captured image (default is "captured_image.jpg").
    """
    # Open the camera
    cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 50)
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}")
        return False
    
    # Capture a single frame
    ret, frame = cap.read()
    
    # Release the camera
    cap.release()
    
    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not capture frame")
        return False
    
    # Save the captured image
    cv2.imwrite(save_path, frame)
    print(f"Image saved to {save_path}")
    
    return True

if __name__ == "__main__":
    # Example usage: Capture an image from the default camera and save it as "captured_image.jpg"
    capture_image()