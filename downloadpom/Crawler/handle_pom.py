import os
import requests

from bs4 import BeautifulSoup

from file_util import read_json, save_lib
from handle_jar import get_lib_from_list_page

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

def get_pom(groupId, artifactId, version):
    print("groupId: " + str(groupId) + ", artifactId: " + str(artifactId) + ", version: " + str(version))
    downloaded = False
    version_url = "https://mvnrepository.com/artifact/"+groupId+"/"+artifactId+"/"+version
    library_version = requests.get(version_url, headers=headers)
    library_soup = BeautifulSoup(library_version.text, 'lxml');
    results = library_soup.find('div', class_='im')
    if results is None:
        print(downloaded)
        print("can't find 'im' class")
        return
        # raise (CustomizeException("can't find 'im' class"))
    results = results.find_next_sibling(class_='grid')
    information_trs = results.find_all('tr')
    files = None
    view_all_url = None
    for tr in information_trs:
        if 'Files' == tr.th.string:
            entries = tr.td.find_all('a')
            if entries is not None:
                for each in entries:
                    _type = each.get_text().replace('\n', '').split(" ")[0]
                    # print(_type)
                    if _type == 'View':
                        view_all_url = each["href"]
                    if _type == 'pom':
                        pom_url = each["href"]
                        if not os.path.exists("F:/GP/pom/" + groupId+" "+artifactId+" "+version+".pom"):
                            save_lib(pom_url, "F:/GP/pom/" + groupId + " " + artifactId + " " + version + ".pom")
                        downloaded = True
                        break
            break
    if not downloaded and view_all_url is not None:
            downloaded,package_url = get_lib_from_list_page(view_all_url, "pom", None)
    print(downloaded)

def download_unparsed_pom_lib(path):
    data = read_json(path)
    idx = 0
    for pom in data:
        idx+=1
        print(idx)
        groupId= pom["groupId"]
        artifactId = pom["artifactId"]
        if "version" not in  pom:
            print("groupId: " + str(groupId) + ", artifactId: " + str(artifactId) )
            print(False)
            continue
        version = pom["version"]
        get_pom(groupId, artifactId, version)
# get_pom('org.springframework', 'spring-framework-bom', '4.3.7.RELEASE')
download_unparsed_pom_lib("C:/Users/yw/Desktop/pom.txt")