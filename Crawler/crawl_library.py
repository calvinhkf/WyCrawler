import json
import os
import random

import requests
import time

from bs4 import BeautifulSoup
from exception import CustomizeException
from file_util import read_json, write_json, read_file, get_lib_name, save_lib
from useragents import agents
import sys
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

ttype = sys.argv[1]
if ttype == "a":
    output_dir = "E:/data/dependency_library_info"
    lib_dir = "F:/GP/lib/"
elif ttype == "c":
    output_dir = "E:/data/dependency_library_info"
    lib_dir = "E:/data/lib/"
else:
    output_dir = os.getcwd()+'/dependency_library_info'
    lib_dir = os.getcwd()+'/lib/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(lib_dir):
        os.makedirs(lib_dir)

crawled_repo = []
repo_array = []

library_versions_list = []
version_types_list = []
unsolved_lib_list = []

curr_project_id = -1

def save_lib_package(files, _type, classifier,version):
    version_type_dic = {}
    file_list = json.loads(files)
    if _type in file_list:
        jar_url = file_list[_type]
        if not os.path.exists(lib_dir + get_lib_name(jar_url)):
            save_lib(jar_url, lib_dir + get_lib_name(jar_url))
        version_type_dic["version"] = version
        version_type_dic["_type"] = _type
        version_type_dic["classifier"] = classifier
        version_type_dic["jar_package_url"] = get_lib_name(jar_url)
        version_types_list.append(version_type_dic)
        return
    if _type == "tar.gz" or _type == "zip" or _type == "jar" or _type == "test-jar" or _type == "nbm-file" or _type == "xml" or _type == "war" or _type == "kar":
        new_type = _type
        if _type == "nbm-file":
            new_type = "nbm"
        if 'View' in file_list:
            page_url = file_list['View']
            success, package_url = get_lib_from_list_page(page_url, new_type, classifier)
            if success:
                version_type_dic["version"] = version
                version_type_dic["_type"] = _type
                version_type_dic["classifier"] = classifier
                version_type_dic["jar_package_url"] = get_lib_name(package_url)
                version_types_list.append(version_type_dic)
    # if _type == "xml":
    #     return
    else:
        # print("!!!!!!!!!!!!!!!!!!!! unhandled type: " + str(_type))
        raise (CustomizeException("id: "+str(curr_project_id)+"\n version:"+str(version)+"classifier:"+str(classifier)+"type:"+str(_type)+"\n!!!!!!!!!!!!!!!!!!!! unhandled type: " + str(_type)))

def get_lib_from_list_page(page_path, _type, classifier):
    time.sleep(random.randint(2, 5))
    lib_list = get_lib_list_of_one_version(page_path)
    return download_lib_from_list(lib_list, page_path, _type, classifier)

def download_lib_from_list(lib_list, page_path, _type, classifier):
    success = False
    package_url = None

    for lib_package in lib_list:
        if _type == "test-jar" and lib_package.endswith(
                ".jar") and "-sources" not in lib_package and "-javadoc" not in lib_package and "tests" in lib_package:
            url = None
            if classifier is not None:
                if classifier in lib_package:
                    url = page_path + "/" + lib_package
            else:
                url = page_path + "/" + lib_package
            if url is not None:
                package_url = lib_package
                if not os.path.exists(lib_dir + lib_package):
                    save_lib(url, lib_dir + lib_package)
                success = True
                break
        elif lib_package.endswith("." + _type) and "-sources" not in lib_package and "-javadoc" not in lib_package:
            url = None
            if classifier is not None:
                if classifier in lib_package:
                    url = page_path + "/" + lib_package
            else:
                url = page_path + "/" + lib_package
            if url is not None:
                package_url = lib_package
                if not os.path.exists(lib_dir + lib_package):
                    save_lib(url, lib_dir + lib_package)
                success = True
                break
    return success, package_url

def get_lib_list_of_one_version(path):
    newlist = []
    try:
        # time.sleep(random.randint(3, 6))
        # time.sleep(random.randint(1, 3))
        headers = {'User-Agent': random.choice(agents)}
        page = requests.get(path, headers=headers)
        soup = BeautifulSoup(page.text, 'lxml');
        list = soup.find_all('a')
        for li in list:
            newlist.append(li.get_text())
    except Exception as e:
        print('no use repo: ' + str(path))
    return newlist

