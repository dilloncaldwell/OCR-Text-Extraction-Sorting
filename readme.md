# Using Python to extract text from images and sort them

1. Add the teams to `config.py` teams array
2. Then the `preprocess_images.py` will run and prepare the images to extract text from them, and map the preprocess images to the original images
3. Then the `extract_text_from_image.py` will extract the text from the images and save a copy of the orginal images to the organized-images directory and append the name with the extracted text.
4. Then the `create_team_dirs.py` will create the directories for each team and move the images with matching names to the team directories. auto sorting them.
5. Then `mv_images_to_teams.py` will move the images from organized-images into matching teams directories using the extracted text.
6. Run `bash run_scripts.sh` to run these scripts in order.
