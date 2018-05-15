import json

import os
import requests

import database
from exception import CustomizeException
from bs4 import BeautifulSoup

from file_util import save_lib
from handle_jar import get_lib_from_list_page

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
db = database.connectdb()

def read_used_library():
    for i in range(1, 975):
        sql = "SELECT * FROM library_usage WHERE id = " + str(i)
        results = database.querydb(db, sql)
        print('+++++++++++++++++++++++++++++++++++' + str(i) + ': ' + results[0][3] + " " + results[0][4] + " " + results[0][5])
        version_id = results[0][1]
        sql = "SELECT * FROM library_versions WHERE id = " + str(version_id)
        version_info = database.querydb(db, sql)
        print(version_info[0][5])
        # print(json.loads(version_info[0][12].replace("'", "\""))['View All'])
        lib_url = json.loads(version_info[0][12].replace("'", "\""))['View All']
        print(lib_url)
        page = requests.get(lib_url, headers=headers)
        soup = BeautifulSoup(page.text, 'lxml');
        list = soup.find('pre').find_all('a')
        for li in list:
            if li["href"].endswith(".jar") and "-sources" in li["href"]:
                print(li["href"])
                jar = requests.get(lib_url+"/"+li["href"], headers=headers)
                with open("F:/GP/lib/"+li["href"], "wb") as f:
                    f.write(jar.content)
                f.close()
        print()

def download_lib(groupId, artifactId, version,_type,classifier):
    print("groupId: " + str(groupId) + ", artifactId: " + str(artifactId) + ", version: " + str(version) + ", type: " + str(_type) + ", classifier: " + str(classifier))
    version_url = "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId + "/" + version
    library_version = requests.get(version_url, headers=headers)
    library_soup = BeautifulSoup(library_version.text, 'lxml');
    results = library_soup.find('div', class_='im')
    if results is None:
        raise (CustomizeException("can't find 'im' class"))
    results = results.find_next_sibling(class_='grid')
    information_trs = results.find_all('tr')
    downloaded = False
    view_all_url = None
    for tr in information_trs:
        if 'Files' == tr.th.string:
            entries = tr.td.find_all('a')
            if entries is not None:
                for each in entries:
                    curr_type = each.get_text().replace('\n', '').split(" ")[0]
                    if curr_type == 'View':
                        view_all_url = each["href"]
                    if _type is None:
                        if curr_type == 'jar':
                            jar_url = each["href"]
                            if not os.path.exists("F:/GP/lib/" + get_lib_name(jar_url)):
                                save_lib(jar_url, "F:/GP/lib/" + get_lib_name(jar_url))
                            downloaded = True
                            break
                    elif _type == "tar.gz" or _type == "zip":
                        if curr_type == 'View':
                            if get_lib_from_list_page(each["href"], _type, classifier):
                                downloaded = True
                                break
                    elif _type == "test":
                        continue
            break
    if not downloaded:
        if _type is None and view_all_url is not None:
            downloaded,package_url = get_lib_from_list_page(view_all_url, "jar", classifier)
    print(downloaded)
