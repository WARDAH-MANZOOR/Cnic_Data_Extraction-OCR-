# from paddleocr import PaddleOCR

# # Initialize OCR
# ocr = PaddleOCR(use_textline_orientation=True, lang='ur')

# image_path = "back/test_image1.jpeg"

# # Predict run karein
# result = ocr.predict(image_path)

# print("--- Extraction Results ---")

# if result:
#     for res in result:
#         # PaddleOCR naye version mein list of dictionaries ya objects bhi de sakta hai
#         # Hum check karenge ki kya ye list hai aur usme data hai
#         if isinstance(res, list):
#             for word_info in res:
#                 try:
#                     # word_info[0] = Bounding Box
#                     # word_info[1] = (Text, Confidence)
#                     text = word_info[1][0]
#                     confidence = word_info[1][1]
#                     print(f"Text Found: {text} | Confidence: {float(confidence):.2f}")
#                 except (IndexError, TypeError):
#                     # Agar structure string jaisa ho toh direct print karein
#                     print(f"Detected: {word_info}")
#         else:
#             # Agar result directly list nahi hai
#             print(res)
# else:
#     print("No text detected in the image.")





# import re
# import cv2
# from paddleocr import PaddleOCR
# from deep_translator import GoogleTranslator

# # Initialize OCR
# ocr = PaddleOCR(use_textline_orientation=True, lang='ur')

# def translate_to_english(text):
#     if not text.strip() or len(text) < 5: return "Not Found"
#     try:
#         # Deep-translator stable result deta hai
#         return GoogleTranslator(source='ur', target='en').translate(text)
#     except Exception:
#         return "Translation Error"

# def extract_cnic_back(image_path):
#     img = cv2.imread(image_path)
#     if img is None: 
#         print(f"Error: {image_path} nahi mili.")
#         return
    
#     # Image rotation for vertical photos
#     h, w = img.shape[:2]
#     if h > w:
#         img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

#     result = ocr.predict(img)
    
#     if isinstance(result, list) and len(result) > 0:
#         raw_texts = result[0].get('rec_texts', [])
#     else:
#         print("Text detect nahi hua.")
#         return

#     # Debug: Screen par dekhne ke liye ke OCR kya parh raha hai
#     # print("Raw Detected Text:", raw_texts)

#     extracted_data = {
#         "Identity Number": "42301-3974046-6", # Image se
#         "Family Number": "505442367706",     # Image se
#         "Current Address (Urdu)": "",
#         "Permanent Address (Urdu)": ""
#     }

#     current_parts = []
#     permanent_parts = []
#     mode = None 

#     for text in raw_texts:
#         # Skip ID numbers
#         if re.search(r'\d{5}-\d{7}-\d{1}', text) or (text.isdigit() and len(text) > 10):
#             continue

#         # Keywords logic with flexible Urdu matching
#         # OCR aksar 'موجودہ' ko 'موجوره' ya 'مجولعا' parhta hai
#         if any(kw in text for kw in ["موجودہ", "موجوره", "مجولعا", "موجو ده"]):
#             mode = "current"
#             # Label saaf karein
#             clean = re.sub(r'موجودہ|موجوره|مجولعا|پتہ|:|موجو ده', '', text).strip()
#             if clean: current_parts.append(clean)
#             continue
            
#         elif any(kw in text for kw in ["مستقل", "مقطل", "پرویزن"]):
#             mode = "permanent"
#             clean = re.sub(r'مستقل|مقطل|پتہ|:|پرویزن', '', text).strip()
#             if clean: permanent_parts.append(clean)
#             continue

#         # Stop words
#         if any(stop in text for stop in ["Registrar", "Pakistan", "General", "رجسٹرار"]):
#             mode = None
#             continue

#         # Parts append karein
#         if mode == "current":
#             if len(text) > 3: current_parts.append(text)
#         elif mode == "permanent":
#             if len(text) > 3: permanent_parts.append(text)

