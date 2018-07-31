import json

import os
import random

import requests
import time

import database
from exception import CustomizeException
from bs4 import BeautifulSoup

from file_util import save_lib, get_lib_name, read_json, read_file

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
db = database.connectdb()
repo_dir = "E:/data/repo"

def insert_project_lib_usage(project_id, version_type_id, module_):
    sql = "SELECT * FROM project_lib_usage WHERE project_id = '" + str(project_id) +"' and version_type_id = " + str(version_type_id)
    record = database.querydb(db, sql)
    if len(record) == 0:
        if module_ is None:
            sql = "INSERT INTO project_lib_usage (project_id,version_type_id) VALUES ('" + str(project_id) + "','" + str(version_type_id) + "')"
        else:
            sql = "INSERT INTO project_lib_usage (project_id,version_type_id,module) VALUES ('" + str(project_id) + "','" + str(version_type_id) + "','"+ str(module_) + "')"
        database.execute_sql(db, sql)
        print('======================== INSERT INTO project_lib_usage : ' + str(project_id) + "  " + str(version_type_id))


def insert_version_type(version_id,_type,classifier,jar_package_url):
    if classifier is None:
        sql = "INSERT INTO version_types" \
              "(version_id,type,classifier,jar_package_url) " \
              "VALUES (\'" \
              + str(version_id).replace("'", "''") + "\',\'" \
              + str(_type).replace("'", "''") + "\',NULL,\'" \
              + str(jar_package_url).replace("'", "''") + "\')"
    else:
        sql = "INSERT INTO version_types" \
              "(version_id,type,classifier,jar_package_url) " \
              "VALUES (\'" \
              + str(version_id).replace("'", "''") + "\',\'" \
              + str(_type).replace("'", "''") + "\',\'" \
              + str(classifier).replace("'", "''") + "\',\'" \
              + str(jar_package_url).replace("'", "''") + "\')"
    database.execute_sql(db, sql)
    print('======================== INSERT INTO version_types : ' + str(version_id) + "  " + str(_type)+"  " + str(classifier)+"  " + str(jar_package_url))
    sql = "SELECT LAST_INSERT_ID()"
    results = database.querydb(db, sql)
    return results[0][0]

def insert_library_version(group,name1,version1,version_url,license,categories,organization,home_page,date,files,repository,used_by,category_url):
    sql = "INSERT INTO library_versions" \
          "(group_str,name_str,version,url,license,categories,organization,home_page,date,files,repository,used_by,category_url) " \
          "VALUES (\'" \
          + str(group).replace("'", "''") + "\',\'" \
          + str(name1).replace("'", "''") + "\',\'" \
          + str(version1).replace("'", "''") + "\',\'" \
          + str(version_url).replace("'", "''") + "\',"

    if license is not None:
        sql += "\'" + str(license).replace("'", "''") + "\',"
    else:
        sql += "NULL,"
    if categories is not None:
        sql += "\'" + str(categories).replace("'", "''") + "\',"
    else:
        sql += "NULL,"
    if organization is not None:
        sql += "\'" + str(organization).replace("'", "''") + "\',"
    else:
        sql += "NULL,"
    if home_page is not None:
        sql += "\'" + str(home_page).replace("'", "''") + "\',"
    else:
        sql += "NULL,"
    if date is not None:
        sql += "\'" + str(date).replace("'", "''") + "\',"
    else:
        sql += "NULL,"
    if files is not None:
        sql += "\'" + str(files).replace("'", "''") + "\',"
    else:
        sql += "NULL,"
    if repository is not None:
        sql += "\'" + str(repository).replace("'", "''") + "\',"
    else:
        sql += "NULL,"
    if used_by is not None:
        sql += "\'" + str(used_by).replace("'", "''") + "\',"
    else:
        sql += "NULL,"
    if category_url is not None:
        sql += "\'" + str(category_url).replace("'", "''") + "\')"
    else:
        sql += "NULL)"
    database.execute_sql(db, sql)
    print('======================== INSERT INTO library_versions :' + str(group) + "  " + str(name1)+"  " + str(version1))
    sql = "SELECT LAST_INSERT_ID()"
    results = database.querydb(db, sql)
    return results[0][0]

