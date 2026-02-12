import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: API key not found in .env file!")
else:
    genai.configure(api_key=api_key)

def start_extraction():
    # Image path for the front side
    # image_path = "front/shayan-front.jpeg" 
    # image_path = "front/haider-front.jpeg" 
    image_path = "front/test_image1.jpeg" 


    
    if not os.path.exists(image_path):
        print(f"Error: File not found at path: '{image_path}'")
        return

    try:
        img = Image.open(image_path)
        # Using Gemini 1.5 Flash (optimized for speed and extraction)
        model = genai.GenerativeModel(model_name='gemini-3-flash-preview')
        
        print("Processing Front Side... Please wait.")
        
        # Updated prompt for front side data
        prompt = """Extract the following details from this CNIC front image. 
        Provide the output strictly in this format:
        
        Name            : [Name]
        Father Name     : [Father Name]
        Gender          : [Gender (M as Male, F as Female)]
        Identity Number : [Identity Number]
        Date of Birth   : [Date of Birth]
        Date of Issue   : [Date of Issue]
        Date of Expiry  : [Date of Expiry]
        """
        
        # API Call
        response = model.generate_content([prompt, img])
        
        # Printing the result
        print("\n" + "="*40)
        print("       EXTRACTED CNIC FRONT DATA")
        print("="*40)
        print(response.text)
        print("="*40)
        
        # Saving to file
        with open("cnic_front_result.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("\nData saved to 'cnic_front_result.txt'.")

    except Exception as e:
        print(f"\n[ERROR]: {e}")

if __name__ == "__main__":
    start_extraction()