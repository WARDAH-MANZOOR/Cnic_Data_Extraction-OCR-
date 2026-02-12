import google.generativeai as genai
from PIL import Image
import os
import time
from dotenv import load_dotenv

# Load key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: API key not found in .env file! Please check your configuration.")
else:
    genai.configure(api_key=api_key)

def start_extraction():
    # Image path configuration
    image_path = "back/test_image1.jpeg" 
    
    if not os.path.exists(image_path):
        print(f"Error: File not found at path: '{image_path}'")
        return

    try:
        img = Image.open(image_path)
        # Using the best available model from your previous list
        model = genai.GenerativeModel(model_name='gemini-3-flash-preview')
        
        print("Processing... Please wait.")
        
        prompt = """Extract the addresses from this card. 
        Provide the output strictly in this format:
        
        PRESENT ADDRESS (Urdu): [address here]
        PRESENT ADDRESS (English): [address here]
        ---
        PERMANENT ADDRESS (Urdu): [address here]
        PERMANENT ADDRESS (English): [address here]
        """
        
        # API Call
        response = model.generate_content([prompt, img])
        
        # Printing the formatted result
        print("\n" + "="*50)
        print("          EXTRACTED ADDRESS DATA")
        print("="*50)
        print(response.text)
        print("="*50)
        
        # Saving to file for proper Urdu character rendering
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("\nNote: Please check 'result.txt' to view Urdu characters correctly.")

    except Exception as e:
        error_msg = str(e)
        
        # English Error Handling Logic
        if "429" in error_msg:
            print("\n[QUOTA ERROR]: You have exceeded your API rate limit.")
            print("Please wait 30-60 seconds before retrying or switch to a new API project.")
        elif "404" in error_msg:
            print("\n[MODEL ERROR]: The specified model was not found. Please verify the model name.")
        elif "network" in error_msg.lower() or "connection" in error_msg.lower():
            print("\n[NETWORK ERROR]: Please check your internet connection and try again.")
        else:
            print(f"\n[UNEXPECTED ERROR]: {e}")

if __name__ == "__main__":
    start_extraction()