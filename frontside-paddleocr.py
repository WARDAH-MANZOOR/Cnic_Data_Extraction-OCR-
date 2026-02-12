
import cv2
import numpy as np
import re
from paddleocr import PaddleOCR

def enhance_for_ocr(img_path):
    img = cv2.imread(img_path)
    if img is None: return None
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    balanced = clahe.apply(gray)
    denoised = cv2.fastNlMeansDenoising(balanced, None, 10, 7, 21)
    return cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR)

ocr = PaddleOCR(use_textline_orientation=True, lang='en')
image_path = "front/shayan-front.jpeg"
clean_img = enhance_for_ocr(image_path)

if clean_img is not None:
    result = ocr.predict(clean_img)
    if result:
        texts = [str(t).strip() for t in result[0]['rec_texts']]
        
        extracted_data = {
            "Name": "Not Found",
            "Father Name": "Not Found",
            "Gender": "Not Found",
            "Country": "Not Found",
            "Identity Number": "Not Found",
            "Date of Birth": "Not Found",
            "Date of Issue": "Not Found",
            "Date of Expiry": "Not Found"
        }

        # 1. Dates ko sahi se nikaal kar sort karna
        all_dates = [d for d in texts if re.search(r'\d{2}\.\d{2}\.\d{4}', d)]
        if len(all_dates) >= 3:
            # Dates ko Year ke mutabiq sort karenge
            # Sab se purani date = DOB, darmiyan wali = Issue, sab se late = Expiry
            sorted_dates = sorted(all_dates, key=lambda x: int(x.split('.')[-1]))
            extracted_data["Date of Birth"] = sorted_dates[0]
            extracted_data["Date of Issue"] = sorted_dates[1]
            extracted_data["Date of Expiry"] = sorted_dates[2]

        for i, t in enumerate(texts):
            text_upper = t.upper()
            
            # Identity Number
            if re.search(r'\d{5}-\d{7}-\d{1}', t):
                extracted_data["Identity Number"] = t
            
            # Name
            elif text_upper == "NAME" and i + 1 < len(texts):
                extracted_data["Name"] = texts[i+1]
                
            # 2. Father Name (Improved logic for Urdu mixed text)
            elif "FATHER" in text_upper:
                # Agar "Father Name" ke agle index mein Urdu ho, toh usse agla check karein
                # Hum next 3 strings check karte hain jo numeric na hon
                for j in range(1, 4):
                    if i + j < len(texts):
                        candidate = texts[i+j]
                        # Agar candidate mein English letters hain aur wo koi date/number nahi hai
                        if re.search('[a-zA-Z]', candidate) and not re.search(r'\d', candidate):
                            extracted_data["Father Name"] = candidate
                            break
            
            # Gender
            if re.search(r'\bF\b', text_upper): extracted_data["Gender"] = "Female"
            elif re.search(r'\bM\b', text_upper): extracted_data["Gender"] = "Male"
                
            # Country
            if "PAKISTAN" in text_upper: extracted_data["Country"] = "Pakistan"

        # Final Display
        print("\n" + "="*40)
        print("       ENHANCED EXTRACTION RESULTS")
        print("="*40)
        for key, value in extracted_data.items():
            print(f"{key:16}: {value}")
        print("="*40)


# DEATAIL RESULT
# import cv2
# import numpy as np
# import re
# from paddleocr import PaddleOCR
# import pprint  # Raw dictionary ko tameez se print karne ke liye

# def enhance_for_ocr(img_path):
#     img = cv2.imread(img_path)
#     if img is None: return None
#     img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#     balanced = clahe.apply(gray)
#     denoised = cv2.fastNlMeansDenoising(balanced, None, 10, 7, 21)
#     return cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR)

# ocr = PaddleOCR(use_textline_orientation=True, lang='en')
# image_path = "front/shayan-front.jpeg"
# clean_img = enhance_for_ocr(image_path)

# if clean_img is not None:
#     # 1. Raw Prediction
#     result = ocr.predict(clean_img)
    
#     if result:
#         # --- RAW OUTPUT PRINTING ---
#         print("\n" + "="*20 + " RAW EXTRACTION RESULTS " + "="*20)
#         # result[0] wahi dictionary hai jo aapne share ki (rec_texts, rec_scores, etc.)
#         pprint.pprint(result[0]) 
#         print("="*60 + "\n")

#         # 2. Structured Extraction Logic
#         texts = [str(t).strip() for t in result[0]['rec_texts']]
        
#         extracted_data = {
#             "Name": "Not Found",
#             "Father Name": "Not Found",
#             "Gender": "Not Found",
#             "Country": "Not Found",
#             "Identity Number": "Not Found",
#             "Date of Birth": "Not Found",
#             "Date of Issue": "Not Found",
#             "Date of Expiry": "Not Found"
#         }

#         # Dates Extraction
#         all_dates = [d for d in texts if re.search(r'\d{2}\.\d{2}\.\d{4}', d)]
#         if len(all_dates) >= 3:
#             sorted_dates = sorted(all_dates, key=lambda x: int(x.split('.')[-1]))
#             extracted_data["Date of Birth"] = sorted_dates[0]
#             extracted_data["Date of Issue"] = sorted_dates[1]
#             extracted_data["Date of Expiry"] = sorted_dates[2]

#         for i, t in enumerate(texts):
#             text_upper = t.upper()
            
#             # Identity Number (CNIC Format)
#             if re.search(r'\d{5}-\d{7}-\d{1}', t):
#                 extracted_data["Identity Number"] = t
            
#             # Name
#             elif text_upper == "NAME" and i + 1 < len(texts):
#                 extracted_data["Name"] = texts[i+1]
                
#             # Father Name
#             elif "FATHER" in text_upper:
#                 for j in range(1, 4):
#                     if i + j < len(texts):
#                         candidate = texts[i+j]
#                         if re.search('[a-zA-Z]', candidate) and not re.search(r'\d', candidate):
#                             extracted_data["Father Name"] = candidate
#                             break
            
#             # Gender
#             if re.search(r'\bF\b', text_upper): extracted_data["Gender"] = "Female"
#             elif re.search(r'\bM\b', text_upper): extracted_data["Gender"] = "Male"
                
#             # Country
#             if "PAKISTAN" in text_upper: extracted_data["Country"] = "Pakistan"

#         # --- FINAL CLEAN DISPLAY ---
#         print("\n" + "="*40)
#         print("      CLEANED ENHANCED RESULTS")
#         print("="*40)
#         for key, value in extracted_data.items():
#             print(f"{key:16}: {value}")
#         print("="*40)
