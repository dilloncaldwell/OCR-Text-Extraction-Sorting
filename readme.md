# Using Python to extract text from images and sort them using that text

Wanted to see if I could extract text from images of football & Cheer players and sort them by their team, category, and age group.

1. Set up the config file `_00_config.py`, Add teams, directories, additional keywords for team names
2. Then the `_01_preprocess_images.py` will run and prepare the images to extract text from them, and map the preprocess images to the original images
3. Then the `_02_extract_text_from_image.py` will extract the text from the images and save a copy of the orginal images to the organized-images directory and append the name with the extracted text. Can help with recognition by adding words to look for in the `wordslist.txt` file.
4. Then the `_03_create_team_dirs.py` will create the directories for each team and move the images with matching names to the team directories. auto sorting them.
5. Then `_04_mv_images_to_teams.py` will move the images from organized-images into matching teams directories using the extracted text.
6. Then `_05_sort_images_by_category.py` will sort the images by category.
7. Then `_06_sort_images_by_age_group.py` will sort the images by age group.
8. Need to make sure the Bash scripts have executable permissions to use them `chmod +x init.sh exit.sh run_scripts.sh`
9. Can run the `init.sh` to set up virtural environment and install dependancies. `source init.sh`
10. Can run the `run_scripts.sh` to run all the scripts in order. `./run_scripts.sh`
11. Can run the `exit.sh` to deactivate the virtual environment `source exit.sh`
