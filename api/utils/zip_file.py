import os
from zipfile import ZipFile
from config import settings


def get_all_file_paths(directory):
    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

            # returning all file paths
    return file_paths


def get_zip(zip_name):
    zip_path = settings.ZIP_PATH
    zip_name = zip_name + '.zip'
    filepaths = get_all_file_paths(settings.IMAGES_PATH)
    with ZipFile(zip_path + zip_name, 'w') as zip:
        for file in filepaths:
            zip.write(file)
    return zip_path, zip_name
