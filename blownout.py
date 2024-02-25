from PIL import Image
import os

def is_image_blowout(image_path, white_threshold=230, blowout_percentage=20):
    """
    Check if an image has a high amount of white.
    :param image_path: Path to the image file.
    :param white_threshold: The minimum value to consider a pixel 'white'. Default is 230 (on a scale of 0-255).
    :param blowout_percentage: The percentage of white pixels at which we consider the image 'blown out'.
    :return: True if the image is blown out, False otherwise.
    """
    try:
        image = Image.open(image_path)
        if image.mode != 'RGB':
            # Convert non-RGB images to RGB
            image = image.convert('RGB')
        pixels = list(image.getdata())
        white_pixels = [pixel for pixel in pixels if all(val > white_threshold for val in pixel)]
        
        white_ratio = (len(white_pixels) / len(pixels)) * 100
        return white_ratio > blowout_percentage
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False


# Define your source directory
source_dir = '/Volumes/Solardisk/scraper_all_images_flat/testwhite'

# Output file to save the filenames
output_file = '/Volumes/Solardisk/scraper_all_images_flat/testwhite/not_blown_out_images.txt'

# Get a sorted list of filenames in the source directory
sorted_filenames = sorted(os.listdir(source_dir))

# Open the output file in write mode
with open(output_file, 'w') as file:
    # Loop through the sorted list of filenames
    for filename in sorted_filenames:
        file_path = os.path.join(source_dir, filename)
        # Check if the file is an image (for simplicity, checking extension only)
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            # If the image is not blown out, write its filename to the file
            if not is_image_blowout(file_path):
                file.write(filename + '\n')
                print(f'Not blown out image: {filename}')

print(f"List of not blown out images saved to {output_file}")
