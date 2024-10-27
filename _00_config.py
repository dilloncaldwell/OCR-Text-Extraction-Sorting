teams = [
    'boger-city-optimists', 
    'carolina-bears', 
    'cleveland-seminoles',
    'cramerton-panthers',
    'east-lincoln-mustangs',
    'gyso-huskies',
    'kings-mountain-elite',
    'mt-view-tigers',
    'next-level-spartans',
    'port-city-gators',
    'southern-masterminds',
    'west-carolina-ducks'
]
categories = ['cheer', 'football']
age_groups = ['tm', 'mm', 'jv', 'v']

# Add addtional keywords to the team_mppings.json file other then team name, mapped to teams index
team_additional_keywords = {
    0: ['BOGERCITYOPTIMIST'], 
    1: [],  
    2: [], 
    3: [], 
    4: ['angs'], 
    5: [], 
    6: ['kmelite'], 
    7: ['VIEWTIGERS', 'MT.VIEWTIGERS'], 
    8: [], 
    9: [], 
    10: [], 
    11: ['wcyso'], 
}

# Path to the directory where team folders is created for sorting the images
teams_dir = "teams"
# Path to the directory where preprocessed images will be saved
preprocessed_images_dir = "preprocessed-images"
# Path to the directory containing the original images
original_images_dir = "original-images"
# Path to the JSON file containing the team mapping and keywords to look for to match
team_mapping_file = "team_mapping.json"
# Path to JSON file that maps original image to preprocessed image and the extracted text
extracted_text_mapping_file = "extracted_text_mapping.json"

