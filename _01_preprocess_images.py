import os
import cv2
import json
from concurrent.futures import ThreadPoolExecutor
from _00_config import original_images_dir, preprocessed_images_dir

# Create a mapping dictionary to map preprocessed image filenames to original image filenames
image_mapping = {}

# Create preprocessed images directory if it doesn't exist
if not os.path.exists(preprocessed_images_dir):
    os.makedirs(preprocessed_images_dir)

# Function to preprocess a single image
def preprocess_single_image(image_file):
    try:
        original_path = os.path.join(original_images_dir, image_file)
        preprocessed_filename = f"{os.path.splitext(image_file)[0]}.jpg"
        preprocessed_path = os.path.join(preprocessed_images_dir, preprocessed_filename)
        
        original_image = cv2.imread(original_path)
        if original_image is None:
            print(f"Failed to read image: {image_file}")
            return None

        gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        cv2.imwrite(preprocessed_path, denoised)
        return (image_file, preprocessed_filename)
    
    except Exception as e:
        print(f"Error preprocessing image {image_file}: {e}")
        return None

# Function to preprocess images in parallel
def preprocess_images_parallel():
    image_mapping = {}
    with ThreadPoolExecutor() as executor:
        # List all image files
        image_files = [f for f in os.listdir(original_images_dir) if f.endswith(('.jpg', '.JPG', '.jpeg', '.png'))]
        
        # Process images in parallel
        results = list(executor.map(preprocess_single_image, image_files))
        
        # Collect non-None results
        for result in results:
            if result:
                image_mapping[result[0]] = result[1]

    # Save the mapping dictionary to a JSON file
    mapping_file = os.path.join(preprocessed_images_dir, "image_mapping.json")
    with open(mapping_file, 'w') as f:
        json.dump(image_mapping, f)
    print("Preprocessing completed and mapping saved.")

# Run the parallel preprocessing function
preprocess_images_parallel()