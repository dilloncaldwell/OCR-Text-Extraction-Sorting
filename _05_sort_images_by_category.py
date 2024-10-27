import os
import shutil
import json
import re
from _00_config import teams, categories, teams_dir, extracted_text_mapping_file

def clean_text(text):
    """Clean the extracted text to improve keyword matching."""
    # text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)  # Remove special characters
    # text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text.strip().lower()  # Convert to lowercase

def sort_images_by_category():
    # Load the extracted text mapping from JSON
    with open(extracted_text_mapping_file, 'r') as f:
        extracted_text_mapping = json.load(f)

    # Define category mappings
    category_mappings = {
        'cheer': ['cheer', 'cheerleading', 'lead', 'heer'],
        'football': ['football', 'footbal', 'ooball', 'ball', 'foot'],  # Consider any common typos here if needed
    }

    # Loop through each team
    for team in teams:
        team_folder_path = os.path.join(teams_dir, team)

        # Check if the team folder exists
        if not os.path.exists(team_folder_path):
            print(f"Team folder {team} does not exist. Skipping...")
            continue

        # Create category folders
        for category in categories:
            category_folder_path = os.path.join(team_folder_path, category)
            os.makedirs(category_folder_path, exist_ok=True)

        # Sort images based on categories
        for image_name, details in extracted_text_mapping.items():
            extracted_text = details['extracted_text']
            cleaned_text = clean_text(extracted_text)  # Clean the text
            print(f"Processing {image_name} with cleaned text: {cleaned_text}")  # Debug statement
            found_category = False

            # Check each category for keywords in the cleaned text
            for category, keywords in category_mappings.items():
                # Check for direct keyword presence
                if any(keyword in cleaned_text for keyword in keywords):
                    # Move the image to the corresponding category folder
                    source_path = os.path.join(team_folder_path, image_name)
                    destination_path = os.path.join(team_folder_path, category, image_name)
                    
                    if os.path.exists(source_path):
                        shutil.move(source_path, destination_path)
                        print(f"Moved {image_name} to {category} folder")
                        found_category = True
                        break  # Exit the category loop when match is found

            if not found_category:
                print(f"Image {image_name} did not match any category keywords. Skipping...")

if __name__ == "__main__":
    sort_images_by_category()
