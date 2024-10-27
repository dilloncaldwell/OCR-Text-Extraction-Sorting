import os
import cv2
import pytesseract
import json
import re
from concurrent.futures import ThreadPoolExecutor
from _00_config import preprocessed_images_dir, extracted_text_mapping_file

# Load the image mapping dictionary
mapping_file = os.path.join(preprocessed_images_dir, "image_mapping.json")
with open(mapping_file, 'r') as f:
    image_mapping = json.load(f)

# Load allowed terms from wordlist.txt into a set
def load_allowed_terms(file_path="wordlist.txt"):
    allowed_terms = set()
    with open(file_path, 'r') as file:
        for line in file:
            # Add each line as a term after stripping whitespace and converting to lowercase
            term = line.strip()
            if term:  # Only add non-empty lines
                allowed_terms.add(term.lower())
    return allowed_terms

allowed_terms = load_allowed_terms("wordlist.txt")

# Function to remove unwanted characters, extra spaces, newlines, etc.
# def clean_and_extract_text(text):
def clean_and_extract_text(text, allowed_terms):
    text = re.sub(r'[\n\r]+', ' ', text)  # Replaces all newlines with spaces
    text = re.sub(r'[|—]', '', text)  # Removes unwanted characters like | and —
    # Split the text into words, and filter to keep only allowed terms or terms longer than 3 characters
    words = text.split()
    cleaned_words = []
    for word in words:
        # Check if the word is in allowed terms or if any allowed term is found within the word
        if word.lower() in allowed_terms:
            cleaned_words.append(word)
        else:
            # Check for partial matches by seeing if any allowed term is a substring of the current word
            if any(term in word.lower() for term in allowed_terms):
                cleaned_words.append(word)
    
    # Join cleaned words back into a single string
    cleaned_text = ' '.join(cleaned_words)
    return cleaned_text.strip()

# Function to extract text from a single image using Tesseract
def extract_text_single_image(image_file, preprocessed_file, allowed_terms):
    try:
        image_path = os.path.join(preprocessed_images_dir, preprocessed_file)
        img = cv2.imread(image_path)
        if img is None:
            return None
        # Use both configurations as you mentioned
        config1 = r'--oem 1 --psm 3 -l eng --user-words wordlist.txt -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-'
        config2 = r'--oem 3 --psm 6 -l eng --user-words wordlist.txt -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-'
        config3 = r'--oem 3 --psm 12 -l eng --user-words wordlist.txt -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-'
        config4 = r'--oem 1 --psm 12 -l eng --user-words wordlist.txt -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-'
        extracted_text1 = pytesseract.image_to_string(img, config=config1).strip()
        extracted_text2 = pytesseract.image_to_string(img, config=config2).strip()
        extracted_text3 = pytesseract.image_to_string(img, config=config3).strip()
        extracted_text4 = pytesseract.image_to_string(img, config=config4).strip()
        original_combined_text = f"{extracted_text1} | {extracted_text2} | {extracted_text3} | {extracted_text4}"
        original_combined_text = re.sub(r'[\n\r]+', ' ', original_combined_text)
        # Clean and return text
        cleaned_text = clean_and_extract_text(original_combined_text, allowed_terms)
        return (image_file, original_combined_text, cleaned_text)
    except Exception as e:
        print(f"Error extracting text from {image_file}: {e}")
        return None

# Function to map images and extracted text to JSON (in parallel)
def map_extracted_text_parallel():
    extracted_text_mapping = {}
    with ThreadPoolExecutor() as executor:
        # Process images in parallel
        results = list(executor.map(lambda item: extract_text_single_image(*item, allowed_terms), image_mapping.items()))
        # Collect non-None results
        for result in results:
            if result:
                extracted_text_mapping[result[0]] = {
                    "preprocessed_image": image_mapping[result[0]],
                    "extracted_text": result[1],
                    "cleaned_text": result[2]
                }
    # Write the extracted text mapping to JSON
    with open(extracted_text_mapping_file, 'w') as json_file:
        json.dump(extracted_text_mapping, json_file, indent=4)
    print(f"Mapping saved to '{extracted_text_mapping_file}'")

# Run the parallel OCR extraction function
map_extracted_text_parallel()