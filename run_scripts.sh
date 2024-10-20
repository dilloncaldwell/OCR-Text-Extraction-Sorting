#!/bin/bash

# Run the script to create team directories
echo "Preprocesssing the images..."
python3 preprocess_images.py

# Run the script to 
echo "Extract text from images..."
python3 extract_text_from_image.py

# Run the script to create team directories
echo "Creating team directories..."
python3 create_team_dirs.py

# Run the script to move images to team directories
echo "Moving images to team directories..."
python3 mv_images_to_teams.py

echo "Done."
