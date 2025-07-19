# speech.py
import pyttsx3

# Initialize the engine once
_engine = None

def _initialize_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty('rate', 180)  # Adjust speed
        voices = _engine.getProperty('voices')
        # Try to find a natural-sounding voice if available
        # You might need to experiment with voice indices on your system
        try:
            _engine.setProperty('voice', voices[0].id) # Default voice
            # You could loop through voices to find specific ones, e.g.,
            # for voice in voices:
            #     if "en-us" in voice.id.lower() and "female" in voice.id.lower():
            #         _engine.setProperty('voice', voice.id)
            #         break
        except IndexError:
            print("Warning: Could not set specific voice, using default.")
    return _engine

def speak(text):
    print(f"[SPEAKING]: {text}")
    engine = _initialize_engine()
    engine.say(text)
    engine.runAndWait()

# Optional: Add a function to shut down the engine cleanly
def shutdown_speech_engine():
    global _engine
    if _engine:
        _engine.stop()
        _engine = None # Reset for potential re-initialization if needed