import os
import argparse
import shutil
from datetime import datetime
from itertools import zip_longest, combinations

#1. log.txt
def write_log(message, log_file="log.txt"):
    time = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"{time} {message}\n")

#2. Delete empty files
def delete_empty_file(folder_path):
    for root, _, files in os.walk(folder_path): 
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) == 0:
                os.remove(file_path)
                msg = f"{file} is removed (empty)"
                print(msg)
                write_log(msg)

#3. Check if two files are identical
def are_files_identical(file1, file2):
    with open(file1, 'r', encoding='utf-8', errors='ignore') as f1, open(file2, 'r', encoding='utf-8', errors='ignore') as f2:
        for l1, l2 in zip_longest(f1, f2): 
            if l1 != l2:
                return False
        return True

#4. Delete duplicate files
def check_delete_similar(folder_path):
    for root, _, files in os.walk(folder_path):
        full_paths = [os.path.join(root, f) for f in files]
        for file1, file2 in combinations(full_paths, 2):
            if are_files_identical(file1, file2):
                os.remove(file2)
                msg = f"{os.path.basename(file2)} is removed (duplicate of {os.path.basename(file1)})"
                print(msg)
                write_log(msg)

#5. Extensions mapping
EXTENSIONS_MAP = {
    'Documents': ['.pdf', '.docx', '.txt'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Videos': ['.mp4', '.mov', '.avi'],
    'Music': ['.mp3', '.wav'],
    'Archives': ['.zip', '.rar', '.tar'],
    'Scripts': ['.py', '.js', '.sh', '.bat'],
}

#6. Classify a file
def classify_file(filename):
    _, ext = os.path.splitext(filename.lower())
    for folder, extensions in EXTENSIONS_MAP.items():
        if ext in extensions:
            return folder
    return 'Others'

#7. Parse arguments (get the folder path)
def get_arguments():
    parser = argparse.ArgumentParser(description="Organize and clean a folder automatically.")
    parser.add_argument('--path', type=str, required=True, help="Path of the folder to clean.")
    args = parser.parse_args()
    return args.path

#8. Organize folder by moving files into categorized folders
def organize_folder(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            category = classify_file(item)
            new_folder = os.path.join(folder_path, category)

            os.makedirs(new_folder, exist_ok=True)

            try:
                shutil.move(item_path, os.path.join(new_folder, item))
                msg = f"{item} moved to {category}/"
                print(msg)
                write_log(msg)
            except Exception as e:
                error_msg = f"Error while moving {item}: {e}"
                print(error_msg)
                write_log(error_msg)

# 9. Main function
def main():
    folder_path = get_arguments()

    if not os.path.exists(folder_path):
        print("The specified path does not exist. Please check.")
        return

    print(f"Selected folder: {folder_path}")
    organize_folder(folder_path)
    delete_empty_file(folder_path)
    check_delete_similar(folder_path)

#10. Entry point
if __name__ == "__main__":
    main()
