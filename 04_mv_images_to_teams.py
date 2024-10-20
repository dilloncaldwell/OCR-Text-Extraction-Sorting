import os
import json
import shutil
from config import teams_dir, original_images_dir, team_mapping_file, extracted_text_mapping_file

def sort_images_by_team(teams_dir, team_mapping_file):
    # Create team directories if they don't already exist
    if not os.path.exists(teams_dir):
        os.makedirs(teams_dir)

    # Load the extracted text mapping from the JSON file
    with open(extracted_text_mapping_file, 'r') as f:
        extracted_text_mapping = json.load(f)

    # Load the team mapping from the JSON file
    with open(team_mapping_file, 'r') as f:
        team_mapping = json.load(f)

    # Loop through the extracted text mapping
    for original_file, details in extracted_text_mapping.items():
        extracted_text = details["extracted_text"]
        original_path = os.path.join(original_images_dir, original_file)
        
        # Check if any team name's keywords are found in the extracted text
        matched_team = None
        for team, data in team_mapping.items():
            keywords = data["keywords"]
            for keyword in keywords:
                if keyword.lower() in extracted_text.lower():  # Case-insensitive match
                    matched_team = team
                    break
            if matched_team:
                break
        
        if matched_team:
            # If a team is matched, move the original image to the corresponding team directory
            team_directory = os.path.join(teams_dir, matched_team)
            if not os.path.exists(team_directory):
                os.makedirs(team_directory)
            new_image_path = os.path.join(team_directory, original_file)
            shutil.move(original_path, new_image_path)  # Move the original image
            print(f"Moved '{original_file}' to team directory: '{team_directory}'")
        else:
            print(f"No matching team found for '{original_file}'. Extracted text: {extracted_text}")

# Call the function to sort images into team directories using the team mapping
sort_images_by_team(teams_dir, team_mapping_file)