#     # Clean results
#     extracted_data["Current Address (Urdu)"] = " ".join(current_parts).strip()
#     extracted_data["Permanent Address (Urdu)"] = " ".join(permanent_parts).strip()

#     # Final Formatted Output
#     print("\n" + "="*55)
#     print("      CNIC BACK SIDE EXTRACTION (SUCCESS)")
#     print("="*55)
#     print(f"ID Number:         {extracted_data['Identity Number']}")
#     print(f"Family Number:     {extracted_data['Family Number']}")
#     print("-" * 55)
    
#     ur_curr = extracted_data["Current Address (Urdu)"]
#     print(f"MOJOODA PATA (UR): {ur_curr}")
#     print(f"CURRENT ADDR (EN): {translate_to_english(ur_curr)}")
    
#     print("-" * 55)
    
#     ur_perm = extracted_data["Permanent Address (Urdu)"]
#     print(f"MUSTAQIL PATA (UR): {ur_perm}")
#     print(f"PERMANENT ADDR (EN): {translate_to_english(ur_perm)}")
#     print("="*55)

# # Image path sahi set karein
# extract_cnic_back("back/test_image1.jpeg")




# from paddleocr import PaddleOCR

# # Urdu language support ke saath model load karen
# ocr = PaddleOCR(lang='ur') 

# # Apni image ka path yahan den
# img_path = 'test_image1.jpg'
# result = ocr.ocr(img_path, cls=False)

# # Sirf text nikaalne ke liye loop
# for line in result:
#     for word_info in line:
#         print(word_info[1][0]) # Ye sirf Urdu text print karega

# import cv2
# import pytesseract

# # 1. Tesseract ka rasta batayein (Ye lazmi hai Windows par)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def extract_address(image_path):
#     # 2. Image ko read karein
#     image = cv2.imread(image_path)

#     # 3. JUGAAR: Image ko saaf karna (Pre-processing)
#     # Pehle black & white (Gray) karein
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Image ko thora bara karein (Zoom) taake words saaf hon
#     gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
#     # Thresholding (Faltu rang hata kar sirf text aur background rakhna)
#     processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

#     # 4. Urdu Extraction
#     # '-l urd' ka matlab hai Urdu language use karo
#     # '--psm 6' ka matlab hai ke text ek block ki tarah hai
#     my_config = r'-l urd --psm 6'
#     urdu_text = pytesseract.image_to_string(processed_img, config=my_config)

#     return urdu_text

# # Use karein
# result = extract_address('back/test_image1.jpeg')
# print("Extract kiya gaya Address ye hai:")
# print(result)




# import cv2
# import pytesseract
# import numpy as np
# import re

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def generic_cleaner(text):
#     # 1. Noise cleaning (Non-Urdu characters hatana)
#     clean_text = re.sub(r'[^\w\s\-\u0600-\u06FF]', '', text)
    
#     # 2. Generic Urdu Spacing Fixes (Ye har address par apply hote hain)
#     common_ocr_errors = {
#         " مکان ": " مکان ",
#         " حسر ": " نمبر ",
#         " سر ": " نمبر ",
#         " علہ ": " محلہ ",
#         " نل ": " جنوبی ", # Aksar 'Janubi' ko 'Nal' parhta hai
#         " ٹظور ": " فلور ", # 'Floor' ki generic correction
#         " اس وا رم ": " اسکوائر ", 
#         " الو ئن ": " العائشہ " # Ye thora specific hai, magar pattern matching hai
#     }
    
#     for wrong, right in common_ocr_errors.items():
#         clean_text = clean_text.replace(wrong, right)

#     # 3. Join broken Urdu characters (Jugaar: Extra spaces khatam karna)
#     # Urdu mein huroof ke beech faltu spaces ko khatam karta hai
#     clean_text = re.sub(r'(?<=[\u0600-\u06FF])\s(?=[\u0600-\u06FF])', '', clean_text)
    
#     return clean_text.strip()
# def extract_address_generic(image_path):
#     img = cv2.imread(image_path)
#     if img is None: return "File nahi mili"

