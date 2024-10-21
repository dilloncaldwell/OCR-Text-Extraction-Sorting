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
        'cheer': ['cheer', 'cheerleading'],
        'football': ['football', 'footbal'],  # Consider any common typos here if needed
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






# import os
# import shutil
# import json
# import re
# from fuzzywuzzy import process
# from _00_config import teams, categories, teams_dir, extracted_text_mapping_file

# def clean_text(text):
#     """Clean the extracted text to improve keyword matching."""
#     text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)  # Remove special characters
#     text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
#     return text.strip().lower()  # Convert to lowercase

# def sort_images_by_category():
#     # Load the extracted text mapping from JSON
#     with open(extracted_text_mapping_file, 'r') as f:
#         extracted_text_mapping = json.load(f)

#     # Define category mappings
#     category_mappings = {
#         'cheer': ['cheer', 'cheerleading'],
#         'football': ['football', 'footbal'],  # Consider standardizing 'footbal' to 'football'
#     }

#     # Loop through each team
#     for team in teams:
#         team_folder_path = os.path.join(teams_dir, team)

#         # Check if team folder exists
#         if not os.path.exists(team_folder_path):
#             print(f"Team folder {team} does not exist. Skipping...")
#             continue

#         # Create category folders
#         for category in categories:
#             category_folder_path = os.path.join(team_folder_path, category)
#             os.makedirs(category_folder_path, exist_ok=True)

#         # Sort images based on categories
#         for image_name, details in extracted_text_mapping.items():
#             extracted_text = details['extracted_text']
#             cleaned_text = clean_text(extracted_text)  # Clean the text
#             print(f"Processing {image_name} with cleaned text: {cleaned_text}")  # Debug statement
#             found_category = False

#             # Check each category for keywords in the cleaned text
#             for category, keywords in category_mappings.items():
#                 print(f"Checking category: {category} with keywords: {keywords}")  # Debug statement
                
#                 # Use fuzzy matching to check for keyword presence
#                 best_match, score = process.extractOne(cleaned_text, keywords)
#                 print(f"Best match: '{best_match}' with score: {score}")  # Debugging output

#                 # Check if the best match score is above the threshold
#                 if score >= 50:  # Increase threshold for more accurate matching
#                     # Move the image to the corresponding category folder
#                     source_path = os.path.join(team_folder_path, image_name)
#                     destination_path = os.path.join(category_folder_path, image_name)
                    
#                     if os.path.exists(source_path):
#                         shutil.move(source_path, destination_path)
#                         print(f"Moved {image_name} to {category_folder_path}")
#                         found_category = True
#                         break  # Exit the category loop

#                 # Additionally check for direct keyword presence
#                 if any(keyword in cleaned_text for keyword in keywords):
#                     # Move the image to the corresponding category folder
#                     source_path = os.path.join(team_folder_path, image_name)
#                     destination_path = os.path.join(category_folder_path, image_name)

#                     if os.path.exists(source_path):
#                         shutil.move(source_path, destination_path)
#                         print(f"Moved {image_name} to {category_folder_path} (direct match)")
#                         found_category = True
#                         break  # Exit the category loop

#             if not found_category:
#                 print(f"Image {image_name} did not match any category keywords. Skipping...")

# if __name__ == "__main__":
#     sort_images_by_category()










# def sort_images_by_category():
#     # Load extracted text mapping from JSON file
#     with open(extracted_text_mapping_file, 'r') as f:
#         extracted_text_mapping = json.load(f)

#     # Loop through each team
#     for team in teams:
#         team_path = os.path.join(teams_dir, team)
        
#         # Check if team directory exists
#         if not os.path.exists(team_path):
#             print(f"Team directory {team_path} not found. Skipping...")
#             continue
        
#         # Create category directories if they don't exist
#         for category in categories:
#             category_path = os.path.join(team_path, category)
#             os.makedirs(category_path, exist_ok=True)

#         # Loop through images in extracted text mapping
#         for image, info in extracted_text_mapping.items():
#             preprocessed_image = info["preprocessed_image"]
#             extracted_text = info["extracted_text"]

#             # Determine category based on extracted text
#             for category in categories:
#                 if category.upper() in extracted_text.upper():  # Match category in extracted text
#                     # Move the image to the appropriate category folder
#                     source_image_path = os.path.join(teams_dir, team, preprocessed_image)
#                     destination_image_path = os.path.join(category_path, preprocessed_image)
                    
#                     if os.path.exists(source_image_path):
#                         shutil.move(source_image_path, destination_image_path)
#                         print(f"Moved {preprocessed_image} to {category_path}")
#                     else:
#                         print(f"Image {preprocessed_image} not found in {team}. Skipping...")
#                     break  # Break once category is found

# if __name__ == "__main__":
#     sort_images_by_category()
