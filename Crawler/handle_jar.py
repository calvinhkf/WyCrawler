import json

import os
import random

import requests
import time

import database
from exception import CustomizeException
from bs4 import BeautifulSoup

from file_util import save_lib, get_lib_name, read_json

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
# db = database.connectdb()
# lib_path = "F:/GP/lib/"
lib_path = "C:/Users/yw/Desktop/lib/"
result_path ="C:/Users/yw/Desktop/result/"
output_path ="C:/Users/yw/Desktop/"

project_array = []
version_type_dic = {}
lib_usage_dic = {}
library_version_dic = {}
entry_dic = {}

# def insert_project_lib_usage(project_id, version_type_id, module_):
#     sql = "SELECT * FROM project_lib_usage WHERE project_id = '" + str(project_id) +"' and version_type_id = " + str(version_type_id)
#     record = database.querydb(db, sql)
#     if len(record) == 0:
#         if module_ is None:
#             sql = "INSERT INTO project_lib_usage (project_id,version_type_id) VALUES ('" + str(project_id) + "','" + str(version_type_id) + "')"
#         else:
#             sql = "INSERT INTO project_lib_usage (project_id,version_type_id,module) VALUES ('" + str(project_id) + "','" + str(version_type_id) + "','"+ str(module_) + "')"
#         database.execute_sql(db, sql)
#         print('======================== INSERT INTO project_lib_usage : ' + str(project_id) + "  " + str(version_type_id))
#
#
# def insert_version_type(version_id,_type,classifier,jar_package_url):
#     sql = "INSERT INTO version_types" \
#           "(version_id,type,classifier,jar_package_url) " \
#           "VALUES (\'" \
#           + str(version_id).replace("'", "''") + "\',\'" \
#           + str(_type).replace("'", "''") + "\',\'" \
#           + str(classifier).replace("'", "''") + "\',\'" \
#           + str(jar_package_url).replace("'", "''") + "\')"
#     database.execute_sql(db, sql)
#     print('======================== INSERT INTO version_types : ' + str(version_id) + "  " + str(_type)+"  " + str(classifier)+"  " + str(jar_package_url))
#     sql = "SELECT LAST_INSERT_ID()"
#     results = database.querydb(db, sql)
#     return results[0][0]
#
# def insert_library_version(group,name1,version1,version_url,license,categories,organization,home_page,date,files,repository,used_by,page,category_url):
#     sql = "INSERT INTO library_versions" \
#           "(group_str,name_str,version,url,license,categories,organization,home_page,date,files,repository,used_by,page,category_url) " \
#           "VALUES (\'" \
#           + str(group).replace("'", "''") + "\',\'" \
#           + str(name1).replace("'", "''") + "\',\'" \
#           + str(version1).replace("'", "''") + "\',\'" \
#           + str(version_url).replace("'", "''") + "\',\'" \
#           + str(license).replace("'", "''") + "\',\'" \
#           + str(categories).replace("'", "''") + "\',\'" \
#           + str(organization).replace("'", "''") + "\',\'" \
#           + str(home_page).replace("'", "''") + "\',\'" \
#           + str(date).replace("'", "''") + "\',\'" \
#           + str(files).replace("'", "''") + "\',\'" \
#           + str(repository).replace("'", "''") + "\',\'" \
#           + str(used_by).replace("'", "''") + "\',\'" \
#           + str(page).replace("'", "''") + "\',\'" \
#           + str(category_url).replace("'", "''") + "\')"
#     database.execute_sql(db, sql)
#     print('======================== INSERT INTO library_versions :' + str(group) + "  " + str(name1)+"  " + str(version1))
#     sql = "SELECT LAST_INSERT_ID()"
#     results = database.querydb(db, sql)
#     return results[0][0]

