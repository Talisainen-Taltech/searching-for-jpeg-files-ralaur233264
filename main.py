import os
import requests
import zipfile
import shutil

# Author and version info
__author__ = "Ramses Laursoo"
__version__ = "1.0.0"

# ZIP file and folder info
zip_url = "https://upload.itcollege.ee/~aleksei/random_files_without_extension.zip" 
zip_path = "random_files.zip"
extracted_folder = "random_files"

# Download ZIP file
response = requests.get(zip_url, stream=True)
with open(zip_path, 'wb') as file:
    for chunk in response.iter_content(chunk_size=128):
        file.write(chunk)

# Extract ZIP file
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)

# Remove nested folders
extracted_contents = os.listdir(extracted_folder)
if len(extracted_contents) == 1 and os.path.isdir(os.path.join(extracted_folder, extracted_contents[0])):
    nested_folder = os.path.join(extracted_folder, extracted_contents[0])

    # Move nested files to parent folder
    for filename in os.listdir(nested_folder):
        shutil.move(os.path.join(nested_folder, filename), extracted_folder)
    os.rmdir(nested_folder)

# Find jpg files without jpg extension
jpg_files = 0
removed_files = 0
for filename in os.listdir(extracted_folder):
    file_path = os.path.join(extracted_folder, filename)

    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            header = file.read(2)
        
        if header == b'\xFF\xD8':
            jpg_files += 1
            print(f"Found JPG file without JPG extension: {filename}")
        else:
            removed_files += 1
#            ´print(f"Removed non-JPG file: {filename}")
            os.remove(file_path)

print(f"Total number of JPG files found: {jpg_files}")
print(f"Total number of removed files: {removed_files}")

# Remove ZIP file
os.remove(zip_path)
