from PIL import Image, ImageDraw
import os

def add_black_corners_to_folder(input_folder, output_folder, square_size):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each image in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.jpg'):
            image_path = os.path.join(input_folder, filename)

            try:
                # Open the image
                with Image.open(image_path) as img:
                    # Create a drawing context
                    draw = ImageDraw.Draw(img)

                    # Image dimensions
                    width, height = img.size

                    # Coordinates for squares
                    coordinates = [
                        (0, 0, square_size, square_size),  # Top-left corner
                        (width - square_size, 0, width, square_size),  # Top-right corner
                        (0, height - square_size, square_size, height),  # Bottom-left corner
                        (width - square_size, height - square_size, width, height)  # Bottom-right corner
                    ]

                    # Draw the squares
                    for coord in coordinates:
                        draw.rectangle(coord, fill="black")

                    # Save the image in the output folder
                    img.save(os.path.join(output_folder, filename), quality=95)

            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Example usage
add_black_corners_to_folder("/Users/espensommereide/Developer/solar-dataset/solar-big-bear", "/Users/espensommereide/Developer/solar-dataset/solar-big-bear-black", 260)  # Replace with your paths and square size
