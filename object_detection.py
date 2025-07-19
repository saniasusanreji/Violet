# object_detection.py

import torch
from ultralytics import YOLO
from config import CONFIDENCE_THRESHOLD

def load_model():
    return YOLO('yolov8n.pt')

def detect_objects(model, frame):
    results = model(frame)[0]
    detections = []

    for r in results.boxes:
        cls = int(r.cls[0])
        conf = float(r.conf[0])
        if conf >= CONFIDENCE_THRESHOLD:
            xyxy = r.xyxy[0].tolist()
            bbox = [int(x) for x in xyxy]
            name = model.names[cls]
            detections.append({
                'name': name,
                'confidence': conf,
                'bbox': bbox
            })

    return detections
