from PIL import Image
import os

def convert_png_to_jpg(source_folder, target_folder, quality=95):
    """
    Convert all PNG images in the source folder to high-quality JPG images in the target folder.
    Handles grayscale images and images with 16-bit depth correctly.

    Parameters:
    - source_folder: The folder containing the source PNG images.
    - target_folder: The folder where the converted JPG images will be saved.
    - quality: The quality of the JPG images, ranging from 1 (worst) to 95 (best). Default is 95.
    """
    # Ensure target folder exists
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Process each file in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith('.png'):
            # Open the image
            with Image.open(os.path.join(source_folder, filename)) as img:
                # If the image has an alpha channel, remove it by pasting onto a white background
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else img.getchannel('A'))
                    img = background
                elif img.mode == 'P':
                    # Convert paletted images to RGB
                    img = img.convert('RGB')

                # Convert 16-bit images to 8-bit
                if img.mode in ('I', 'I;16'):
                    img = img.point(lambda i: i*(1/256)).convert('L')

                # Define the target filename and path
                target_file = os.path.splitext(filename)[0] + '.jpg'
                target_path = os.path.join(target_folder, target_file)

                # Save the image as JPG with the specified quality
                img.save(target_path, 'JPEG', quality=quality)

    print(f'All PNG images from {source_folder} have been converted to high-quality JPG images in {target_folder}.')

# Example usage
source_folder = '/Volumes/Solardisk/sunplanet/010224-over-ekeberg/timelapse-overekeberg/SF_crop_contrast_train'
target_folder = '/Volumes/Solardisk/sunplanet/010224-over-ekeberg/timelapse-overekeberg/trainA'
convert_png_to_jpg(source_folder, target_folder)