def get_lib_from_maven_repo(groupId, artifactId, version, _type, classifier):
    version_url = "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId + "/" + version
    # time.sleep(random.randint(10, 18))
    time.sleep(random.randint(1, 3))
    headers = {'User-Agent': random.choice(agents)}
    library_version = requests.get(version_url, headers=headers)
    library_soup = BeautifulSoup(library_version.text, 'lxml');
    category_url = None
    if library_soup.find('h2', class_='im-title') is None:
        print("can't find h2 'im-title' class")
        get_lib_from_other_repo(groupId, artifactId, version, _type, classifier)
        return
    titles = library_soup.find('h2', class_='im-title').find_all('a')
    if titles[len(titles) - 1].get_text() == version:
        if len(titles) - 2 >= 0:
            category_url = "https://mvnrepository.com" + titles[len(titles) - 2]["href"]
            print("category_url:" + category_url)
    results = library_soup.find('div', class_='im')
    if results is None:
        print("can't find 'im' class")
        get_lib_from_other_repo(groupId, artifactId, version, _type, classifier)
        return
    results = results.find_next_sibling(class_='grid')
    information_trs = results.find_all('tr')
    repository, license, categories, organization, home_page, files, used_by = None, None, None, None, None, None, None
    for tr in information_trs:
        if 'License' == tr.th.string:
            license = ''
            spans = tr.td.find_all('span')
            for span in spans:
                license = license + span.string + ','
            if license[len(license) - 1] == ',':
                license = license[:-1].replace('\n', '')
        if 'Categories' == tr.th.string:
            categories = "{\"" + tr.td.a.string.replace('\n', '') + "\":\"" + "http://mvnrepository.com" + tr.td.a[
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
            date = tr.td.string
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
        if 'Repositories' == tr.th.string:
            entries = tr.td.find_all('a')
            if entries is not None:
                for each in entries:
                    repository = "http://mvnrepository.com" + each["href"]
                    break
        if 'Used By' == tr.th.string:
            used_by = "{\"" + tr.td.a.string.replace('\n', '') + "\":\"" + "http://mvnrepository.com" + tr.td.a[
                "href"] + "\"}"
    print('    repository:' + str(repository))
    # print('    license:' + str(license))
    # print('    categories:' + str(categories))
    # print('    organization:' + str(organization))
    # print('    home_page:' + str(home_page))
    print('    date:' + str(date))
    print('    files:' + str(files))
    # print('    used_by:' + str(used_by))
    if "https://mvnrepository.com" not in crawled_repo:
        # time.sleep(random.randint(15, 20))
        time.sleep(random.randint(1, 3))
        headers = {'User-Agent': random.choice(agents)}
        library = requests.get("https://mvnrepository.com/artifact/" + groupId + "/" + artifactId, headers=headers)
        library_soup = BeautifulSoup(library.text, 'lxml');
        results = library_soup.find('ul', class_='tabs').find_all('li')
        for tab in results:
            temp = get_other_library_versions_in_maven("http://mvnrepository.com" + tab.a["href"],
                                                       "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId,
                                                       groupId, artifactId, version)
            if temp is not None:
                repository = temp
        crawled_repo.append("https://mvnrepository.com")

    library_version_dic = {}
    library_version_dic["group"] = groupId
    library_version_dic["name"] = artifactId
    library_version_dic["version"] = version
    library_version_dic["version_url"] = version_url
    library_version_dic["license"] = license
    library_version_dic["categories"] = categories
    library_version_dic["organization"] = organization
    library_version_dic["home_page"] = home_page
    library_version_dic["date"] = date
    library_version_dic["files"] = files
    library_version_dic["repository"] = repository
    library_version_dic["used_by"] = used_by
    library_version_dic["category_url"] = category_url
    library_versions_list.append(library_version_dic)
    # version_id = insert_library_version(groupId, artifactId, version, version_url, license, categories,
    #                                     organization,
    #                                     home_page, date,
    #                                     files, repository, used_by, category_url)
    save_lib_package(files, _type, classifier,version)

def get_other_library_versions_in_maven(tab_url, category_url, groupId, artifactId, target_version):
    target_version_repo = None
    # time.sleep(random.randint(12, 15))
    time.sleep(random.randint(1, 3))
    headers = {'User-Agent': random.choice(agents)}
    print('------------------------- tab_url:' + tab_url)
    library_tab = requests.get(tab_url, headers=headers)
    library_soup = BeautifulSoup(library_tab.text, 'lxml');
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
        raise (CustomizeException("id: "+str(curr_project_id)+"\n tab_url:"+str(tab_url)+"\n groupId:"+str(groupId)+"artifactId:"+str(artifactId)+"target_version:"+str(target_version)+"\nVersion Repository Usages Date imcomplete"))
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
            version_url = category_url[0:category_url.rindex('/')] + '/' + tds[tr_version].a["href"]
            version = tds[tr_version].a.string.replace('\n', '')
            repository = "http://mvnrepository.com" + tds[tr_repository].a["href"]
            usages = None
            if tds[tr_usages].a is None:
                usages = "{'" + tds[tr_usages].get_text().replace('\n', '') + "':''}"
            else:
                usages = "{'" + tds[tr_usages].a.string.replace('\n', '') + "':'" + category_url + tds[tr_usages].a[
                    "href"] + "'}"
            date = tds[tr_date].string.replace('\n', '')
            # time.sleep(random.randint(15, 25))
            time.sleep(random.randint(1, 3))
            headers = {'User-Agent': random.choice(agents)}
            library_version = requests.get(version_url, headers=headers)
            page = library_version.text
            library_soup = BeautifulSoup(library_version.text, 'lxml');
            results = library_soup.find('div', class_='im')
            if results is None:
                raise (CustomizeException("id: "+str(curr_project_id)+"\n tab_url:"+str(tab_url)+"\n groupId:"+str(groupId)+"artifactId:"+str(artifactId)+"target_version:"+str(target_version)+"\ncan't find 'im' class"))
                # print("can't find 'im' class")
                # return
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
                    categories = "{\"" + tr.td.a.string.replace('\n', '') + "\":\"" + "http://mvnrepository.com" + \
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
                    date = tr.td.string
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
                    used_by = "{\"" + tr.td.a.string.replace('\n', '') + "\":\"" + "http://mvnrepository.com" + tr.td.a[
                        "href"] + "\"}"
            print('    repository:' + str(repository))
            print('    date:' + str(date))
            print('    files:' + str(files))
            if target_version == version:
                target_version_repo = repository
            else:
                declarations = library_soup.find('div', id='snippets')
                if declarations is not None:
                    declarations = str(declarations)
                declarations_soup = BeautifulSoup(str(declarations), 'lxml');
                maven = declarations_soup.find(id='maven-a').string
                declarations_soup = BeautifulSoup(maven, 'xml');
                group = declarations_soup.find('groupId').string
                name1 = declarations_soup.find('artifactId').string
                version1 = declarations_soup.find('version').string
                library_version_dic = {}
                library_version_dic["group"] = group
                library_version_dic["name"] = name1
                library_version_dic["version"] = version1
                library_version_dic["version_url"] = version_url
                library_version_dic["license"] = license
                library_version_dic["categories"] = categories
                library_version_dic["organization"] = organization
                library_version_dic["home_page"] = home_page
                library_version_dic["date"] = date
                library_version_dic["files"] = files
                library_version_dic["repository"] = repository
                library_version_dic["used_by"] = used_by
                library_version_dic["category_url"] = category_url
                library_versions_list.append(library_version_dic)
                # insert_library_version(groupId, artifactId, version, version_url, license, categories, organization,
                #                        home_page, date, files, repository, used_by, category_url)
    return target_version_repo

def get_lib_from_other_repo(groupId, artifactId, version, _type, classifier):
    success = False
    for repo_url in repo_array:
        success = save_lib_in_other_repo(repo_url, groupId, artifactId, version, _type, classifier)
        if success:
            break
    if not success:
        # insert_unsolved_library(groupId, artifactId, version, _type, classifier)
        unsolved_library_dic = {}
        unsolved_library_dic["group"] = groupId
        unsolved_library_dic["name"] = artifactId
        unsolved_library_dic["version"] = version
        unsolved_library_dic["_type"] = _type
        unsolved_library_dic["classifier"] = classifier
        unsolved_lib_list.append(unsolved_library_dic)

def save_lib_in_other_repo(repo_url, groupId, artifactId, version, _type, classifier):
    print("try repo_url: " + repo_url)
    groupUrl = groupId.replace('.', '/')
    list_page_url = repo_url + "/" + groupUrl + "/" + artifactId + "/" + version
    lib_list = get_lib_list_of_one_version(list_page_url)
    maven_metadata_url = list_page_url + "/" + "maven-metadata.xml"
    success = False
    try:
        meta_data = requests.get(maven_metadata_url, headers=headers)
        if meta_data is not None:
            meta_data_soup = BeautifulSoup(meta_data.text, 'xml');
            snapshot_date = None
            if meta_data_soup.find('timestamp') is not None:
                snapshot_date = meta_data_soup.find('timestamp').string
            elif meta_data_soup.find('lastUpdated') is not None:
                snapshot_date = meta_data_soup.find('lastUpdated').string
            snapshot_versions = meta_data_soup.find_all('snapshotVersion')
            for snapshot_version in snapshot_versions:
                snapshot_type = snapshot_version.extension.string
                if snapshot_type == _type:
                    snapshot_classifier = None
                    if snapshot_version.classifier is not None:
                        snapshot_classifier = snapshot_version.classifier.string

                    version_num = snapshot_version.value.string
                    package_url = None
                    if classifier is None and snapshot_classifier is None:
                        package_url = artifactId + "-" + version_num + "." + _type
                    elif classifier is not None and snapshot_classifier is not None and classifier == snapshot_classifier:
                        package_url = artifactId + "-" + version_num + "-" + classifier + "." + _type
                    if package_url is None:
                        continue

                    print(package_url)
                    lib_name = None
                    if package_url in lib_list:
                        if not os.path.exists(lib_dir + package_url):
                            save_lib(list_page_url + "/" + package_url, lib_dir + package_url)
                        success = True
                        lib_name = package_url
                    else:
                        success, lib_name = download_lib_from_list(lib_list, list_page_url, _type, classifier)
                    if success:
                        # other versions
                        if repo_url not in crawled_repo:
                            library_url = list_page_url[0:list_page_url.rindex('/')]
                            get_other_library_versions_in_other_repo(repo_url,library_url, groupId, artifactId, version)
                            crawled_repo.append(repo_url)

                        print('    repository:' + str(repo_url))
                        print('    date:' + str(snapshot_date))
                        library_version_dic = {}
                        library_version_dic["group"] = groupId
                        library_version_dic["name"] = artifactId
                        library_version_dic["version"] = version
                        library_version_dic["version_url"] = list_page_url
                        library_version_dic["license"] = None
                        library_version_dic["categories"] = None
                        library_version_dic["organization"] = None
                        library_version_dic["home_page"] = None
                        library_version_dic["date"] = snapshot_date
                        library_version_dic["files"] = None
                        library_version_dic["repository"] = repo_url
                        library_version_dic["used_by"] = None
                        library_version_dic["category_url"] = None
                        library_versions_list.append(library_version_dic)
                        # version_id = insert_library_version(groupId, artifactId, version, list_page_url, None,
                        #                                     None, None, None, snapshot_date, None, repo_url,
                        #                                     None, None)
                        # version_type_id = insert_version_type(version_id, _type, classifier,
                        #                                       get_lib_name(lib_name))
                        version_type_dic = {}
                        version_type_dic["version"] = version
                        version_type_dic["_type"] = _type
                        version_type_dic["classifier"] = classifier
                        version_type_dic["jar_package_url"] = get_lib_name(package_url)
                        version_types_list.append(version_type_dic)

                    break
    except Exception as e:
        meta_data = None
    return success

def get_other_library_versions_in_other_repo(repo_url,library_url, groupId,artifactId, target_version):
    versions_meta_url = library_url + "/" + "maven-metadata.xml"
    try:
        # time.sleep(random.randint(3, 6))
        versions_meta_data = requests.get(versions_meta_url, headers=headers)
        if versions_meta_data is not None:
            meta_data_soup = BeautifulSoup(versions_meta_data.text, 'xml');
            versions = meta_data_soup.find_all('version')
            version_list = []
            for v in versions:
                version_list.append(v.string)
            for ver in version_list:
                if ver != target_version:
                    version_detail_url = library_url + "/" + ver
                    version_detail_meta_url = version_detail_url + "/" + "maven-metadata.xml"
                    # time.sleep(random.randint(3, 6))
                    versions_meta_data = requests.get(version_detail_meta_url, headers=headers)
                    meta_data_soup = BeautifulSoup(versions_meta_data.text, 'xml');
                    update_date = None
                    if meta_data_soup.find('timestamp') is not None:
                        update_date = meta_data_soup.find('timestamp').string
                    # insert_library_version(groupId, artifactId, ver, version_detail_url, None,
                    #                                 None, None, None, update_date, None, repo_url,
                    #                                 None, None)
                    print('    repository:' + str(repo_url))
                    print('    date:' + str(update_date))
                    library_version_dic = {}
                    library_version_dic["group"] = groupId
                    library_version_dic["name"] = artifactId
                    library_version_dic["version"] = ver
                    library_version_dic["version_url"] = version_detail_url
                    library_version_dic["license"] = None
                    library_version_dic["categories"] = None
                    library_version_dic["organization"] = None
                    library_version_dic["home_page"] = None
                    library_version_dic["date"] = update_date
                    library_version_dic["files"] = None
                    library_version_dic["repository"] = repo_url
                    library_version_dic["used_by"] = None
                    library_version_dic["category_url"] = None
                    library_versions_list.append(library_version_dic)

    except Exception as e:
        versions_meta_data = None

def handle_lib_by_range(start, end):
    global curr_project_id
    # 2845
    # json_data = read_json("combined_dependencies_list.txt")
    json_data = read_json("dependencies_list.txt")
    print(len(json_data))
    for i in range(start, end):
        print("+++++++++++++++++++++++++++++++ " + str(i))
        curr_project_id = i
        handle_one_lib(json_data[i])

def handle_one_lib(lib_obj):
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    key = lib_obj['lib_name']
    if os.path.exists(output_dir+"/"+key+".json"):
        return
    global repo_array,crawled_repo,library_versions_list,version_types_list,unsolved_lib_list
    crawled_repo = []
    library_versions_list = []
    version_types_list = []
    unsolved_lib_list = []
    versions_array = lib_obj['versions_array']
    repo_array = lib_obj['repo_array']
    names = key.split(' ')
    if len(names) != 2:
        raise (CustomizeException("id: "+str(curr_project_id)+"\n key:" +str(key) + "\nnames length != 2"))
    groupId = names[0]
    artifactId = names[1]
    # print(groupId + "====" + artifactId)
    for version_info in versions_array:
        values = version_info.split(' ')
        if len(values) != 2 and len(values) != 3:
            raise (CustomizeException("id: "+str(curr_project_id)+"\n key:" +str(key) + "\nvalues length != 2 or 3:" + str(version_info)))
        version = values[0]
        _type = values[1]
        classifier = None
        if len(values) == 3:
            classifier = values[2]
        print(groupId + " ==== " + artifactId + " ==== " + version + " ==== " + _type + " ==== " + str(classifier))
        get_lib_from_maven_repo(groupId, artifactId, version, _type, classifier)
    save_obj = {}
    save_obj['library_versions_list'] = library_versions_list
    save_obj['version_types_list'] = version_types_list
    save_obj['unsolved_lib_list'] = unsolved_lib_list
    write_json(output_dir+"/"+key+".json", save_obj)
# get_denpendencies_of_proj(4,5539)
# print(len(lib_dict))
# dependency_dict_to_list()
# 90 573 589
numa = sys.argv[2]
numb = sys.argv[3]
handle_lib_by_range(int(numa),int(numb))
# save_lib_package("{\"View\":\"http://bits.netbeans.org/nexus/content/groups/netbeans/org/netbeans/modules/org-netbeans-modules-spi-actions/RELEASE82/\"}", "nbm-file", None,"RELEASE82")