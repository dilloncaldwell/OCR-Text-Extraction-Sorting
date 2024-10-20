import os
import json
from config import teams, categories, age_groups, teams_dir, team_mapping_file

def create_folder_structure(teams_dir, teams, categories, age_groups):
    for team in teams:
        for category in categories:
            for age_group in age_groups:
                # Create the main age group directory
                age_group_path = os.path.join(teams_dir, team, category, age_group)
                os.makedirs(age_group_path, exist_ok=True)
                # Create the coaches directory
                coaches_path = os.path.join(age_group_path, 'coaches')
                os.makedirs(coaches_path, exist_ok=True)

def create_team_mapping(teams, output_file):
    team_mapping = {}
    for team in teams:
        # Split the team name into keywords based on hyphens
        keywords = team.split('-')
        team_mapping[team] = {"keywords": keywords}
    
    # Save the team mapping to a JSON file
    with open(output_file, 'w') as f:
        json.dump(team_mapping, f, indent=4)
    print(f"Team mapping saved to {output_file}")

# if teams_dir does not exist, create it
os.makedirs(teams_dir, exist_ok=True)

create_folder_structure(teams_dir, teams, categories, age_groups)
create_team_mapping(teams, team_mapping_file)