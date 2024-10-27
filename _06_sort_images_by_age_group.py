import os
import shutil
import json
import re
from _00_config import teams, categories, teams_dir, extracted_text_mapping_file

def clean_text(text):
    return text.strip().lower()

def sort_images_by_age_group():
    with open(extracted_text_mapping_file, 'r') as f:
        extracted_text_mapping = json.load(f)

    age_group_mappings = {
        'tm': ['tm', 'tiny mites', 'tiny mights', '6U', 'tiny', 'tinymites', 'tinymights'],
        'mm': ['mm', 'mighty mites', 'mighty mights', '8U', 'mighty', 'mightymites', 'mightymights'],
        'jv': ['jv', 'junior varsity', '10U', 'junior', 'juniorvarsity', '10'],
        'v': ['v', 'varsity', '12U', '12'],
    }

    for team in teams:
        team_folder_path = os.path.join(teams_dir, team)

        if not os.path.exists(team_folder_path):
            print(f"Team folder {team} does not exist. Skipping...")
            continue

        for category in categories:
            category_folder_path = os.path.join(team_folder_path, category)

            if not os.path.exists(category_folder_path):
                print(f"Category folder {category} does not exist in team {team}. Skipping...")
                continue

            for image_name, details in extracted_text_mapping.items():
                extracted_text = details['extracted_text']
                cleaned_text = clean_text(extracted_text)
                found_age_group = False

                for short_name, keywords in age_group_mappings.items():
                    for keyword in keywords:
                        if len(keyword) > 3:  # For longer keywords, allow partial matching
                            if keyword.lower() in cleaned_text:
                                found_age_group = True
                        else:
                            # For shorter keywords, ensure exact word boundary matching
                            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                            if re.search(pattern, cleaned_text):
                                found_age_group = True
                        if found_age_group:
                            # Create the age group folder path inside the category folder
                            age_group_folder_path = os.path.join(category_folder_path, short_name)
                            os.makedirs(age_group_folder_path, exist_ok=True)
                            # Define source and destination paths
                            source_path = os.path.join(category_folder_path, image_name)
                            destination_path = os.path.join(age_group_folder_path, image_name)
                            if os.path.exists(source_path):
                                shutil.move(source_path, destination_path)
                                print(f"Moved {image_name} to {age_group_folder_path}.")
                                break  # Exit the keyword loop after moving the image

                    if found_age_group:
                        break  # Exit the age group loop once a match is found

                if not found_age_group:
                    print(f"Image {image_name} did not match any age group keywords. Skipping...")

if __name__ == "__main__":
    sort_images_by_age_group()