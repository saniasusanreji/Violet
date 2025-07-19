import pyttsx3

def speak(text):
    print(f"[SPEAKING]: {text}")
    engine = pyttsx3.init()  # Re-initialize engine every time to avoid freezing
    engine.setProperty('rate', 180)  # Adjust speed (optional)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # You can change index if needed
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Properly close engine
