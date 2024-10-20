#!/bin/bash

# Run the script to create team directories
echo "Preprocesssing the images..."
python3 01_preprocess_images.py

# Run the script to 
echo "Extract text from images..."
python3 02_extract_text_from_image.py

# Run the script to create team directories
echo "Creating team directories..."
python3 03_create_team_dirs.py

# Run the script to move images to team directories
echo "Moving images to team directories..."
python3 04_mv_images_to_teams.py

echo "Done."
