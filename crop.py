from PIL import Image
import os

def crop_center(image_path, output_path, new_width=1835, new_height=1835):
    with Image.open(image_path) as img:
        width, height = img.size

        # Calculate the left, top, right, and bottom coordinates for the crop
        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2

        # Crop the center of the image
        img_cropped = img.crop((left, top, right, bottom))
        img_cropped.save(output_path)

def crop_images_in_folder(input_folder, output_folder, new_width=1835, new_height=1835):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        print(filename)
        # Check for image files (You can add or modify the extension based on your needs)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', 'tiff', 'tif')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            try:
                crop_center(input_path, output_path, new_width, new_height)
                print(f"Cropped image saved to {output_path}")
            except Exception as e:
                print(f"Error processing {input_path}: {e}")

# Example usage
input_folder = '/Volumes/Solardisk/sunplanet/040124-lowdisc/timelapse5sec200/pss'  # Change this to your input folder path
output_folder = '/Volumes/Solardisk/sunplanet/040124-lowdisc/timelapse5sec200/pss-crop'  # Change this to your output folder path
crop_images_in_folder(input_folder, output_folder)
