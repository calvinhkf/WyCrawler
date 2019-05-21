import json
import os
import random
import time
import sys

import requests
from bs4 import BeautifulSoup

import database
from crawl_library import get_lib_from_list_page
from exception import CustomizeException
from file_util import get_lib_name, save_lib, write_json, read_json
from useragents import agents

url = "https://mvnrepository.com"
res = requests.get(url)
cookies = dict(res.cookies.items())

# num1 = int(sys.argv[1])
# num2 = int(sys.argv[2])
# root = sys.argv[3]

string_list = "97:98:99:123:124:140:147:148:162:181:184:276:277:280:281:282:286:287:289:295:308:320:442:449:452:454:457:458:459:462:463:464:465:471:543:546:553:565:625:636:677:678:679:680:681:683:684:687:688:696:699:802:803:810:829:830:843:844:940:986:8:11:96:234:431:499:540:542:761"
root = sys.argv[1]

lib_dir = root + "/lib/"
lib_json_dir = root + "/lib_json/"
lib_ver_json_dir = root + "/lib_version_json/"

if not os.path.exists(lib_dir):
    os.mkdir(lib_dir)
if not os.path.exists(lib_json_dir):
    os.mkdir(lib_json_dir)
if not os.path.exists(lib_ver_json_dir):
    os.mkdir(lib_ver_json_dir)

