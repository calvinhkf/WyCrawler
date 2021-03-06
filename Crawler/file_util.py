import json
import random

import os
import requests
import subprocess
import platform
from useragents import agents

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
def read_json(path):
    try:
        with open(path, encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data
    except Exception as e:
        with open(path, encoding='gbk') as json_file:
            data = json.load(json_file)
            return data


def write_json(path,json_data):
    with open(path, 'w', encoding='utf-8') as file_object:
        json.dump(json_data, file_object)

def write_json_format(path,json_data):
    with open(path, 'w', encoding='utf-8') as file_object:
        json.dump(json_data, file_object, indent=4)

def save_lib(url,path):
    headers = {'User-Agent': random.choice(agents)}
    lib = requests.get(url, headers=headers)
    with open(path, "wb") as f:
        f.write(lib.content)
    f.close()
    # cmd = "wget -O " + path + " " + url
    # pf = platform.system()
    # if pf == "Windows":
    #     process = subprocess.Popen(cmd)
    # else:
    #     process = subprocess.Popen(cmd.split(" "))

def get_lib_name(path):
    return path.split("/")[-1]

def read_file(path):
    try:
        with open(path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].strip('\n')
        return lines
    except Exception as e:
        with open(path, "r", encoding='gbk') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].strip('\n')
        return lines


def append_file(file_path,content):
    with open(file_path, "a", encoding='utf-8') as f:
        f.write(content + "\n")
    f.close()