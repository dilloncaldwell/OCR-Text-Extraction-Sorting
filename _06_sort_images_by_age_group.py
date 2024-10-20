import os
import shutil
import json
from _00_config import teams, age_groups, teams_dir, extracted_text_mapping_file, categories

# Age group mappings for keywords
age_group_mappings = {
    'tm': ['tm', 'tiny mites', 'tiny mights', '6U'],
    'mm': ['mm', 'mighty mites', 'tiny mights', '8U'],
    'jv': ['jv', 'junior varsity', '10U'],
    'v': ['v', 'varsity', '12U'],
}

def sort_images_by_age_group():
    # Load extracted text mapping from JSON file
    with open(extracted_text_mapping_file, 'r') as f:
        extracted_text_mapping = json.load(f)

    # Loop through each team
    for team in teams:
        team_path = os.path.join(teams_dir, team)
        
        # Check if team directory exists
        if not os.path.exists(team_path):
            print(f"Team directory {team_path} not found. Skipping...")
            continue
        
        # Loop through each category
        for category in categories:
            category_path = os.path.join(team_path, category)
            
            # Check if category directory exists
            if not os.path.exists(category_path):
                print(f"Category directory {category_path} not found. Skipping...")
                continue

            # Create age group directories if they don't exist
            for age_group in age_groups:
                age_group_path = os.path.join(category_path, age_group)
                os.makedirs(age_group_path, exist_ok=True)

            # Loop through images in extracted text mapping
            for image, info in extracted_text_mapping.items():
                preprocessed_image = info["preprocessed_image"]
                extracted_text = info["extracted_text"]

                # Determine age group based on extracted text
                for age_group, keywords in age_group_mappings.items():
                    # Check if any keyword is present in the extracted text
                    if any(keyword.upper() in extracted_text.upper() for keyword in keywords):
                        # Move the image to the appropriate age group folder
                        source_image_path = os.path.join(teams_dir, team, category, preprocessed_image)
                        destination_image_path = os.path.join(age_group_path, preprocessed_image)
                        
                        if os.path.exists(source_image_path):
                            shutil.move(source_image_path, destination_image_path)
                            print(f"Moved {preprocessed_image} to {age_group_path}")
                        # else:
                            # print(f"Image {preprocessed_image} not found in {category}. Skipping...")
                        break  # Break once age group is found

if __name__ == "__main__":
    sort_images_by_age_group()

