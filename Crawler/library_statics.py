import os

def same_time_of_different_versions(dir_path):
    file_list = os.listdir(dir_path)
    for file in file_list:
        path = os.path.join(dir_path, file)
