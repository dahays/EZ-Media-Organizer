# EZ Media Organizer

EZ Media Organizer is a simple Python utility that helps clean up folders full of photos and videos imported from cameras or phones.

The program can:

1. **Organize media files into folders by date**
2. **Normalize portrait image orientations to landscape display**

It reads **EXIF metadata** from images to determine when a photo was taken and then moves files into date-based folders automatically.

---

# Features

* Organizes photos and videos into folders by date  
* Uses **EXIF DateTimeOriginal** when available  
* Falls back to **file modification date** if metadata is missing  
* Automatically creates date directories in `MM_DD_YYYY` format  
* Prevents filename conflicts by appending `_copy`, `_copy2`, etc.  
* Can reset portrait EXIF orientation to landscape display  
* Provides a summary of actions performed  

Example output directory structure:

media_folder/

│

├── 03_07_2026/

│ ├── IMG_0001.jpg

│ ├── IMG_0002.jpg

│ └── VID_0001.mp4

│

├── 03_08_2026/

│ ├── IMG_0003.jpg

│ └── IMG_0004.jpg

│

└── organize_media.py


---

# Requirements

### Python

Python **3.8 or newer** is recommended.

Verify installation:


python --version


---

### Required Python Library

The program uses the **exif** library to read and modify image metadata.

Install it using pip:


pip install exif


---

# Supported Media Types

### Images

.jpg
.jpeg
.png


### Videos

.mp4
.mov
.avi
.mkv
.mts


Images use **EXIF metadata** to determine the capture date.

Videos typically do not contain accessible EXIF metadata, so the program uses the **file's last modified timestamp** instead.

---

# Usage

1. Copy `organize_media.py` into the folder containing your photos and videos.

Example:


VacationPhotos/

IMG_0001.jpg

IMG_0002.jpg

VID_0001.mp4

organize_media.py


2. Open a terminal or command prompt in that folder.

3. Run the script:


python organize_media.py


---

# Menu Options

When the program runs, you will see a menu:

Welcome to the EZ Media Organizer tool.

1. Organize Media Files by Date

2. Convert Portrait Orientations to Landscape

3. QUIT


### Option 1 — Organize Media Files

Moves all supported media files into date-based folders.

Example:


03_07_2026: 18 files moved

03_08_2026: 22 files moved

Total files moved: 40


---

### Option 2 — Convert Portrait Orientations

Some cameras store portrait photos rotated using an EXIF orientation tag.

This option resets the orientation metadata so the images display correctly as landscape orientation in most viewers.

Example output:


===== Orientation Conversion Summary =====

Images converted: 14

Images skipped: 26


---

### Option 3 — Quit

Exits the program.

---

# Safety Notes

The program **moves files** but does not delete them.

If duplicate filenames exist, the program automatically renames them:

IMG_0001.jpg

IMG_0001_copy.jpg

IMG_0001_copy2.jpg


---

# Recommended Workflow

1. Copy photos from your camera into a folder.
2. Place `organize_media.py` in that folder.
3. Run the script.
4. Choose **Option 1** to organize everything automatically.

---

# License

This project is provided for personal and educational use.

You are free to modify or extend the script as needed.
