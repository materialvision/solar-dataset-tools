# Path to your existing file containing the list of filenames
input_file_path = '/Volumes/Solardisk/scraper_all_images_flat/boul-60-70/not_blown_out_images.txt'

# Path to the new file that will be created, with "file" prefixed
output_file_path = '/Volumes/Solardisk/scraper_all_images_flat/boul-60-70/not_blown_out_images-ffmpeg.txt'

# Open the existing file to read and the new file to write
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
    for line in input_file:
        # Strip newline characters from the end of the line, then format with "file" directive
        formatted_line = f"file '{line.strip()}'\n"
        # Write the formatted line to the new file
        output_file.write(formatted_line)

print(f"Formatted filenames have been saved to {output_file_path}")
