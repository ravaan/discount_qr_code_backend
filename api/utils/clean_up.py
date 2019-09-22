import os
import shutil

from config import settings


def clean_up():
    directory_list = [settings.IMAGES_PATH, settings.ZIP_PATH]
    for directory in directory_list:
        for the_file in os.listdir(directory):
            file_path = os.path.join(directory, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)
