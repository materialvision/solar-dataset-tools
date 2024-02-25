import os
import argparse
from PIL import Image
import numpy as np
from scipy import signal
from scipy.ndimage import map_coordinates

def load_image(image_path):
    return Image.open(image_path).convert('L')

def create_warp_matrix(image_shape, amplitude, frequency):
    """ Create a warp matrix with sine wave based displacements """
    yy, xx = np.meshgrid(np.arange(image_shape[0]), np.arange(image_shape[1]), indexing='ij')
    warp_matrix_x = amplitude * np.sin(2 * np.pi * frequency * xx / image_shape[1])
    warp_matrix_y = amplitude * np.sin(2 * np.pi * frequency * yy / image_shape[0])
    return np.array([warp_matrix_x, warp_matrix_y])

def warp(image, warp_matrix):
    """ Apply warping using the warp matrix """
    coordinates = np.array(np.meshgrid(np.arange(image.shape[0]), np.arange(image.shape[1]), indexing='ij'))
    coordinates = coordinates + warp_matrix
    coordinates = np.clip(coordinates, 0, np.array(image.shape)[:, None, None] - 1)
    warped_image = map_coordinates(image, coordinates, order=1, mode='reflect')
    return warped_image

def reduce_contrast(image, factor):
    """ Reduce the contrast of the image """
    mid_gray = 90
    adjusted_image = image.astype(np.float32) * factor + mid_gray * (1 - factor)
    return np.clip(adjusted_image, 0, 255)

def apply_effects(image, kernel, amplitude, frequency, contrast_factor, enable_blur, enable_turbulence, enable_contrast):
    image_np = np.array(image)

    if enable_contrast:
        image_np = reduce_contrast(image_np, contrast_factor)

    if enable_blur:
        image_np = signal.convolve(image_np, kernel, mode='same')

    if enable_turbulence:
        warp_matrix = create_warp_matrix(image.size, amplitude, frequency)
        image_np = warp(image_np, warp_matrix)

    return Image.fromarray(image_np.astype(np.uint8))

def resize_and_tile(image, tile_size=256):
    width, height = image.size
    new_width = ((width - 1) // tile_size + 1) * tile_size
    new_height = ((height - 1) // tile_size + 1) * tile_size
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    tiles = []
    for i in range(0, new_width, tile_size):
        for j in range(0, new_height, tile_size):
            tile = resized_image.crop((i, j, i + tile_size, j + tile_size))
            tiles.append(tile)
    return tiles

def convert_to_color(image):
    color_image = Image.merge("RGB", (image, image, image))
    return color_image

def process_folder(args):
    kernel = np.ones((args.kernel_size, args.kernel_size)) / (args.kernel_size ** 2)

    if not os.path.exists(args.dest_folder):
        os.makedirs(args.dest_folder)

    tile_count = 0
    for filename in sorted(os.listdir(args.source_folder)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
            image_path = os.path.join(args.source_folder, filename)
            image = load_image(image_path)

            processed_image = apply_effects(image, kernel, args.amplitude, args.frequency, args.contrast_factor, args.enable_blur, args.enable_turbulence, args.enable_contrast)
            
            if args.tile:
                tiles = resize_and_tile(processed_image)
                for idx, tile in enumerate(tiles):
                    if tile_count >= args.max_tiles:
                        print(f"Generated {tile_count} tiles, stopping as per limit.")
                        return

                    save_path = os.path.join(args.dest_folder, f"{os.path.splitext(filename)[0]}_tile{idx}.jpg")
                    tile_to_save = convert_to_color(tile) if args.colorize else tile
                    tile_to_save.save(save_path, quality=100)
                    tile_count += 1
            else:
                if tile_count >= args.max_tiles:
                    print(f"Generated {tile_count} files, stopping as per limit.")
                    return

                save_path = os.path.join(args.dest_folder, filename)
                processed_image = convert_to_color(processed_image) if args.colorize else processed_image
                processed_image.save(save_path, quality=100)
                tile_count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process images with optional effects.")
    parser.add_argument("source_folder", type=str, help="Source folder path")
    parser.add_argument("dest_folder", type=str, help="Destination folder path")
    parser.add_argument("--kernel_size", type=int, default=5, help="Size of the blur kernel")
    parser.add_argument("--amplitude", type=float, default=2, help="Amplitude for warp matrix")
    parser.add_argument("--frequency", type=float, default=10, help="Frequency for warp matrix")
    parser.add_argument("--contrast_factor", type=float, default=0.5, help="Contrast factor")
    parser.add_argument("--tile", action="store_true", help="Enable tiling of images")
    parser.add_argument("--colorize", action="store_true", help="Convert grayscale to color")
    parser.add_argument("--enable_blur", action="store_true", help="Enable blurring effect")
    parser.add_argument("--enable_turbulence", action="store_true", help="Enable turbulence effect")
    parser.add_argument("--enable_contrast", action="store_true", help="Enable contrast adjustment")
    parser.add_argument("--max_tiles", type=int, default=float('inf'), help="Maximum number of tiles to generate")

    args = parser.parse_args()
    process_folder(args)

#python turbulence_emulation.py /Users/espensommereide/Developer/solar-dataset/solar-big-bear-black /Users/espensommereide/Developer/solar-dataset/solar-tiles2 --kernel_size 5 --amplitude 2 --frequency 10 --contrast_factor 0.5 --tile --colorize --apply_effects --max_tiles 5500
#python turbulence_emulation.py /Users/espensommereide/Developer/solar-dataset/solar-big-bear-black /Users/espensommereide/Developer/solar-dataset/solar-tiles-org2 --tile --colorize --max_tiles 5500
#python turbulence_emulation.py /Users/espensommereide/Developer/solar-dataset/solar-big-bear-black /Users/espensommereide/Developer/solar-dataset/solar-tiles-turb-bw --kernel_size 5 --amplitude 2 --frequency 10 --contrast_factor 0.5 --tile --apply_effects --max_tiles 5500
#python turbulence_emulation.py /Users/espensommereide/Developer/solar-dataset/solar-big-bear-black /Users/espensommereide/Developer/solar-dataset/solar-tiles-org-bw --tile --max_tiles 5500
#python turbulence_emulation.py /Users/espensommereide/Dropbox/Projects/SUN/tiff /Users/espensommereide/Dropbox/Projects/SUN/tifftile --tile --max_tiles 100
#python turbulence_emulation.py /Users/espensommereide/Developer/solar-dataset/solar-big-bear-black /Users/espensommereide/Developer/solar-dataset/solar-big-bear-black-tiles --tile --colorize --max_tiles 5000
#python turbulence_emulation.py /Users/espensommereide/Developer/solar-dataset/solar-big-bear-black /Users/espensommereide/Developer/solar-dataset/solar-big-bear-black-tiles-blur --enable_blur --tile --colorize --max_tiles 5000
#python turbulence_emulation.py /Users/espensommereide/Developer/solar-dataset/solar-big-bear-color-blur /Users/espensommereide/Developer/solar-dataset/solar-big-bear-black-blurx2 --enable_blur
#python turbulence_emulation.py /Users/espensommereide/Developer/solar-dataset/solar-big-bear-black /Users/espensommereide/Developer/solar-dataset/solar-big-bear-black-blur --enable_blur
#python turbulence_emulation.py /Users/espensommereide/Developer/solar-dataset/solar-suntrast-one-tiles /Users/espensommereide/Developer/solar-dataset/solar-suntrast-one-tiles -tile --colorize