def insert_unsolved_library(group,name1,version1,_type,classifier,project_id):
    if classifier is None:
        sql = "SELECT * FROM unsolved_libraries WHERE group_str = '" + str(group) + "' and name_str = '" + str(
        name1) +"' and version = '"+str(version1)+"' and type = '"+str(_type)+"' and classifier = NULL"
    else:
        sql = "SELECT * FROM unsolved_libraries WHERE group_str = '" + str(group) + "' and name_str = '" + str(
        name1) +"' and version = '"+str(version1)+"' and type = '"+str(_type)+"' and classifier = '"+str(classifier)+"'"
    record = database.querydb(db, sql)
    if len(record) == 0:
        sql = "INSERT INTO unsolved_libraries" \
              "(project_id, group_str,name_str,version,type,classifier) " \
              "VALUES (\'" \
              + str(project_id).replace("'", "''") + "\',\'" \
              + str(group).replace("'", "''") + "\',\'" \
              + str(name1).replace("'", "''") + "\',\'" \
              + str(version1).replace("'", "''") + "\',\'" \
              + str(_type).replace("'", "''") + "\',"
        if classifier is not None:
            sql += "\'" + str(classifier).replace("'", "''") + "\')"
        else:
            sql += "NULL)"
        database.execute_sql(db, sql)
        print('======================== INSERT INTO unsolved_libraries :' + str(group) + "  " + str(name1)+"  " + str(version1)+"  " + str(_type)+"  " + str(classifier))

def download_lib_from_list(lib_list,page_path,_type,classifier):
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
                if not os.path.exists("F:/GP/lib/" + lib_package):
                    save_lib(url, "F:/GP/lib/" + lib_package)
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
                if not os.path.exists("F:/GP/lib/" + lib_package):
                    save_lib(url, "F:/GP/lib/" + lib_package)
                success = True
                break
    return success, package_url

def get_lib_from_list_page(page_path,_type,classifier):
    success = False
    package_url = None
    time.sleep(random.randint(2, 5))
    lib_list = get_lib_list_of_one_version(page_path)
    return download_lib_from_list(lib_list, page_path, _type, classifier)

def save_lib_package(files, version_id, _type, classifier, project_id, module_):
    file_list = json.loads(files)
    if _type in file_list:
        jar_url = file_list[_type]
        if not os.path.exists("F:/GP/lib/" + get_lib_name(jar_url)):
            save_lib(jar_url, "F:/GP/lib/" + get_lib_name(jar_url))
        version_type_id = insert_version_type(version_id, _type, classifier, get_lib_name(jar_url))
        insert_project_lib_usage(project_id, version_type_id, module_)
        return
    if _type == "tar.gz" or _type == "zip" or _type == "jar" or _type == "test-jar":
        if 'View' in file_list:
            page_url = file_list['View']
            success,package_url = get_lib_from_list_page(page_url, _type, classifier)
            if success:
                version_type_id = insert_version_type(version_id, _type, classifier, get_lib_name(package_url))
                insert_project_lib_usage(project_id, version_type_id, module_)
    # if _type == "xml":
    #     return
    else:
        # print("!!!!!!!!!!!!!!!!!!!! unhandled type: " + str(_type))
        raise (CustomizeException("!!!!!!!!!!!!!!!!!!!! unhandled type: " + str(_type)))

def library_crawler(groupId, artifactId, version, _type, classifier, project_id, module_):
    print("groupId: " + str(groupId) + ", artifactId: " + str(artifactId) + ", version: " + str(
            version) + ", type: " + str(_type) + ", classifier: " + str(classifier)+ ", module: " + str(module_))
    version_url = "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId + "/" + version
    print(version_url)
    sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId)+"' and name_str = '"+str(artifactId)+"' and version = '"+str(version)+"'"
    version_info = database.querydb(db, sql)
    if len(version_info) != 0:
        version_id = version_info[0][0]

        print("+++++++++++++++++++++++++version_id:" +str(version_id))
        sql = "SELECT * FROM version_types WHERE version_id = " + str(version_id)
        types = database.querydb(db, sql)
        for t in types:
            if t[2] == _type:
                if (classifier is not None and classifier == t[3]) or (classifier == None and t[3] == None):
                    insert_project_lib_usage(project_id, t[0], module_)
                    return
        files = version_info[0][12]
        if files != None:
            save_lib_package(files, version_id, _type, classifier, project_id, module_)
        else:
            get_lib_from_other_repo(version_id, groupId, artifactId, version, _type, classifier, project_id, module_)

    else:
        get_lib_from_maven_repo(version_url, groupId, artifactId, version, _type, classifier, project_id, module_)
    # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

