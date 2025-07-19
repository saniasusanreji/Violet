# main.py
from object_detection import load_model, detect_objects
from scene_description import generate_description
from speech import speak
from camera_feed import get_frame
import time

print("👟 SceneSpeaker is starting...")

model = load_model()

while True:
    print("\n📸 Capturing scene...")
    frame = get_frame()
    objects = detect_objects(model, frame)
    description = generate_description(objects, frame.shape)
    speak(description)
    time.sleep(5)
