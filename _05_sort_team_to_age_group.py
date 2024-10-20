import os
import shutil
import json
from _00_config import teams, age_groups, teams_dir, extracted_text_mapping_file, categories

# Define the mappings for age groups
age_group_mappings = {
    'tm': ['tm', 'tiny mites', 'tiny mights', '6U'],
    'mm': ['mm', 'mighty mites', 'tiny mights', '8U'],
    'jv': ['jv', 'junior varsity', '10U'],
    'v': ['v', 'varsity', '12U'],
}

def sort_images_by_age_group():
    # Load the extracted text mapping from the JSON file
    with open(extracted_text_mapping_file, 'r') as f:
        extracted_text_mapping = json.load(f)

    for team in teams:
        team_folder_path = os.path.join(teams_dir, team)
        
        # Check if the team folder exists
        if not os.path.exists(team_folder_path):
            print(f"Team folder '{team}' does not exist. Skipping...")
            continue

        # Iterate through each image in the extracted text mapping
        for image_name, info in extracted_text_mapping.items():
            extracted_text = info['extracted_text']
            image_path = os.path.join(team_folder_path, image_name)
            
            # Check if the image exists in the team folder
            if not os.path.isfile(image_path):
                print(f"Image {image_name} not found in {team}. Skipping...")
                continue

            # Check for age group keywords in the extracted text
            for short_name, keywords in age_group_mappings.items():
                if any(keyword.upper() in extracted_text.upper() for keyword in keywords):
                    # Create the age group folder path
                    age_group_folder_path = os.path.join(team_folder_path, short_name)
                    os.makedirs(age_group_folder_path, exist_ok=True)

                    # Move the image to the corresponding age group folder
                    os.rename(image_path, os.path.join(age_group_folder_path, image_name))
                    print(f"Moved {image_name} to {age_group_folder_path}.")
                    break  # Break to avoid moving the same image multiple times

if __name__ == "__main__":
    sort_images_by_age_group()
