# This script will extract creation dates from media files and move all files
# to a subdirectory by date. If the creation date isn't available it should
# fall back to the last modification date.
#
# Ensure you have Python installed and Python set in PATH
# Install the EXIF module from a command prompt with:
# pip install exif
#
# Run from a command prompt in your media directory with:
# python organize_media.py

import os
import shutil
from datetime import datetime
from collections import defaultdict
from exif import Image as ExifImage

# Supported file extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".mts"}
MEDIA_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

# Named constants for menu choices
ORGANIZE = 1
ORIENT = 2
QUIT = 3

def menu():
    """
    Displays menu and returns a valid user choice.
    """
    while True:

        print("\nWelcome to the EZ Media Organizer tool.")
        print("Please choose from the following menu options.")
        print("----------------------------------------------")
        print("1. Organize Media Files by Date")
        print("2. Convert Portrait Orientations to Landscape")
        print("3. QUIT")

        choice = input("Enter a choice from the menu: ")

        try:
            choice = int(choice)

            if ORGANIZE <= choice <= QUIT:
                return choice
            else:
                print(f"Please enter a number between {ORGANIZE} and {QUIT}.")

        except ValueError:
            print("Invalid input. Please enter a number.")

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

    return get_modified_date(filepath)

def get_modified_date(filepath):
    """
    Returns the last modified date of a file.
    """
    timestamp = os.path.getmtime(filepath)
    date = datetime.fromtimestamp(timestamp)
    return date.strftime("%m_%d_%Y")

def generate_unique_filename(destination_path):
    """
    Appends _copy, _copy2, etc. if a filename already exists.
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

def convert_portrait_to_landscape():
    """
    Converts portrait-oriented images to landscape by resetting
    the EXIF orientation tag to 1 (normal).
    """
    working_directory = os.getcwd()
    converted = 0
    skipped = 0

    for filename in os.listdir(working_directory):
        filepath = os.path.join(working_directory, filename)
        if not os.path.isfile(filepath):
            continue
        extension = os.path.splitext(filename)[1].lower()

        if extension not in IMAGE_EXTENSIONS:
            continue
        try:

            with open(filepath, "rb") as img_file:
                img = ExifImage(img_file)
            if not img.has_exif:
                skipped += 1
                continue
            if hasattr(img, "orientation"):
                if img.orientation in [3, 6, 8]:
                    img.orientation = 1
                    with open(filepath, "wb") as new_file:
                        new_file.write(img.get_file())
                    converted += 1
                else:
                    skipped += 1
            else:
                skipped += 1

        except Exception:
            skipped += 1

    print("\n===== Orientation Conversion Summary =====")
    print(f"Images converted: {converted}")
    print(f"Images skipped: {skipped}")


def organize_media():
    """
    Organizes media files into folders by date.
    """
    working_directory = os.getcwd()
    summary = defaultdict(int)

    for filename in os.listdir(working_directory):
        filepath = os.path.join(working_directory, filename)
        if not os.path.isfile(filepath):
            continue

        extension = os.path.splitext(filename)[1].lower()
        if extension not in MEDIA_EXTENSIONS:
            continue

        # Determine folder date
        if extension in IMAGE_EXTENSIONS:
            date_folder = get_exif_date_taken(filepath)
        else:
            date_folder = get_modified_date(filepath)

        destination_folder = os.path.join(working_directory, date_folder)

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        destination_path = os.path.join(destination_folder, filename)
        destination_path = generate_unique_filename(destination_path)
        shutil.move(filepath, destination_path)
        summary[date_folder] += 1

    print("\n===== Organization Summary =====")
    total_files = 0

    for folder, count in sorted(summary.items()):
        print(f"{folder}: {count} files moved")
        total_files += count
    print(f"\nTotal files moved: {total_files}")

def main():
    """
    Process the menu choice
    """
    while True:
        choice = menu()
        if choice == ORGANIZE:
            organize_media()

        elif choice == ORIENT:
            convert_portrait_to_landscape()

        elif choice == QUIT:
            print("\nThank you for using EZ Media Organizer.")
            break

# Main guard
if __name__ == "__main__":
    main()