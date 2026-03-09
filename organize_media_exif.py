# This script will extract creation dates from media files and move all files
# to a subdirectory by date.  If the creation date isn't available it should
# fall back to the last modification date.
# Ensure you have the current version of Python installed and Python set in PATH
# Install the EXIF module from a command prompt with: pip install exif
# Run from a command prompt from your media directory with: python3 organize_media.py

import os
import shutil
from datetime import datetime
from collections import defaultdict
from exif import Image as ExifImage

# Supported file extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".mts"}
MEDIA_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

def get_exif_date_taken(filepath):
    """
    Extracts EXIF DateTimeOriginal from an image.
    Falls back to file modified date if unavailable.
    """
    try:
        with open(filepath, "rb") as f:
            img = ExifImage(f)
            if img.has_exif and hasattr(img, "datetime_original"):
                date = datetime.strptime(img.datetime_original, "%Y:%m:%d %H:%M:%S")
                return date.strftime("%m_%d_%Y")
    except Exception:
        pass

    # fallback
    return get_modified_date(filepath)

def get_modified_date(filepath):
    timestamp = os.path.getmtime(filepath)
    date = datetime.fromtimestamp(timestamp)
    return date.strftime("%m_%d_%Y")

def generate_unique_filename(destination_path):
    """
    Appends _copy, _copy2, etc. to filename if it already exists
    """
    base, extension = os.path.splitext(destination_path)
    counter = 1
    new_path = destination_path

    while os.path.exists(new_path):
        if counter == 1:
            new_path = f"{base}_copy{extension}"
        else:
            new_path = f"{base}_copy{counter}{extension}"
        counter += 1

    return new_path

def main():
    working_directory = os.getcwd()
    summary = defaultdict(int)

    for filename in os.listdir(working_directory):
        filepath = os.path.join(working_directory, filename)

        if not os.path.isfile(filepath):
            continue

        extension = os.path.splitext(filename)[1].lower()
        if extension not in MEDIA_EXTENSIONS:
            continue

        # Determine date folder
        if extension in IMAGE_EXTENSIONS:
            date_folder = get_exif_date_taken(filepath)
        else:
            # Videos: fallback to file modified date
            date_folder = get_modified_date(filepath)

        destination_folder = os.path.join(working_directory, date_folder)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        destination_path = os.path.join(destination_folder, filename)
        destination_path = generate_unique_filename(destination_path)

        shutil.move(filepath, destination_path)
        summary[date_folder] += 1

    # Summary
    print("\n===== Organization Summary =====")
    total_files = 0
    for folder, count in sorted(summary.items()):
        print(f"{folder}: {count} files moved")
        total_files += count

    print(f"\nTotal files moved: {total_files}")

if __name__ == "__main__":
    main()