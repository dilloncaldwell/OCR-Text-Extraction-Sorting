#!/bin/bash

# Run the script to create team directories
echo "Preprocesssing the images..."
python3 _01_preprocess_images.py

# Run the script to 
echo "Extract text from images..."
python3 _02_extract_text_from_image.py

# Run the script to create team directories
echo "Creating team directories..."
python3 _03_create_team_dirs.py

# Run the script to move images to team directories
echo "Moving images to team directories..."
python3 _04_mv_images_to_teams.py

# Run the script to move team images to category directories
echo "Moving images to team directories..."
python3 _05_sort_images_by_category.py

# Run the script to move category images to age group directories
echo "Moving images to team directories..."
python3 _06_sort_images_by_age_group.py

echo "Done."
