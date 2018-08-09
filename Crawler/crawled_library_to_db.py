import json

import os
import random

import requests
import time

import database
from exception import CustomizeException
from bs4 import BeautifulSoup

from file_util import save_lib, get_lib_name, read_json
from handle_jar_db import insert_library_version, db, insert_version_type, insert_project_lib_usage

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

lib_path = "C:/Users/yw/Desktop/lib/"
# result_path ="C:/Users/yw/Desktop/result/"
# output_path ="C:/Users/yw/Desktop/"
crawled_lib_path = "E:/data/dependency_library_info"

def insert_unsolved_library_without_projectid(group,name1,version1,_type,classifier):
    if classifier is None:
        sql = "SELECT * FROM unsolved_libraries WHERE group_str = '" + str(group) + "' and name_str = '" + str(
        name1) +"' and version = '"+str(version1)+"' and type = '"+str(_type)+"' and classifier is NULL"
    else:
        sql = "SELECT * FROM unsolved_libraries WHERE group_str = '" + str(group) + "' and name_str = '" + str(
        name1) +"' and version = '"+str(version1)+"' and type = '"+str(_type)+"' and classifier = '"+str(classifier)+"'"
    record = database.querydb(db, sql)
    if len(record) == 0:
        sql = "INSERT INTO unsolved_libraries" \
              "(group_str,name_str,version,type,classifier) " \
              "VALUES (\'" \
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

def read_crawled_lib_from_file():
    list = os.listdir(crawled_lib_path)
    for i in range(0, len(list)):
        path = os.path.join(crawled_lib_path, list[i])
        print(path)
        if os.path.isfile(path) and path.endswith(".json"):
            lib_str = list[i][:-5]
            print(lib_str)
            lib_array = lib_str.split(" ")
            if len(lib_array) != 2:
                raise CustomizeException("!!!!!!!!!!!!!!! len(lib_array)!= 2 : "+lib_str)
            groupId = lib_array[0]
            artifactId = lib_array[1]
            # print(groupId)
            # print(artifactId)
            json_data = read_json(path)
            library_versions_list = json_data["library_versions_list"]
            unsolved_lib_list = json_data["unsolved_lib_list"]
            version_types_list = json_data["version_types_list"]
            for library_version in  library_versions_list:
                insert_library_version(library_version["group"], library_version["name"], library_version["version"],
                                       library_version["version_url"], library_version["license"],
                                       library_version["categories"], library_version["organization"],
                                       library_version["home_page"],
                                       library_version["date"], library_version["files"], library_version["repository"],
                                       library_version["used_by"], library_version["category_url"])
            for version_type in version_types_list:
                version = version_type["version"]
                _type = version_type["_type"]
                classifier = version_type["classifier"]
                jar_package_url = version_type["jar_package_url"]
                sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
                    artifactId) + "' and version = '" + str(version) + "'"
                version_info = database.querydb(db, sql)
                if len(version_info) != 0:
                    version_id = version_info[0][0]
                    break
                added = False
                sql = "SELECT * FROM version_types WHERE version_id = " + str(version_id)
                types = database.querydb(db, sql)
                for t in types:
                    if t[2] == _type:
                        if (classifier is not None and classifier == t[3]) or (classifier == None and t[3] == None):
                            added = True
                            break
                if not added:
                    version_type_id = insert_version_type(version_id, _type, classifier, jar_package_url)
                # insert_project_lib_usage(project_id, version_type_id, module_)
            for unsolved_lib in unsolved_lib_list:
                insert_unsolved_library_without_projectid(unsolved_lib["group"], unsolved_lib["name"], unsolved_lib["version"], unsolved_lib["_type"], unsolved_lib["classifier"])

def in_unsolved_table(group,name1,version1,_type,classifier):
    if classifier is None:
        sql = "SELECT * FROM unsolved_libraries WHERE group_str = '" + str(group) + "' and name_str = '" + str(
        name1) +"' and version = '"+str(version1)+"' and type = '"+str(_type)+"' and classifier is NULL"
    else:
        sql = "SELECT * FROM unsolved_libraries WHERE group_str = '" + str(group) + "' and name_str = '" + str(
        name1) +"' and version = '"+str(version1)+"' and type = '"+str(_type)+"' and classifier = '"+str(classifier)+"'"
    record = database.querydb(db, sql)
    if len(record) == 0:
        return False
    else:
        return True

def in_version_type_table(version_id,type_,classifier):
    sql = "SELECT * FROM version_types WHERE version_id = " + str(version_id)
    types = database.querydb(db, sql)
    for t in types:
        if t[2] == type_:
            if (classifier is not None and classifier == t[3]) or (classifier == None and t[3] == None):
                return t[0]
    return -1

def project_crawled_lib_usage(path):
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
        if type(version) == list:
            continue
        else:
            sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
                artifactId) + "' and version = '" + str(version) + "'"
            version_info = database.querydb(db, sql)
            version_id = None
            if len(version_info) != 0:
                version_id = version_info[0][0]
            if version_id is None:
                is_in_table = in_unsolved_table(groupId, artifactId, version, type_, classifier)
                if not is_in_table:
                    raise CustomizeException("unrecorded library: "+"groupId: " + str(groupId) + "   artifactId: " + str(artifactId) + "   version: " + str(
                    version) + "   type: " + str(type_) + "   classifier: " + str(classifier))
                else:
                    continue
            version_type_id = in_version_type_table(version_id, type_, classifier)
            if version_type_id < 0:
                is_in_table = in_unsolved_table(groupId, artifactId, version, type_, classifier)
                if not is_in_table:
                    raise CustomizeException("unrecorded library: " + "groupId: " + str(groupId) + "   artifactId: " + str(artifactId) + "   version: " + str(
                            version) + "   type: " + str(type_) + "   classifier: " + str(classifier))
                else:
                    continue
            insert_project_lib_usage(project_id, version_type_id, module_)
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# for i in range(1213, 1214):
#     # global project_array
#     if not os.path.exists(output_path+str(i)+".txt"):
#         project_array = []
#         get_lib_usedby_project(result_path + str(i) + ".txt")
#         # get_lib_usedby_project("C:/Users/yw/Desktop/test/"+str(i)+".txt")
#         if len(project_array) != 0:
#             with open(output_path + str(i) + ".txt", 'w') as file_object:
#                 json.dump(project_array, file_object)
# read_crawled_lib_from_file()