def get_info_from_maven_repo(groupId, artifactId, versions):
    if os.path.exists(lib_json_dir + groupId + "__fdse__" + artifactId + ".txt"):
        return
    result_dic = {}
    time.sleep(random.randint(10, 30))
    headers = {'User-Agent': random.choice(agents),'Referer': 'https://mvnrepository.com/'}
    library = requests.get("https://mvnrepository.com/artifact/" + groupId + "/" + artifactId, headers=headers, verify=False, cookies=cookies)
    if library.status_code == 403:
        print("Exception status 403:" + "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId)
        os._exit(0)
    library_soup = BeautifulSoup(library.text, 'lxml')
    test_tab = library_soup.find('ul', class_='tabs')
    if test_tab is None:
        write_json(lib_json_dir + groupId + "__fdse__" + artifactId + ".txt", result_dic)
        return
    results = test_tab.find_all('li')
    if results is None:
        write_json(lib_json_dir + groupId + "__fdse__" + artifactId + ".txt", result_dic)
        return
    for tab in results:
        temp, over = get_all_versions_from_maven_repo("https://mvnrepository.com" + tab.a["href"],
                                                   "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId,
                                                   groupId, artifactId, versions)
        result_dic[tab.a["href"]] = temp
        if over:
            break
    write_json(lib_json_dir + groupId + "__fdse__" + artifactId + ".txt", result_dic)

def get_all_versions_from_maven_repo(tab_url, category_url, groupId, artifactId, versions):
    library_versions_list = []
    time.sleep(random.randint(10, 30)) #
    headers = {'User-Agent': random.choice(agents),'Referer': 'https://mvnrepository.com/artifact/' + groupId + '/' + artifactId}
    print('------------------------- tab_url:' + tab_url)
    library_tab = requests.get(tab_url, headers=headers, verify=False, cookies=cookies)
    if library_tab.status_code == 403:
        print("Exception status 403:" + tab_url)
        if tab_url.startswith("https://mvnrepository.com"):
            os._exit(0)
    library_soup = BeautifulSoup(library_tab.text, 'lxml')
    results = library_soup.find(class_='grid versions')
    version_idx, repository_idx, usages_idx, date_idx = -1, -1, -1, -1
    ths = results.thead.find_all('th')
    for i in range(0, len(ths)):
        if 'Version' == ths[i].string:
            version_idx = i
        if 'Repository' == ths[i].string:
            repository_idx = i
        if 'Usages' == ths[i].string:
            usages_idx = i
        if 'Date' == ths[i].string:
            date_idx = i
    if (version_idx == -1 or repository_idx == -1 or usages_idx == -1 or date_idx == -1):
        raise (CustomizeException("tab_url:"+str(tab_url)+"\n groupId:"+str(groupId)+"artifactId:"+str(artifactId)+"\nVersion Repository Usages Date imcomplete"))
    tbodys = results.find_all('tbody')
    # bi = 0
    for body in tbodys:
        # bi = bi + 1
        # if bi < 21:
        #     continue
        trs = body.find_all('tr')
        # tri = 0
        for tr in trs:
            # tri = tri + 1
            # if bi == 21 and tri < 29:
            # # if tri < 6:
            #     continue
            tds = tr.find_all('td')
            tr_version = version_idx
            tr_repository = repository_idx
            tr_usages = usages_idx
            tr_date = date_idx
            if (ths[0].string is None):
                if (tds[0].a is not None):
                    tr_version = tr_version - 1
                    tr_repository = tr_repository - 1
                    tr_usages = tr_usages - 1
                    tr_date = tr_date - 1
            test_version = tds[tr_version].a.string.replace('\n', '')
            if os.path.exists(lib_ver_json_dir + groupId + "__fdse__" + artifactId + "__fdse__" + test_version + ".txt"):
                continue
            version_url = category_url[0:category_url.rindex('/')] + '/' + tds[tr_version].a["href"]
            repository = "https://mvnrepository.com" + tds[tr_repository].a["href"]
            usages = None
            if tds[tr_usages].a is None:
                usages = "{'" + tds[tr_usages].get_text().replace('\n', '') + "':''}"
            else:
                usages = "{'" + tds[tr_usages].a.string.replace('\n', '') + "':'" + category_url + tds[tr_usages].a[
                    "href"] + "'}"
            time.sleep(random.randint(10, 30)) #
            headers = {'User-Agent': random.choice(agents),'Referer': tab_url}
            library_version = requests.get(version_url, headers=headers, verify=False, cookies=cookies)
            if library_version.status_code == 403:
                print("Exception status 403:" + version_url)
                if version_url.startswith("https://mvnrepository.com"):
                    os._exit(0)
            page = library_version.text
            library_soup = BeautifulSoup(library_version.text, 'lxml');
            results = library_soup.find('div', class_='im')
            if results is None:
                raise (CustomizeException("tab_url:"+str(tab_url)+"\n groupId:"+str(groupId)+"artifactId:"+str(artifactId)+"\ncan't find 'im' class"))
            results = results.find_next_sibling(class_='grid')
            information_trs = results.find_all('tr')
            license, categories, organization, home_page, files, used_by = None, None, None, None, None, None
            for tr in information_trs:
                if 'License' == tr.th.string:
                    license = ''
                    spans = tr.td.find_all('span')
                    for span in spans:
                        license = license + span.string + ','
                    if license[len(license) - 1] == ',':
                        license = license[:-1].replace('\n', '')
                if 'Categories' == tr.th.string:
                    categories = "{\"" + tr.td.a.string.replace('\n', '') + "\":\"" + "https://mvnrepository.com" + \
                                 tr.td.a[
                                     "href"] + "\"}"
                if 'Organization' == tr.th.string:
                    if tr.td.a is None:
                        organization = "{\"" + tr.td.string.replace('\n', '') + "\":\"\"}"
                    else:
                        organization = "{\"" + tr.td.a.string.replace('\n', '') + "\":\"" + tr.td.a["href"] + "\"}"
                if 'HomePage' == tr.th.string:
                    if tr.td.a is None:
                        home_page = tr.td.string.replace('\n', '')
                    else:
                        home_page = tr.td.a["href"]
                if 'Date' == tr.th.string:
                    _date = tr.td.string
                if 'Files' == tr.th.string:
                    entries = tr.td.find_all('a')
                    if entries is not None:
                        files = "{"
                        for each in entries:
                            file_type = each.get_text().replace('\n', '').split(' ')[0]
                            files = files + "\"" + file_type + "\":\"" + each["href"] + "\","
                        if files[len(files) - 1] == ",":
                            files = files[:-1]
                        files = files + "}"
                if 'Used By' == tr.th.string:
                    used_by = "{\"" + tr.td.a.string.replace('\n', '') + "\":\"" + "https://mvnrepository.com" + tr.td.a[
                        "href"] + "\"}"
            print('    repository:' + str(repository))
            print('    date:' + str(_date))

            declarations = library_soup.find('div', id='snippets')
            if declarations is not None:
                declarations = str(declarations)
            declarations_soup = BeautifulSoup(str(declarations), 'lxml');
            maven = declarations_soup.find(id='maven-a').string
            declarations_soup = BeautifulSoup(maven, 'xml');
            group = declarations_soup.find('groupId').string
            name1 = declarations_soup.find('artifactId').string
            version1 = declarations_soup.find('version').string
            if os.path.exists(lib_ver_json_dir + groupId + "__fdse__" + artifactId + "__fdse__" + version1 + ".txt"):
                continue
            print('    version:' + str(version1))
            jar_name = save_lib_package(files, "jar", None, version1)
            library_version_dic = {}
            library_version_dic["group"] = group
            library_version_dic["name"] = name1
            library_version_dic["version"] = version1
            library_version_dic["usages"] = usages
            library_version_dic["repository"] = repository
            library_version_dic["date"] = _date
            library_version_dic["jar_name"] = jar_name

            library_version_dic["license"] = license
            library_version_dic["categories"] = categories
            library_version_dic["organization"] = organization
            library_version_dic["home_page"] = home_page
            library_version_dic["files"] = files
            library_version_dic["used_by"] = used_by
            write_json(lib_ver_json_dir + groupId + "__fdse__" + artifactId + "__fdse__" + version1 + ".txt", library_version_dic)
            library_versions_list.append(library_version_dic)
            if version1 in versions:
                versions.remove(version1)
                if len(versions) == 0:
                    return library_versions_list, True
    return library_versions_list, False


def save_lib_package(files, _type, classifier,version):
    file_list = json.loads(files)
    if _type in file_list:
        jar_url = file_list[_type]
        if not os.path.exists(lib_dir + get_lib_name(jar_url)):
            save_lib(jar_url, lib_dir + get_lib_name(jar_url))
        return get_lib_name(jar_url)
    if _type == "tar.gz" or _type == "zip" or _type == "jar" or _type == "test-jar" or _type == "nbm-file" or _type == "xml" or _type == "war" or _type == "kar" or _type == "swc" or _type == "pom" or _type == "executable-war":
        new_type = _type
        if _type == "nbm-file":
            new_type = "nbm"
        if _type == "executable-war":
            new_type = "war"
        if 'View' in file_list:
            page_url = file_list['View']
            success, package_url = get_lib_from_list_page(page_url, new_type, classifier)
            if success:
                return get_lib_name(package_url)
    else:
        # print("!!!!!!!!!!!!!!!!!!!! unhandled type: " + str(_type))
        raise (CustomizeException("version:"+str(version)+"classifier:"+str(classifier)+"type:"+str(_type)+"\n!!!!!!!!!!!!!!!!!!!! unhandled type: " + str(_type)))

def crawl_top50(path):
    json_data = read_json(path)
    for entry in json_data:
        key_array = entry[0].split("__fdse__")
        groupId = key_array[0]
        artifactId = key_array[1]
        print("++++++++++++++++++ " + groupId + "  " + artifactId)
        get_info_from_maven_repo(groupId, artifactId)

def crawl_mv(path, num1, num2):
    json_data = read_json(path)
    for i in range(num1, num2):
        obj = json_data[i]
        key = obj["lib"]
        key_array = key.split("__fdse__")
        groupId = key_array[0]
        artifactId = key_array[1]
        versions = obj["versions"]
        if len(versions) == 0:
            versions.append("version")
        print("++++++++++++++++++ " + str(i) + " : " + groupId + "  " + artifactId)
        get_info_from_maven_repo(groupId, artifactId, versions)

def get_version_for_top100():
    db = database.connectdb()
    json_data = read_json("E:/data/top100.txt")
    result = []
    for entry in json_data:
        lib = entry[0]
        groupId = lib.split("__fdse__")[0]
        artifactId = lib.split("__fdse__")[1]
        sql = "SELECT version FROM library_versions WHERE group_str = '" + groupId + "' and name_str = '" + artifactId + "' and repository = 'http://central.maven.org/maven2' ORDER BY parsed_date desc"
        query_result = database.querydb(db, sql)
        version = query_result[0][0]
        value = groupId + "__fdse__" + artifactId + "__fdse__" + version
        print(value)
        result.append(value)
    write_json("E:/data/top100_version.txt", result)


def crawl_mv2(path, string_list):
    string_list = string_list.split(':')

    json_data = read_json(path)
    for ele in string_list:
        i = ele.strip(' ')
        i = int(i)

        obj = json_data[i]
        key = obj["lib"]
        key_array = key.split("__fdse__")
        groupId = key_array[0]
        artifactId = key_array[1]
        versions = obj["versions"]
        if len(versions) == 0:
            versions.append("version")
        print("++++++++++++++++++ " + str(i) + " : " + groupId + "  " + artifactId)
        get_info_from_maven_repo(groupId, artifactId, versions)


crawl_mv2("mv_libs.txt", string_list)
# crawl_top50("E:/data/top51-100.txt")
# print(num1)
# print(num2)
# crawl_mv("mv_libs.txt", num1, num2)
# get_info_from_maven_repo("com.amazonaws", "aws-java-sdk-bundle", ["1.11.271", "1.11.134", "1.11.172", "1.11.199", "1.11.106"])
# get_info_from_maven_repo("com.google.http-client", "google-http-client", ["1.22.0", "1.20.0", "1.23.0"])
# get_info_from_maven_repo("org.apache.hadoop", "hadoop-hdfs", ["0.22.0", "3.1.0", "2.4.0", "2.7.4", "2.7.3", "2.6.0-cdh5.7.0", "2.4.1", "2.2.0", "2.6.0-cdh5.4.2", "2.6.0-cdh5.10.0", "2.3.0-cdh5.1.3", "2.7.3.2.6.1.0-129", "2.0.0-alpha", "2.3.0", "2.6.0", "2.0.0-cdh4.4.0", "2.6.2", "3.0.0", "2.5.2", "2.6.5", "2.5.1", "2.6.1", "2.8.3", "2.7.5", "0.23.3", "2.8.1", "2.7.1", "3.0.0-beta1", "2.3.0-cdh5.1.5", "2.6.0-cdh5.7.4", "2.7.2", "2.5.0", "2.9.0"])
# get_version_for_top100()
# get_info_from_maven_repo("com.android.support", "appcompat-v7", ["28.0.0"])
