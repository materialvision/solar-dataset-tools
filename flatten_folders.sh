#!/bin/bash

# Define the source directory you want to copy files from
SOURCE_DIR="/Volumes/Solardisk/scraper_solar_get_more"

# Define the target directory where you want to collect files
TARGET_DIR="/Volumes/Solardisk/scraper_all_images_flat"

# Create the target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Find and copy all files from the source to the target directory
find "$SOURCE_DIR" -type f -exec cp {} "$TARGET_DIR" \;