def get_lib_from_list_page(page_path,_type,classifier):
    success = False
    package_url = None
    time.sleep(random.randint(15, 20))
    page = requests.get(page_path, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml');
    if soup.find('pre') is None:
        print("error : has no attribute 'pre'")
        return success, package_url
    list = soup.find('pre').find_all('a')
    for li in list:
        if _type == "test-jar" and li["href"].endswith(".jar") and "-sources" not in li["href"] and "-javadoc" not in li["href"] and "test" in li["href"]:
            url = None
            if classifier is not None:
                if classifier in li["href"]:
                    url = page_path + "/" + li["href"]
            else:
                url = page_path + "/" + li["href"]
            if url is not None:
                package_url = li["href"]
                if not os.path.exists(lib_path + li["href"]):
                    save_lib(url, lib_path + li["href"])
                success = True
                break
        elif li["href"].endswith("." + _type) and "-sources" not in li["href"] and "-javadoc" not in li["href"]:
            url = None
            if classifier is not None:
                if classifier in li["href"]:
                    url = page_path + "/" + li["href"]
            else:
                url = page_path + "/" + li["href"]
            if url is not None:
                package_url = li["href"]
                if not os.path.exists(lib_path + li["href"]):
                    save_lib(url, lib_path+ li["href"])
                success = True
                break
    return success, package_url

def save_lib_package(files, version_id, _type, classifier, project_id, module_):
    # library_versions :org.apache.hadoop  hadoop-hdfs  3.0.0-beta1
    global version_type_dic, lib_usage_dic
    file_list = json.loads(files)
    if _type in file_list:
        jar_url = file_list[_type]
        if not os.path.exists(lib_path + get_lib_name(jar_url)):
            save_lib(jar_url, lib_path + get_lib_name(jar_url))


        version_type_dic["_type"] = _type
        version_type_dic["classifier"] = classifier
        version_type_dic["jar_package_url"] = get_lib_name(jar_url)

        lib_usage_dic["module_"] = module_

        entry_dic["version_type"] = version_type_dic
        entry_dic["lib_usage"] = lib_usage_dic

        # version_type_id = insert_version_type(version_id, _type, classifier, get_lib_name(jar_url))
        # insert_project_lib_usage(project_id, version_type_id, module_)
        return
    if _type == "tar.gz" or _type == "zip" or _type == "jar" or _type == "test-jar":
        if 'View' in file_list:
            page_url = file_list['View']
            success,package_url = get_lib_from_list_page(page_url, _type, classifier)
            if success:
                version_type_dic["_type"] = _type
                version_type_dic["classifier"] = classifier
                version_type_dic["jar_package_url"] = get_lib_name(package_url)

                lib_usage_dic["module_"] = module_

                entry_dic["version_type"] = version_type_dic
                entry_dic["lib_usage"] = lib_usage_dic

            #     version_type_id = insert_version_type(version_id, _type, classifier, get_lib_name(package_url))
            #     insert_project_lib_usage(project_id, version_type_id, module_)
    # if _type == "xml":
    #     return
    else:
        print("!!!!!!!!!!!!!!!!!!!! unhandled type: " + str(_type))
        # raise (CustomizeException("!!!!!!!!!!!!!!!!!!!! unhandled type: " + str(_type)))

def save_version_information(groupId, artifactId, version, _type, classifier, project_id, module_):
    print("groupId: " + str(groupId) + ", artifactId: " + str(artifactId) + ", version: " + str(
            version) + ", type: " + str(_type) + ", classifier: " + str(classifier)+ ", module: " + str(module_))
    version_url = "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId + "/" + version
    print(version_url)
    # sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId)+"' and name_str = '"+str(artifactId)+"' and version = '"+str(version)+"'"
    # version_info = database.querydb(db, sql)
    # if len(version_info) != 0:
    #     version_id = version_info[0][0]
    #     files = version_info[0][12]
    #     print("+++++++++++++++++++++++++version_id:" +str(version_id))
    #     sql = "SELECT * FROM version_types WHERE version_id = " + str(version_id)
    #     types = database.querydb(db, sql)
    #     for t in types:
    #         if t[2] == _type:
    #             insert_project_lib_usage(project_id, t[0], module_)
    #             return
    # else:
    library_version = requests.get(version_url, headers=headers)
    page = library_version.text
    library_soup = BeautifulSoup(library_version.text, 'lxml');
    category_url = None
    if library_soup.find('h2', class_='im-title') is None:
        print("can't find h2 'im-title' class")
        return
    titles = library_soup.find('h2', class_='im-title').find_all('a')
    if titles[len(titles) - 1].get_text() == version:
        if len(titles) - 2 >= 0:
            category_url = "https://mvnrepository.com"+titles[len(titles) - 2]["href"]
            print("category_url:"+category_url)
    results = library_soup.find('div', class_='im')
    if results is None:
        print("can't find 'im' class")
        return
        # raise (CustomizeException("can't find 'im' class"))
    time.sleep(random.randint(15, 20))
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
    # print('    license:', end="")
    # print(license)
    # print('    categories:', end="")
    # print(categories)
    # print('    organization:', end="")
    # print(organization)
    # print('    home_page:', end="")
    # print(home_page)
    # print('    date:', end="")
    # print(date)
    # print('    files:', end="")
    # print(files)
    # print('    repository:', end="")
    # print(repository)
    # print('    used_by:', end="")
    # print(used_by)
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

    entry_dic["library_version"] = library_version_dic
    # version_id = insert_library_version(group, name1, version1, version_url, license, categories, organization, home_page, date,
    #                    files, repository, used_by, page, category_url)
    save_lib_package(files, -1, _type, classifier, project_id, module_)
    if len(entry_dic) != 0:
        project_array.append(entry_dic)
    # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

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
        if groupId is None or artifactId is None or version is None or '${' in groupId or '${' in artifactId or '${' in version:
            print("groupId: " + str(groupId) +"   artifactId: " + str(artifactId)+"   version: " + str(version))
            print(False)
            continue
        if project_id is None:
            continue
        type_ = "jar"
        classifier = None
        if "type" in lib:
            type_ = lib["type"]
        if "classifier" in lib:
            classifier = lib["classifier"]
        if "module" in lib:
            module_ = lib["module"]
        # if not do:
        #     if artifactId == "camel-xmpp-starter" and groupId == "org.apache.camel":
        #         do = True
        #     else:
        #         continue
        # if do:
        global version_type_dic,lib_usage_dic,library_version_dic,entry_dic
        version_type_dic = {}
        lib_usage_dic = {}
        library_version_dic = {}
        entry_dic = {}
        if type(version) == list:
            for ver in version:
                version_type_dic = {}
                lib_usage_dic = {}
                library_version_dic = {}
                entry_dic = {}
                save_version_information(groupId, artifactId, ver, type_, classifier, project_id, module_)
        else:
            save_version_information(groupId, artifactId, version, type_, classifier, project_id, module_)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# save_version_information("org.apache.mina", "mina-integration-beans", "2.0.17", "jar", None,1)
# read_used_library()
# for i in range(179, 1380):
for i in range(1213, 1214):
    # global project_array
    if not os.path.exists(output_path+str(i)+".txt"):
        project_array = []
        get_lib_usedby_project(result_path + str(i) + ".txt")
        # get_lib_usedby_project("C:/Users/yw/Desktop/test/"+str(i)+".txt")
        if len(project_array) != 0:
            with open(output_path + str(i) + ".txt", 'w') as file_object:
                json.dump(project_array, file_object)
# print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
# get_lib_usedby_project(result_path+str(4)+".txt")
