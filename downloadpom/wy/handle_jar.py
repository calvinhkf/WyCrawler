import json

import os
import requests

# import database
# from exception import CustomizeException
from bs4 import BeautifulSoup

from file_util import save_lib2, get_lib_name, read_json, save_lib, read_pom_file
pom_path = "F:/GP/pom/"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

def get_lib_from_list_page(page_path, groupId, artifactId, version, _type,classifier):
    content = None
    success = False
    page = requests.get(page_path, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml');
    list = soup.find_all('a')
    for li in list:
        if li["href"].endswith("." + _type) and "-sources" not in li["href"] and "-javadoc" not in li["href"]:
            url = None
            if classifier is not None:
                if classifier in li["href"]:
                    url = page_path + "/" + li["href"]
            else:
                url = page_path + "/" + li["href"]
            if url is not None:
                # if not os.path.exists("C:/Users/huangkaifeng/Desktop/" + li["href"]):
                    # save_lib(url, "C:/Users/huangkaifeng/Desktop/" + li["href"])
                if not os.path.exists(pom_path + groupId + " " + artifactId + " " + version + ".pom"):
                    content = save_lib(url, pom_path + groupId + " " + artifactId + " " + version + ".pom")
                else:
                    content = read_pom_file(pom_path + groupId + " " + artifactId + " " + version + ".pom")
                success = True
                continue
    return success, content