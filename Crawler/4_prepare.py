import os
import shutil

from file_util import read_json, write_json


def get_proj():
    json_date = read_json("D:/WeChat/WeChat Files/WeChat Files/clewang1026/Files/gradle-projs-id-gt145-17.json")
    count = 0
    for entry in json_date:
        if "flag" not in entry:
            count += 1
            name = entry["name"]
            print(name)
            local_addr = entry["local_addr"].replace("C:/", "").replace("D:/", "")
            shutil.copyfile("F:/projects_last/" + local_addr + ".zip", "F:/projects_last/tocopy/" + name + ".zip")
            if count == 100:
                break
    print(count)


def get_left_proj():
    json_date = read_json("C:/Users/yw/Desktop/gradle-projs.json")
    count = 0
    for entry in json_date:
        name = entry["name"]
        print(name)
        if not os.path.exists("F:/projects_last/tocopy/" + name + ".zip") and not os.path.exists("E:/projects_unzips/" + name + ".zip"):
            count += 1
            local_addr = entry["local_addr"].replace("C:/", "").replace("D:/", "")
            shutil.copyfile("F:/projects_last/" + local_addr + ".zip", "E:/projects_unzips/" + name + ".zip")
    print(count)

# get_proj()
get_left_proj()