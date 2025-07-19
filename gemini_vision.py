# gemini_vision.py
import google.generativeai as genai
import os
from PIL import Image
import io
import cv2

# Load API key from environment variable
# It's crucial to set GOOGLE_API_KEY as an environment variable
# e.g., in your terminal: export GOOGLE_API_KEY="YOUR_API_KEY"

# Or if using a .env file:
# from dotenv import load_dotenv
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# For simplicity in this example, we'll assume it's set directly for now,
# but environment variables are strongly recommended for production.
# Replace "YOUR_API_KEY" with your actual Gemini API Key
genai.configure(api_key="AIzaSyAoLRLHQiEJd5kx5ptHf9agWmg0WDK4O9g") # <<< IMPORTANT: Replace with your actual API key or use os.getenv()

def load_gemini_model():
    """Loads the Gemini Pro Vision model."""
    # Use 'gemini-pro-vision' for multimodal input (text and image)
    return genai.GenerativeModel('gemini-1.5-flash')

def describe_scene_with_gemini(model, frame_np):
    """
    Generates a human-like description of the scene using Gemini Pro Vision.

    Args:
        model: The loaded Gemini Pro Vision model.
        frame_np: The NumPy array of the image frame.

    Returns:
        A natural language description of the scene.
    """
    try:
        # Convert OpenCV frame (NumPy array) to PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(frame_np, cv2.COLOR_BGR2RGB))

        # You can provide a system instruction to guide Gemini's response.
        # This helps in making the output more human-like and suitable for a blind person.
        system_instruction = (
             "You are a helpful and friendly assistant describing the visual environment "
        "to a blind person, acting as their eyes. Always describe what is *in front of* "
        "or *around* the person, as if explaining it to them. "
        "Focus on key objects, people, their actions, and their relative positions "
        "within the scene (e.g., 'to your left', 'straight ahead'). "
        "Use natural, conversational language. Avoid directly addressing the user "
        "about themselves (e.g., do not say 'you are a girl'). "
        "Instead, describe what *you see* in the environment from the perspective of their companion. "
        "Use phrases like 'I see...', 'There's a...', 'To your right, you'll find...', 'Looks like...'"
        )

        # Create a content list with the system instruction and the image
        contents = [
            system_instruction,
            pil_image
        ]

        # Generate content with a higher temperature for more creative/diverse descriptions
        response = model.generate_content(
            contents,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7, # Adjust for creativity (higher means more creative)
                top_p=0.95,
                top_k=60,
                max_output_tokens=200 # Limit output length for conciseness
            )
        )
        return response.text.strip()

    except Exception as e:
        print(f"❌ Error describing scene with Gemini: {e}")
        return "I'm having trouble understanding what's around you right now."