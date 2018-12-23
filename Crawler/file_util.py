import json
import random

import os
import requests
import subprocess

from useragents import agents

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data

def write_json(path,json_data):
    with open(path, 'w') as file_object:
        json.dump(json_data, file_object)

def save_lib(url,path):
    # headers = {'User-Agent': random.choice(agents)}
    # lib = requests.get(url, headers=headers)
    # with open(path, "wb") as f:
    #     f.write(lib.content)
    # f.close()
    cmd = "curl -o " + path + " " + url
    process = subprocess.Popen(cmd)

def get_lib_name(path):
    return path.split("/")[-1]

def read_file(path):
    with open(path, "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip('\n')
    return lines

def append_file(file_path,content):
    with open(file_path, "a") as f:
        f.write(content + "\n")
    f.close()