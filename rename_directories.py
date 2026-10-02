import os
from datetime import datetime

def main():
    working_directory = os.getcwd()
    renamed = 0
    skipped = 0

    for name in os.listdir(working_directory):
        old_path = os.path.join(working_directory, name)

        # Only process directories
        if not os.path.isdir(old_path):
            continue

        # Skip directories already in YYYY_MM_DD format
        try:
            date = datetime.strptime(name, "%Y_%m_%d")
            if date.strftime("%Y_%m_%d") == name:
                continue
        except ValueError:
            pass

        # Parse the existing MM_DD_YYYY format
        try:
            date = datetime.strptime(name, "%m_%d_%Y")
            if date.strftime("%m_%d_%Y") != name:
                continue
        except ValueError:
            continue

        new_name = date.strftime("%Y_%m_%d")
        new_path = os.path.join(working_directory, new_name)

        # Avoid overwriting an existing directory
        if os.path.exists(new_path):
            print(f"Skipped: {name} -> {new_name} (destination exists)")
            skipped += 1
            continue

        os.rename(old_path, new_path)
        print(f"Renamed: {name} -> {new_name}")
        renamed += 1

    print("\n===== Rename Summary =====")
    print(f"Directories renamed: {renamed}")
    print(f"Directories skipped due to conflicts: {skipped}")

if __name__ == "__main__":
    main()