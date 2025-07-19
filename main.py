# main.py (updated)

import atexit # To ensure cleanup on exit
from speech import speak, shutdown_speech_engine
from camera_feed import get_frame
from gemini_vision import load_gemini_model as load_vision_model, describe_scene_with_gemini
from news_api import get_top_headlines, format_articles_for_gemini
import time
import cv2
import google.generativeai as genai # Import genai for text model

# Assume a function for speech-to-text (replace with your actual STT implementation)
def listen_for_command():
    """
    Placeholder for speech-to-text functionality.
    In a real application, this would use a microphone and an STT API.
    For testing, you can simulate user input.
    """
    # For demonstration, let's simulate a command
    # You would replace this with actual microphone input and STT processing.
    # For a simple test, you can uncomment the input() line.
    # command = input("Say a command (e.g., 'news', 'describe'): ").lower().strip()
    return "" # Return empty string by default, or 'news' for testing

print("👟 SceneSpeaker is starting...")

vision_model = load_vision_model()
# Load the regular Gemini Pro model for text-based tasks (like news summarization)
text_model = genai.GenerativeModel('gemini-1.5-flash')

last_description = "" # Keep track of last scene description
last_news_summary = "" # Keep track of last news summary
atexit.register(shutdown_speech_engine)

while True:
    command = listen_for_command() # Listen for user commands

    if "news" in command:
        speak("Certainly! Let me fetch the latest headlines for you.")
        articles = get_top_headlines(country='in', category='general', page_size=3) # Example: Indian news
        if articles:
            formatted_news = format_articles_for_gemini(articles)
            
            # Use Gemini to summarize/present the news in a friendly way
            try:
                news_prompt = (
                    f"Please summarize the following news headlines in a friendly and conversational tone, "
                    f"as if you're telling a friend. Keep it concise, around 2-3 sentences per headline, and engaging:\n\n{formatted_news}"
                )
                response = text_model.generate_content(
                    news_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=300
                    )
                )
                news_summary = response.text.strip()
                if news_summary and news_summary.lower() != last_news_summary.lower():
                    speak(news_summary)
                    last_news_summary = news_summary
                else:
                    print("🤔 News summary is similar to the last one, skipping speaking.")

            except Exception as e:
                print(f"❌ Error generating news summary with Gemini: {e}")
                speak("I'm sorry, I couldn't summarize the news right now.")
        else:
            speak("I couldn't find any news headlines at the moment. Please check your internet connection or API key.")
        
        # After news, maybe go back to scene description or wait for another command
        time.sleep(2) # Give some time after news
        continue # Continue to next loop iteration

    # If no specific command, or if command was not "news", proceed with scene description
    print("\n📸 Capturing scene...")
    frame = get_frame()

    if frame is None:
        print("Skipping scene description due to no frame.")
        time.sleep(1)
        continue

    description = describe_scene_with_gemini(vision_model, frame)

    if description and description.lower() != last_description.lower():
        speak(description)
        last_description = description
    else:
        print("🤔 Description is similar to the last one, skipping speaking.")

    time.sleep(5)