def get_lib_from_maven_repo(version_url,groupId, artifactId, version, _type, classifier, project_id, module_):
    library_version = requests.get(version_url, headers=headers)
    library_soup = BeautifulSoup(library_version.text, 'lxml');
    category_url = None
    if library_soup.find('h2', class_='im-title') is None:
        print("can't find h2 'im-title' class")
        get_lib_from_other_repo(-1, groupId, artifactId, version, _type, classifier, project_id, module_)
        # insert_unsolved_library(groupId, artifactId, version, project_id)
        return
    titles = library_soup.find('h2', class_='im-title').find_all('a')
    if titles[len(titles) - 1].get_text() == version:
        if len(titles) - 2 >= 0:
            category_url = "https://mvnrepository.com" + titles[len(titles) - 2]["href"]
            print("category_url:" + category_url)
    results = library_soup.find('div', class_='im')
    if results is None:
        print("can't find 'im' class")
        get_lib_from_other_repo(-1, groupId, artifactId, version, _type, classifier, project_id, module_)
        # insert_unsolved_library(groupId, artifactId, version, project_id)
        return
        # raise (CustomizeException("can't find 'im' class"))
    time.sleep(random.randint(10, 18))
    results = results.find_next_sibling(class_='grid')
    information_trs = results.find_all('tr')
    license = None
    categories = None
    organization = None
    home_page = None
    files = None
    used_by = None
    declarations = None
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
                repository = "{"
                for each in entries:
                    repository = repository + "\"" + each.string.replace('\n',
                                                                         '') + "\":\"" + "http://mvnrepository.com" + \
                                 each["href"] + "\","
                if repository[len(repository) - 1] == ",":
                    repository = repository[:-1]
                    repository = repository + "}"
        if 'Used By' == tr.th.string:
            used_by = "{\"" + tr.td.a.string.replace('\n', '') + "\":\"" + "http://mvnrepository.com" + tr.td.a[
                "href"] + "\"}"
    print('    license:', end="")
    print(license)
    print('    categories:', end="")
    print(categories)
    print('    organization:', end="")
    print(organization)
    print('    home_page:', end="")
    print(home_page)
    print('    date:', end="")
    print(date)
    print('    files:', end="")
    print(files)
    print('    repository:', end="")
    print(repository)
    print('    used_by:', end="")
    print(used_by)
    declarations = library_soup.find('div', id='snippets')
    if declarations is not None:
        declarations = str(declarations)
    declarations_soup = BeautifulSoup(str(declarations), 'lxml');
    maven = declarations_soup.find(id='maven-a').string
    declarations_soup = BeautifulSoup(maven, 'xml');
    group = declarations_soup.find('groupId').string
    name1 = declarations_soup.find('artifactId').string
    version1 = declarations_soup.find('version').string
    # print(group)
    # print(name1)
    # print(version1)
    version_id = insert_library_version(group, name1, version1, version_url, license, categories, organization,
                                        home_page, date,
                                        files, repository, used_by, category_url)
    save_lib_package(files, version_id, _type, classifier, project_id, module_)

def get_lib_from_other_repo(version_id,groupId, artifactId, version, _type, classifier, project_id, module_):
    success = False
    repo_file = repo_dir + "/" + str(project_id) + ".txt"
    if os.path.exists(repo_file):
        lines = read_file(repo_file)
        for i in range(len(lines)):
            repo_url = lines[i]
            groupUrl = groupId.replace('.', '/')
            list_page_url = repo_url + "/" + groupUrl + "/" + artifactId + "/" + version
            if not list_page_url.startswith("https://") and not list_page_url.startswith("http://"):
                list_page_url = "http://" + list_page_url
            success = save_lib_in_other_repo(list_page_url, version_id, groupId, artifactId, version, _type, classifier,
                                   project_id, module_)
            if success:
                break
    if not success:
        insert_unsolved_library(groupId, artifactId, version, _type, classifier, project_id)


