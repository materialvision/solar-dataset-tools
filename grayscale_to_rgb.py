from PIL import Image
import os

def convert_grayscale_to_rgb(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg"):
            file_path = os.path.join(input_folder, filename)
            
            # Open the image
            with Image.open(file_path) as img:
                # Convert the image to RGB
                rgb_img = img.convert("RGB")
                
                # Save the converted image to the output folder with high quality
                output_path = os.path.join(output_folder, filename)
                rgb_img.save(output_path, quality=95, optimize=True, progressive=True)

# Set your input and output folder paths
input_folder = './solar-big-bear-black'
output_folder = './solar-big-bear-color'

convert_grayscale_to_rgb(input_folder, output_folder)
