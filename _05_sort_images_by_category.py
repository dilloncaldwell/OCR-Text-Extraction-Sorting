import os
import shutil
import json
import re
from _00_config import teams, categories, teams_dir, extracted_text_mapping_file

def sort_images_by_category():
    # Load the extracted text mapping from JSON
    with open(extracted_text_mapping_file, 'r') as f:
        extracted_text_mapping = json.load(f)

    # Define category mappings
    category_mappings = {
        'cheer': ['cheer', 'cheerleading', 'lead', 'heer'],
        'football': ['football', 'footbal', 'ootball', 'ball', 'foot'],  # Consider any common typos here if needed
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

        # Get a list of image files in the team folder
        image_files = [f for f in os.listdir(team_folder_path) if os.path.isfile(os.path.join(team_folder_path, f))]

        # Sort images based on categories
        for image_name in image_files:
            # Check if the image is in the extracted text mapping
            if image_name not in extracted_text_mapping:
                print(f"File '{image_name}' is not in extracted text mapping. Skipping...")
                continue
            
            source_path = os.path.join(team_folder_path, image_name)
            cleaned_text = extracted_text_mapping[image_name]['cleaned_text'].lower()
            found_category = False

            # Check each category for keywords in the cleaned text
            for category, keywords in category_mappings.items():
                # Check for direct keyword presence
                # if any(keyword in cleaned_text for keyword in keywords):
                if any(re.search(rf"{keyword}", cleaned_text.replace(" ", "")) for keyword in keywords):
                    destination_path = os.path.join(team_folder_path, category, image_name)
                    shutil.move(source_path, destination_path)
                    print(f"Moved {image_name} to {category} folder")
                    found_category = True
                    break  # Exit the category loop when match is found

            if not found_category:
                print(f"Image {image_name} did not match any category keywords. Skipping...")

if __name__ == "__main__":
    sort_images_by_category()
