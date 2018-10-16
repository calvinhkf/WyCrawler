import os

import file_util


def filter_unvalid_json():
    count = 0
    dir_path = "E:/Workspace_PyCharm/wy/Crawler/dependency_library_info"
    file_list = os.listdir(dir_path)
    for json_file in file_list:
        json_data = file_util.read_json(os.path.join(dir_path,json_file))
        version_types_list = json_data['version_types_list']
        if len(version_types_list) == 0:
            count += 1
            print(json_file)
            os.remove(os.path.join(dir_path,json_file))
    print(count)


def remove_crawled_lib_from_list():
    new_list = []
    count = 0
    output_dir = "E:/Workspace_PyCharm/wy/Crawler/dependency_library_info"
    list_path = '10.12.txt'
    json_data = file_util.read_json(list_path)
    print(len(json_data))
    for lib_obj in json_data:
        key = lib_obj['lib_name']
        if os.path.exists(output_dir + "/" + key + ".json"):
            count += 1
        else:
            new_list.append(lib_obj)
    print(count)
    print(len(new_list))
    file_util.write_json('10.12+.txt',new_list)

# filter_unvalid_json()
remove_crawled_lib_from_list()