import os
import socket

import requests

from bs4 import BeautifulSoup
from urllib3.exceptions import NewConnectionError, MaxRetryError

from file_util import read_json, save_lib2, save_lib, read_pom_file
from handle_jar import get_lib_from_list_page
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

def get_pom(groupId, artifactId, version):
    print("groupId: " + str(groupId) + ", artifactId: " + str(artifactId) + ", version: " + str(version))
    downloaded = False
    version_url = "https://mvnrepository.com/artifact/"+groupId+"/"+artifactId+"/"+version
    print(version_url)
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
    content = None
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
                            content = save_lib(pom_url, "F:/GP/pom/" + groupId + " " + artifactId + " " + version + ".pom")
                        else:
                            content = read_pom_file("F:/GP/pom/" + groupId + " " + artifactId + " " + version + ".pom")
                        # if not os.path.exists("C:/Users/huangkaifeng/Desktop/" + groupId+" "+artifactId+" "+version+".pom"):
                        #     content = save_lib2(pom_url)
                        downloaded = True
                        break
            break

    if not downloaded and view_all_url is not None:
        # print(view_all_url)
        downloaded, content = get_lib_from_list_page(view_all_url, groupId, artifactId, version,"pom", None)
    print(downloaded)
    return content

def get_pom_by_repo_url(repoUrl, groupId, artifactId, version):
    print("groupId: " + str(groupId) + ", artifactId: " + str(artifactId) + ", version: " + str(version))
    downloaded = False
    groupUrl = groupId.replace('.', '/')
    # groupUrl = groupId
    # print(groupUrl)
    pom_url = repoUrl+"/"+groupUrl+"/"+artifactId+"/"+version+"/"+artifactId+"-"+version+".pom"
    if not pom_url.startswith("https://") and not pom_url.startswith("http://"):
        pom_url = "http://" + pom_url

    print(pom_url)
    content = None
    try:
        lib_pom = requests.get(pom_url, headers=headers)
    except Exception as e:
        print(downloaded)
        return content

    if lib_pom is not None and lib_pom.text is not None and lib_pom.text.startswith("<project"):
        if not os.path.exists("F:/GP/pom/" + groupId+" "+artifactId+" "+version+".pom"):
            content = save_lib(pom_url, "F:/GP/pom/" + groupId + " " + artifactId + " " + version + ".pom")
        else:
            content = read_pom_file("F:/GP/pom/" + groupId + " " + artifactId + " " + version + ".pom")
        downloaded = True
    else:
        list_page_url = repoUrl+"/"+groupUrl+"/"+artifactId+"/"+version
        maven_metadata_url = list_page_url + "/" +"maven-metadata.xml"
        try:
            meta_data = requests.get(maven_metadata_url, headers=headers)
            # print(meta_data.text)
            if meta_data is not None:
                meta_data_soup = BeautifulSoup(meta_data.text, 'xml');
                snapshot_versions = meta_data_soup.find_all('snapshotVersion')
                for snapshot_version in snapshot_versions:
                    # print(snapshot_version)
                    # print(snapshot_version.extension.string)
                    type = snapshot_version.extension.string
                    if type == 'pom':
                        version_id = snapshot_version.value.string
                        # print(version_id)
                        pom_url = list_page_url + "/" + artifactId + "-" + version_id + ".pom"
                        # pom_url = list_page_url + "/" + artifactId + "-.pom"
                        print(pom_url)
                        try:
                             lib_pom = requests.get(pom_url, headers=headers)
                        except Exception as e:
                            print(downloaded)
                            return content
                        # print(lib_pom.text)
                        # print("<html>" not in lib_pom.text)
                        if lib_pom is not None and lib_pom.text is not None and "<html>" not in lib_pom.text:
                            if not os.path.exists("F:/GP/pom/" + groupId + " " + artifactId + " " + version + ".pom"):
                                content = save_lib(pom_url,
                                                   "F:/GP/pom/" + groupId + " " + artifactId + " " + version + ".pom")
                            else:
                                content = read_pom_file(
                                    "F:/GP/pom/" + groupId + " " + artifactId + " " + version + ".pom")
                            downloaded = True
                        break
        except Exception as e:
            meta_data = None

    print(downloaded)
    return content

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
# download_unparsed_pom_lib("C:/Users/yw/Desktop/pom.txt")

# get_pom_by_repo_url(
#     "https://artifacts-oss.talend.com/nexus/content/repositories/TalendOpenSourceRelease/org.talend.components/components-parent/0.19.9/components-parent-0.19.9.pom", "org.talend.components", "components-parent", "0.19.9")

# content = get_pom_by_repo_url(
#     "https://github.com/jitsi/jitsi-maven-repository/raw/master/snapshots", "org.jitsi", "jitsi-universe", "1.0-20170425.182805-23")
# print(content)
# content = save_lib("https://raw.githubusercontent.com/jitsi/jitsi-maven-repository/master/snapshots/org/jitsi/jitsi-universe/1.0-SNAPSHOT/jitsi-universe-1.0-20160405.235512-16.pom",
#                    "F:/GP/pom/org.jitsi jitsi-universe 1.0-20160405.235512-16.pom")
# print(content)


# get_pom("org.springframework.boot", "spring-boot-starter-parent", "1.1.0.RC1")