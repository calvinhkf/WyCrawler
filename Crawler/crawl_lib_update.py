import json
import os
import random
import time

import requests
import sys
import urllib3
from bs4 import BeautifulSoup

# import database
import file_util
from file_util import get_lib_name,save_lib
# from check_time import get_maven_proj_update_within_three_months
# from crawled_library_to_db import in_version_type_table
from exception import CustomizeException
from useragents import agents

lib_update_path = "D:/data/lib_update_gradle_maven_2/"
gradle_lib_update_path = "D:/data/lib_update_gradle_maven_2/"
# db = database.connectdb()
# cursor = db.cursor()
# lib_dir = sys.argv[3]
lib_dir = os.getcwd()+'/lib/'
if not os.path.exists(lib_dir):
    os.makedirs(lib_dir)
# lib_dir = "D:/GP/lib/"
urllib3.disable_warnings()

def read_lib_update_data(a,b):
    update_values = []
    for i in range(a,b):
        path = lib_update_path + str(i) + ".txt"
        if os.path.exists(path):
            print("++++++++++++++++++++++++ "+path)
            lines = file_util.read_file(path)
            for line in lines:
                # print(line)
                value = line.split(" VALUES ")[1]
                try:
                    value = tuple(eval(value.strip()))
                except:
                    continue
                print(value)
                update_values.append(value)
                if len(update_values) == 5000:
                    cursor.executemany(
                        'INSERT INTO lib_update (project_id,file,group_str,name_str,prev_version,curr_version,prev_time,curr_time,prev_commit,curr_commit,remark,type,classifier) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        update_values)
                    db.commit()
                    update_values = []
                    print(5000)
    cursor.executemany(
        'INSERT INTO lib_update (project_id,file,group_str,name_str,prev_version,curr_version,prev_time,curr_time,prev_commit,curr_commit,remark,type,classifier) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        update_values)
    db.commit()

def parse_gradle_lib_update_data():
    gradle_array = get_maven_proj_update_within_three_months(90)
    file_list = os.listdir(gradle_lib_update_path)
    for file in file_list:
        li = file
        path = os.path.join(gradle_lib_update_path, li)
        print(path)
        if li.endswith(".txt"):
            li = li[:-4]
        if li.endswith(".txt"):
            li = li[:-4]
        li = li.replace("__fdse__", "/")
        github_url = "https://github.com/" + li
        # sql = "SELECT * FROM project WHERE url = '" + str(github_url) + "'"
        # query_result = database.querydb(db, sql)
        # if len(query_result) <= 0:
        if github_url not in gradle_array:
            # print("remove")
            os.remove(path)
            # raise CustomizeException("can't find :" + str(github_url))
        else:
            sql = "SELECT * FROM project WHERE url = '" + str(github_url) + "'"
            query_result = database.querydb(db, sql)
            if len(query_result) <= 0:
                raise CustomizeException("can't find "+ str(github_url))
            id = query_result[0][0]
            os.rename(os.path.join(gradle_lib_update_path, file), os.path.join(gradle_lib_update_path, str(id) + ".txt"))
            print(file)
            print(id)

def read_lib_update_data_gradle(a,b):
    update_values = []
    for i in range(a,b):
        path = lib_update_path + str(i) + ".txt"
        if os.path.exists(path):
            print("++++++++++++++++++++++++ "+path)
            lines = file_util.read_file(path)
            for line in lines:
                if "====" in line:
                    continue
                # print(line)
                value = line.split(" VALUES ")[1]
                value = value.replace("(-1,","("+str(i)+",")
                value = value.replace("'')", "'jar', '')")
                # print(value)
                try:
                    value = tuple(eval(value.strip()))
                except:
                    continue
                print(value)
                update_values.append(value)
                if len(update_values) == 5000:
                    cursor.executemany(
                        'INSERT INTO lib_update (project_id,file,group_str,name_str,prev_version,curr_version,prev_time,curr_time,prev_commit,curr_commit,remark,type,classifier) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        update_values)
                    db.commit()
                    update_values = []
                    print(5000)
    cursor.executemany(
        'INSERT INTO lib_update (project_id,file,group_str,name_str,prev_version,curr_version,prev_time,curr_time,prev_commit,curr_commit,remark,type,classifier) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        update_values)
    db.commit()

def read_lib_update_data_gradle(a,b):
    update_values = []
    for i in range(a,b):
        path = lib_update_path + str(i) + ".txt"
        if os.path.exists(path):
            print("++++++++++++++++++++++++ "+path)
            lines = file_util.read_file(path)
            for line in lines:
                if "====" in line:
                    continue
                # print(line)
                value = line.split(" VALUES ")[1]
                value = value.replace("(-1,","("+str(i)+",")
                value = value.replace("'')", "'jar', '')")
                # print(value)
                try:
                    value = tuple(eval(value.strip()))
                except:
                    continue
                print(value)
                in_table = in_lib_update_table(i, value[2], value[3], value[4], value[5], value[11], value[8], value[9])
                print(in_table)
                if not in_table:
                    update_values.append(value)
                    if len(update_values) == 5000:
                        cursor.executemany(
                            'INSERT INTO lib_update (project_id,file,group_str,name_str,prev_version,curr_version,prev_time,curr_time,prev_commit,curr_commit,remark,type,classifier) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            update_values)
                        db.commit()
                        update_values = []
                        print(5000)
    cursor.executemany(
        'INSERT INTO lib_update (project_id,file,group_str,name_str,prev_version,curr_version,prev_time,curr_time,prev_commit,curr_commit,remark,type,classifier) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        update_values)
    db.commit()

def in_lib_update_table(project_id,groupId,artifctId,version1,version2,type_,commit1,commit2):
    sql = "SELECT * FROM lib_update WHERE project_id = "+ str(project_id) +" and group_str = '" + str(groupId) + "' and name_str = '" + str(
        artifctId) + "' and prev_version = '" + str(version1) +"' and curr_version = '" + str(version2) +"' and prev_commit = '" +str(commit1) +"' and curr_commit = '" + str(commit2) +"' and type = '" + str(type_) +"' and classifier is null"
    print(sql)
    result = database.querydb(db, sql)
    if len(result) > 0:
        return True
    return False

def get_libs_in_update():
    output_array = []
    sql = "SELECT distinct group_str,name_str,curr_version,type,classifier FROM lib_update"
    # sql = "SELECT distinct group_str,name_str,prev_version,type,classifier FROM lib_update union SELECT distinct group_str,name_str,curr_version,type,classifier FROM lib_update"
    result = database.querydb(db,sql)
    print(len(result))
    file_util.write_json("jar_to_crawl2.txt",result)
    # for lib in result:
    #     groupId = lib[0]
    #     artifactId = lib[1]
    #     version = lib[2]
    #     type_ = lib[3]
    #     classifier = lib[4]
    #     if '${' in groupId or '${' in artifactId or '${' in version or '${' in type_ or '@' in groupId or '@' in artifactId or '@' in version or '@' in type_:
    #         continue
    #     lib_str = groupId + " " + artifactId + " " + version + " " + type_
    #     if classifier is not None:
    #         if '${' in classifier or '@' in classifier:
    #             continue
    #         lib_str = lib_str + " " + classifier
    #     is_exist = False
    #     sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
    #         artifactId) + "' and version = '" + str(version) + "'"
    #     version_info = database.querydb(db, sql)
    #     if len(version_info) == 1 or len(version_info) == 2:
    #         version_id = version_info[0][0]
    #         type_id = in_version_type_table(version_id, type_, classifier)
    #         if type_id >= 0:
    #             is_exist = True
    #     if not is_exist:
    #         output_array.append()
    # print(sql)

def sort_lib():
    output = []
    result = file_util.read_json("jar_to_crawl2.txt")
    print(len(result))
    for lib in result:
        groupId = lib[0]
        artifactId = lib[1]
        version = lib[2]
        type_ = lib[3]
        classifier = lib[4]
        if '${' in groupId or '${' in artifactId or '${' in version or '${' in type_ or '@' in groupId or '@' in artifactId or '@' in version or '@' in type_:
            continue
        lib_str = groupId + " " + artifactId + " " + version + " " + type_
        if classifier is not None:
            if '${' in classifier or '@' in classifier:
                continue
            lib_str = lib_str + " " + classifier
        output.append(lib_str)
    print(len(output))
    file_util.write_json("lib_to_crawl2.txt", output)

# def combine_lib():
#     lib_array1 = file_util.read_json("lib_to_crawl1.txt")
#     lib_array2 = file_util.read_json("lib_to_crawl2.txt")
#     print(len(lib_array1))
#     print(len(lib_array2))
#     for lib in lib_array2:
#         if lib not in lib_array1:
#             lib_array1.append(lib)
#     print(len(lib_array1))
#     file_util.write_json("jars.txt", lib_array1)

def combine_lib():
    lib_array1 = file_util.read_json("lib_to_crawl1.txt")
    lib_array2 = file_util.read_json("lib_to_crawl2.txt")
    print(len(lib_array1))
    print(len(lib_array2))
    # lib_set1 = set(lib_array1)
    # lib_set2 = set(lib_array2)
    # print(len(lib_set1))
    # print(len(lib_set2))
    lib_array1.extend(lib_array2)
    print(len(lib_array1))
    lib_set = set(lib_array1)
    print(len(lib_set))
    result_lib = list(lib_set)
    file_util.write_json("jars.txt", result_lib)
    # for lib in lib_array2:
    #     if lib not in lib_array1:
    #         lib_array1.append(lib)
    # print(len(lib_array1))
    # file_util.write_json("jars1.txt", lib_array1)

def collect_lib():
    result = file_util.read_json("jars.txt")
    print(len(result))
    output = []
    for lib in result:
        # print(lib)
        temp = lib.split(" ")
        groupId = temp[0]
        artifactId = temp[1]
        version = temp[2]
        type_ = temp[3]
        classifier = None
        if len(temp) == 5:
            classifier = temp[4]
        lib_tuple = (groupId,artifactId,version,type_,classifier)
        # print(lib_tuple)
        is_exist = False
        sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
            artifactId) + "' and version = '" + str(version) + "'"
        version_info = database.querydb(db, sql)
        if len(version_info) == 1 or len(version_info) == 2:
            version_id = version_info[0][0]
            type_id = in_version_type_table(version_id, type_, classifier)
            if type_id >= 0:
                is_exist = True
        if not is_exist:
            print(lib_tuple)
            output.append(lib_tuple)
    print(len(output))
    file_util.write_json("jar_final.txt",output)

def save_lib_package(files, _type, classifier,version):
    file_list = json.loads(files)
    if _type in file_list:
        jar_url = file_list[_type]
        if not os.path.exists(lib_dir + get_lib_name(jar_url)):
            file_util.save_lib(jar_url, lib_dir + get_lib_name(jar_url))
        return get_lib_name(jar_url)
    if _type == "tar.gz" or _type == "zip" or _type == "jar" or _type == "test-jar" or _type == "nbm-file" or _type == "xml" or _type == "war" or _type == "kar" or _type == "swc" or _type == "pom" or _type == "executable-war" or _type == "warpath":
        new_type = _type
        if _type == "nbm-file":
            new_type = "nbm"
        if _type == "executable-war" or _type == "warpath":
            new_type = "war"
        if 'View' in file_list:
            page_url = file_list['View']
            success, package_url = get_lib_from_list_page(page_url, new_type, classifier)
            if success:
                return get_lib_name(package_url)
    else:
        raise (CustomizeException("version:"+str(version)+"classifier:"+str(classifier)+"type:"+str(_type)+"\n!!!!!!!!!!!!!!!!!!!! unhandled type: " + str(_type)))
    return None

def get_lib_from_list_page(page_path, _type, classifier):
    time.sleep(random.randint(2, 5))
    lib_list = get_lib_list_of_one_version(page_path)
    return download_lib_from_list(lib_list, page_path, _type, classifier)

def get_lib_list_of_one_version(path):
    newlist = []
    try:
        time.sleep(random.randint(1, 3))
        headers = {'User-Agent': random.choice(agents)}
        page = requests.get(path, headers=headers, verify=False)
        soup = BeautifulSoup(page.text, 'lxml');
        list = soup.find_all('a')
        for li in list:
            newlist.append(li.get_text())
    except Exception as e:
        print('no use repo: ' + str(path))
    return newlist

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

def get_url():
    print()

def crawl_jar_from_maven(lib_tuple,file):
    uncrawled_path = lib_dir + "2uncrawled_lib.txt"

    groupId = lib_tuple[0]
    artifactId = lib_tuple[1]
    version = lib_tuple[2]
    _type = lib_tuple[3]
    classifier = lib_tuple[4]

    if version.endswith("-SNAPSHOT"):
        with open(uncrawled_path, "a") as f:
            f.write(str(lib_tuple) + "\n")
        f.close()
        return

    version_url = "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId + "/" + version
    time.sleep(random.randint(2, 5))
    headers = {'User-Agent': random.choice(agents)}
    print(version_url)
    library_version = requests.get(version_url, headers=headers, verify=False)
    library_soup = BeautifulSoup(library_version.text, 'lxml');

    results = library_soup.find('div', class_='im')
    if results is None:
        print("can't find 'im' class")
        with open(uncrawled_path, "a") as f:
            f.write(str(lib_tuple) + "\n")
        f.close()
        return
    results = results.find_next_sibling(class_='grid')
    information_trs = results.find_all('tr')
    repository, files = None, None
    for tr in information_trs:
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
    print('    repository:' + str(repository))
    print('    date:' + str(date))
    print('    files:' + str(files))
    package_url = save_lib_package(files, _type, classifier, version)
    if package_url is None:
        with open(uncrawled_path, "a") as f:
            f.write(str(lib_tuple) + "\n")
        f.close()
    else:
        new_tuple = (groupId, artifactId, version, _type, classifier, date, repository, package_url)
        with open(file, "a") as f:
            f.write(str(new_tuple) + "\n")
        f.close()

def crawl_jar_by_range(a,b):
    json_data = file_util.read_json("jar_final.txt")
    print(len((json_data)))
    for i in range(a,b):
        print("++++++++++++++++++++++++++++ " + str(i))
        lib_tuple = json_data[i]
        print(lib_tuple)
        crawl_jar_from_maven(lib_tuple, lib_dir +"1result.txt")

# read_lib_update_data(16, 5600)
# parse_gradle_lib_update_data()
# read_lib_update_data_gradle(16,5600)
# get_libs_in_update()
# combine_lib()
# collect_lib()
a = sys.argv[1]
b = sys.argv[2]
crawl_jar_by_range(int(a), int(b))