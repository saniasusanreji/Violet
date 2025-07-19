# camera_feed.py
import cv2

def get_frame():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Cannot access the camera")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Error: Failed to capture image")
        return None

    return frame