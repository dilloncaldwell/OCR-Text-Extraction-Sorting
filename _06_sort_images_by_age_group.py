import os
import shutil
import json
import re
from _00_config import teams, categories, teams_dir, extracted_text_mapping_file

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
                source_path = os.path.join(category_folder_path, image_name)  # Updated
                if not os.path.exists(source_path):  # Only process images in the category folder
                    print(f"File {image_name} does not exist in {category_folder_path}. Skipping...")
                    continue

                cleaned_text = details['cleaned_text'].lower()
                found_age_group = False

                for short_name, keywords in age_group_mappings.items():
                    if any(keyword in cleaned_text for keyword in keywords):
                        age_group_folder_path = os.path.join(category_folder_path, short_name)
                        os.makedirs(age_group_folder_path, exist_ok=True)
                        destination_path = os.path.join(age_group_folder_path, image_name)
                        shutil.move(source_path, destination_path)
                        print(f"Moved {image_name} to {age_group_folder_path}.")
                        found_age_group = True
                        break

                if not found_age_group:
                    print(f"Image {image_name} did not match any age group keywords. Skipping...")

if __name__ == "__main__":
    sort_images_by_age_group()