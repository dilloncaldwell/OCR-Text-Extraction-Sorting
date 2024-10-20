import os
import cv2
import pytesseract
import json
import re
from concurrent.futures import ThreadPoolExecutor
from _00_config import preprocessed_images_dir, original_images_dir, extracted_text_mapping_file

# Load the image mapping dictionary
mapping_file = os.path.join(preprocessed_images_dir, "image_mapping.json")
with open(mapping_file, 'r') as f:
    image_mapping = json.load(f)

# Function to remove unwanted characters, extra spaces, newlines, etc.
def clean_and_extract_text(text):
    cleaned_text = re.sub(r'[\n\r]+', ' ', text)  # Replaces all newlines with spaces
    cleaned_text = re.sub(r'[|—]', '', cleaned_text)  # Removes unwanted characters like | and —
    return cleaned_text.strip()

# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    config1 = r'--oem 1 --psm 3 -l eng --user-words wordlist.txt -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    config2 = r'--oem 3 --psm 6 -l eng --user-words wordlist.txt -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    #'-l eng' sets English as the language
    #'--oem 1' sets LSTM deep learning OCR Engine
    #'--oem 3' Default, based on what is available.
    #'--psm 3' default PSM, fully automatic
    #'--psm 6' Assume a single uniform block of vertically aligned text.
    extracted_text1 = pytesseract.image_to_string(img, config=config1).strip()
    extracted_text2 = pytesseract.image_to_string(img, config=config2).strip()
    # Combine results from both configurations
    combined_text = f"{extracted_text1} | {extracted_text2}"
    return combined_text

# Function to extract text from a single image using Tesseract
def extract_text_single_image(image_file, preprocessed_file):
    try:
        image_path = os.path.join(preprocessed_images_dir, preprocessed_file)
        img = cv2.imread(image_path)
        if img is None:
            return None
        # Use both configurations as you mentioned
        config1 = r'--oem 1 --psm 3 -l eng --user-words wordlist.txt -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        config2 = r'--oem 3 --psm 6 -l eng --user-words wordlist.txt -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        extracted_text1 = pytesseract.image_to_string(img, config=config1).strip()
        extracted_text2 = pytesseract.image_to_string(img, config=config2).strip()
        combined_text = f"{extracted_text1} | {extracted_text2}"
        # Clean and return text
        cleaned_text = clean_and_extract_text(combined_text)
        return (image_file, cleaned_text)
    except Exception as e:
        print(f"Error extracting text from {image_file}: {e}")
        return None

# Function to map images and extracted text to JSON (in parallel)
def map_extracted_text_parallel():
    extracted_text_mapping = {}
    with ThreadPoolExecutor() as executor:
        # Process images in parallel
        results = list(executor.map(lambda item: extract_text_single_image(*item), image_mapping.items()))
        # Collect non-None results
        for result in results:
            if result:
                extracted_text_mapping[result[0]] = {
                    "preprocessed_image": image_mapping[result[0]],
                    "extracted_text": result[1]
                }
    # Write the extracted text mapping to JSON
    with open(extracted_text_mapping_file, 'w') as json_file:
        json.dump(extracted_text_mapping, json_file, indent=4)
    print(f"Mapping saved to '{extracted_text_mapping_file}'")

# Run the parallel OCR extraction function
map_extracted_text_parallel()