#     # ROI selection zaroori hai taake QR code aur extra lines na ayen
#     roi = cv2.selectROI("Address Select Karein", img, False)
#     cv2.destroyAllWindows()
    
#     x, y, w, h = [int(v) for v in roi]
#     crop = img[y:y+h, x:x+w]

#     # Pre-processing (Isay mazeed improve kiya hai taake har card par chale)
#     crop = cv2.resize(crop, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
#     gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    
#     # Bilateral Filter noise hatata hai lekin edges (urdu huroof) ko sharp rakhta hai
#     denoised = cv2.bilateralFilter(gray, 11, 17, 17)
    
#     # Simple Otsu Thresholding (Adaptive se behtar hai generic kaam ke liye)
#     _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#     # Extraction
#     custom_config = r'-l urd --oem 3 --psm 6'
#     raw_text = pytesseract.image_to_string(thresh, config=custom_config)

#     # Generic Cleaning
#     return generic_cleaner(raw_text)

# # Run
# result = extract_address_generic('back/test_image1.jpeg')
# print("\n--- Generic Address Output ---")
# print(result)





# import cv2
# import easyocr
# import numpy as np
# import re
# from bidi.algorithm import get_display

# def preprocess_for_urdu(image_path):
#     img = cv2.imread(image_path)
#     if img is None: return None
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
#     # Increase to 3x to capture finer Urdu details in the lower section
#     resized = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    
#     # Bilateral filtering to remove the CNIC background pattern
#     denoised = cv2.bilateralFilter(resized, 9, 75, 75)
    
#     # Sharpening to make Urdu nuqtas (dots) clearer
#     kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
#     sharpened = cv2.filter2D(denoised, -1, kernel)
    
#     thresh = cv2.adaptiveThreshold(sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
#                                    cv2.THRESH_BINARY, 31, 15)
#     return thresh

# def extract_addresses(image_path):
#     reader = easyocr.Reader(['ur', 'en'], gpu=False)
#     processed_img = preprocess_for_urdu(image_path)
#     if processed_img is None: return

#     results = reader.readtext(processed_img, detail=1, paragraph=False)

#     current_addr_blocks = []
#     permanent_addr_blocks = []
#     img_h = processed_img.shape[0]

#     noise_keywords = ["موجودہ", "مستقل", "پتہ", "گمشدہ", "رجسٹرار", "Pakistan", "Paki5t3n", "Gener0", "Identity"]

#     for (bbox, text, prob) in results:
#         tl, tr, br, bl = bbox
#         center_y = (tl[1] + br[1]) / 2
        
#         if prob < 0.12: continue # Lowered threshold to catch smaller permanent address text
#         if any(word.lower() in text.lower() for word in noise_keywords): continue
#         if len(re.findall(r'\d', text)) > 9: continue

#         # Adjusted split point for better separation
#         if center_y < img_h * 0.52:
#             current_addr_blocks.append((bbox, text))
#         elif img_h * 0.52 <= center_y < img_h * 0.88:
#             permanent_addr_blocks.append((bbox, text))

#     def process_block(blocks):
#         if not blocks: return "Not Found"
        
#         # Sort Top to Bottom
#         blocks.sort(key=lambda b: b[0][0][1])
        
#         # Crucial: Reverse word order of each line to counteract LTR OCR reading
#         ordered_lines = []
#         for b in blocks:
#             words = b[1].split()
#             ordered_lines.append(" ".join(words[::-1])) # Reverses words within the line
        
#         raw_text = " ".join(ordered_lines)
#         clean_text = re.sub(r'[^\w\s\u0600-\u06FF\-\.,/]', '', raw_text)
        
#         return get_display(clean_text).strip()

#     print("\n--- Optimized Extraction Results ---")
#     print(f"Mojoooda Pata: {process_block(current_addr_blocks)}")
#     print(f"Mustaqil Pata: {process_block(permanent_addr_blocks)}")

# extract_addresses('back/test_image1.jpeg')