import json

import requests

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data

def save_lib(url,path):
    lib = requests.get(url, headers=headers)
    with open(path, "wb") as f:
        f.write(lib.content)
    return lib.content

def save_lib2(url):
    lib = requests.get(url, headers=headers)
    return lib.content

def get_lib_name(path):
    return path.split("/")[-1]

def read_pom_file(path):
    with open(path, 'rb') as f:
        return f.read()
        # return f.read().encode(encoding="utf-8")