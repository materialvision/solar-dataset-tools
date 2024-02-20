import os
import argparse
from PIL import Image

def is_image_file(filename):
    """Check if a file is an image based on its extension."""
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)

def pair_images(folder_a, folder_b, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the list of image filenames in both folders, filtering non-image files
    images_a = sorted(filter(is_image_file, os.listdir(folder_a)))
    images_b = sorted(filter(is_image_file, os.listdir(folder_b)))

    # Check if both folders have the same number of images
    if len(images_a) != len(images_b):
        print("The folders contain a different number of images. Please check your folders.")
        return

    # Pair images side by side
    for img_a_name, img_b_name in zip(images_a, images_b):
        path_a = os.path.join(folder_a, img_a_name)
        path_b = os.path.join(folder_b, img_b_name)

        try:
            with Image.open(path_a) as img_a, Image.open(path_b) as img_b:
                # Create a new image with double the width of the originals (assuming they are the same size)
                dst = Image.new('RGB', (img_a.width + img_b.width, img_a.height))
                dst.paste(img_a, (0, 0))
                dst.paste(img_b, (img_a.width, 0))

                # Save the paired image to the output folder
                output_path = os.path.join(output_folder, f"paired_{img_a_name}")
                dst.save(output_path, "JPEG", quality=95)  # Adjust quality as needed, max is 95 for JPEG
        except Exception as e:
            print(f"Error processing {img_a_name} and {img_b_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Pair images from two folders side by side into a third folder.")
    parser.add_argument('folder_a', type=str, help="Path to folder A")
    parser.add_argument('folder_b', type=str, help="Path to folder B")
    parser.add_argument('output_folder', type=str, help="Path to the output folder")

    args = parser.parse_args()

    pair_images(args.folder_a, args.folder_b, args.output_folder)

if __name__ == "__main__":
    main()

#python pair_images.py /Users/espensommereide/Developer/solar-dataset/solar-big-bear-black-tiles /Users/espensommereide/Developer/solar-dataset/solar-big-bear-black-tiles-blur /Users/espensommereide/Developer/solar-dataset/big-solar-pairs
#python pair_images.py /Users/espensommereide/Dropbox/Projects/SUN/tifftile /Users/espensommereide/Dropbox/Projects/SUN/tifftile /Users/espensommereide/Dropbox/Projects/SUN/pairtest