def save_lib_in_other_repo(list_page_url, version_id, groupId, artifactId, version, _type, classifier, project_id, module_):
    lib_list = get_lib_list_of_one_version(list_page_url)
    maven_metadata_url = list_page_url + "/" + "maven-metadata.xml"
    snapshot_date = None
    success = False
    try:
        meta_data = requests.get(maven_metadata_url, headers=headers)
        if meta_data is not None:
            meta_data_soup = BeautifulSoup(meta_data.text, 'xml');
            snapshot_date = meta_data_soup.find('timestamp')
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
                        if not os.path.exists("F:/GP/lib/" + package_url):
                            save_lib(list_page_url + "/" + package_url, "F:/GP/lib/" + package_url)
                        success = True
                        lib_name = package_url
                    else:
                        success, lib_name = download_lib_from_list(lib_list, list_page_url, _type, classifier)
                    if success:
                        if version_id < 0:
                            version_id = insert_library_version(groupId, artifactId, version, list_page_url, None,
                                                                None, None, None, snapshot_date, None, None,
                                                                None, None)
                        version_type_id = insert_version_type(version_id, _type, classifier,
                                                              get_lib_name(lib_name))
                        insert_project_lib_usage(project_id, version_type_id, module_)
                    break
    except Exception as e:
        meta_data = None
    return success

def get_lib_list_of_one_version(path):
    newlist = []
    try:
        time.sleep(random.randint(2, 5))
        page = requests.get(path, headers=headers)
        soup = BeautifulSoup(page.text, 'lxml');
        list = soup.find_all('a')
        for li in list:
            newlist.append(li.get_text())
    except Exception as e:
        print('no use repo: '+str(path))
    return newlist

def get_lib_usedby_project(path):
    if not os.path.exists(path):
        return
    print()
    data = read_json(path)
    project_id = None
    module_ = None
    do = False
    for lib in data:
        if 'id' in lib:
            project_id = lib["id"]
            print("-------------------- project_id: " + str(project_id))
            continue
        if "groupId" not in lib or "artifactId" not in lib or "version" not in lib:
            print(False)
            continue
        groupId= lib["groupId"]
        artifactId = lib["artifactId"]
        version = lib["version"]
        type_ = lib["type"]
        if groupId is None or artifactId is None or version is None or type_ is None or '${' in groupId or '${' in artifactId or '${' in version or '${' in type_:
            print("groupId: " + str(groupId) +"   artifactId: " + str(artifactId)+"   version: " + str(version)+"   type: " + str(type_) )
            print(False)
            continue
        if project_id is None:
            continue
        classifier = None

        if "classifier" in lib:
            classifier = lib["classifier"]
            if '${' in classifier:
                print("groupId: " + str(groupId) + "   artifactId: " + str(artifactId) + "   version: " + str(
                    version) + "   type: " + str(type_) + "   classifier: " + str(classifier))
                print(False)
                continue
        if "module" in lib:
            module_ = lib["module"]
        # if not do:
        #     if artifactId == "apex-common" and groupId == "org.apache.apex":
        #         do = True
        #     else:
        #         continue
        # if do:
        if type(version) == list:
            continue
            # for ver in version:
            #     save_version_information(groupId, artifactId, ver, type_, classifier, project_id, module_)
        else:
            library_crawler(groupId, artifactId, version, type_, classifier, project_id, module_)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# save_version_information("org.apache.mina", "mina-integration-beans", "2.0.17", "jar", None,1)
# read_used_library()
#1139 649 1213 492 654 1261 1265
# for i in range(1, 2):
#     get_lib_usedby_project("E:/data/curr_result_all/"+str(i)+".txt")
# print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
# get_lib_usedby_project("C:/Users/yw/Desktop/result/"+str(4)+".txt")
# package = requests.get("https://oss.sonatype.org/content/repositories/snapshots/consulting/omnia/util/util-io/1.0-SNAPSHOT/util-io-1.0-20150804.045928-1.pom", headers=headers)
# print(package.content)
# print(package.text)
# page = requests.get("http://central.maven.org/maven2/org/apache/zookeeper/zookeeper/3.4.10/", headers=headers)
# soup = BeautifulSoup(page.text, 'lxml');
# list = soup.find_all('a')
# newlist = []
# for li in list:
#     newlist.append(li.get_text())
#     print(li.get_text())
# print("zookeeper-3.4.10-javadoc.jar" in newlist)
# print("zar" in newlist)
# insert_library_version("test", "test", "test", "test", None,None, None, None, "test", None, None,
#                                                                 None, None)
