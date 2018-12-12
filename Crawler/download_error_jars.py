import json
import os
import random
import sys
import time

import requests
from bs4 import BeautifulSoup

import database
import file_util
from exception import CustomizeException
from file_util import read_json, read_file, write_json


db = database.connectdb()
from useragents import agents
lib_dir = "D:/data/new_update_jar/"

def collect_error_jars():
    count = 0
    result_dic = read_json("result_dic.txt")
    result_list = []
    dir_path = "F:/wangying/update_lib_all_decomplie_10_17"
    decompile_folder_list = os.listdir(dir_path)
    for decompile_folder in decompile_folder_list:
        count += 1
        content_list = os.listdir(os.path.join(dir_path,decompile_folder))
        # print(content_list)
        if len(content_list) == 0:
            print(decompile_folder)
            # jar_url = decompile_folder.replace("_decompile", ".jar")
            # if jar_url not in result_dic:
            #     raise CustomizeException(jar_url)
            # else:
            #     result_list.append(jar_url)
    print(count)
    # print(len(result_list))
    # write_json("list_to_recrawl.txt",result_list)
def repo_in_db():
    repo_list = read_json("repo_list.txt")
    # sql = "SELECT distinct repository from library_versions"
    # query_result = database.querydb(db,sql)
    # print(len(query_result))
    # # print(query_result)
    # for entry in query_result:
    #     repository = entry[0]
    #     repo_list.append(repository)
    # write_json("repo_list.txt", repo_list)
    # print(len(repo_list))
        # if repository not in repo_list:
        #     print(repository)

def read_crawled_list():
    temp = []
    repo_dic = read_json("repo_dic.txt")
    repo_list = read_json("repo_list.txt")
    count = 0
    dir_path = "F:/wangying/2018-8-16-updated-jars/output/result"
    result_list = os.listdir(dir_path)
    old_new_dic = read_json("old_new_dic.txt")
    for result in result_list:
        lines = read_file(os.path.join(dir_path,result))
        for line in lines:
            count += 1
            lib_tuple = tuple(eval(line))
            repository = lib_tuple[6]
            if repository in repo_dic:
                repository = repo_dic[repository]
            if repository not in repo_list:
                if repository not in temp:
                    print(repository)
                    temp.append(repository)
            # print(line)
            # if line in old_new_dic:

    print(count)

    # for result in result_list:
    #     lines = read_file(os.path.join(dir_path,result))
    #     for line in lines:
    #         count += 1
    #         line_tuple = tuple(eval(line))
    #         jar_url = line_tuple[7]
    #         print(jar_url)
    #         if jar_url not in result_dic:
    #             new_array = []
    #             new_array.append(line_tuple)
    #             result_dic[jar_url] = new_array
    #         else:
    #             result_dic[jar_url].append(line_tuple)
    # print(len(result_dic))
    # print(count)
    # write_json("result_dic.txt",result_dic)

def read_result_dic():
    count = 0
    result_dic = read_json("result_dic.txt")
    for key in result_dic.keys():
        count += len(result_dic[key])
    print(count)

def add_left_jars_to_decompile():
    count = 0
    lib_dir = "F:/wangying/lib_all"
    decompile_dir = "F:/wangying/lib_all_decompile_10_17"
    jar_list = os.listdir(lib_dir)
    for jar_name in jar_list:
        decompile_path = jar_name.replace(".jar", "_decompile")
        if decompile_path.endswith(".jar"):
            if not os.path.exists(os.path.join(decompile_dir,decompile_path)):
                print(jar_name)
                count +=1
    print(count)

def collect_jar_to_crawl(a,b):
    uncrawled_path = lib_dir + "2uncrawled_lib.txt"

    repo_dic = read_json("repo_dic.txt")
    result_dic = read_json("result_dic.txt")
    json_data = read_json("list_to_recrawl.txt")
    for i in range(a, b):
        jar_url = json_data[i]
    # for jar_url in json_data:
        print(str(i) + "  " +jar_url)
        lib_array = result_dic[jar_url]
        for lib in lib_array:
            print(lib)
            groupId = lib[0]
            artifactId = lib[1]
            version = lib[2]
            _type = lib[3]
            classifier = lib[4]
            repo_url = lib[6]
            if repo_url not in repo_dic:
                raise CustomizeException(repo_url)

            if _type != "jar" and _type != "test-jar":
                return

            if version.endswith("-SNAPSHOT"):
                with open(uncrawled_path, "a") as f:
                    f.write(str(lib) + "\n")
                f.close()
                return

            version_url = "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId + "/" + version
            time.sleep(random.randint(2, 5))
            headers = {'User-Agent': random.choice(agents)}
            print(version_url)
            library_version = requests.get(version_url, headers=headers, verify=False)
            if library_version.status_code == 403:
                print("Exception status 403:" + version_url)
                os._exit(0)
            library_soup = BeautifulSoup(library_version.text, 'lxml');

            results = library_soup.find('div', class_='im')
            if results is None:
                print("can't find 'im' class")
                with open(uncrawled_path, "a") as f:
                    f.write(str(lib) + "\n")
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
                    f.write(str(lib) + "\n")
                f.close()
            else:
                new_tuple = (groupId, artifactId, version, _type, classifier, date, repository, package_url)
                with open(lib_dir +"1result.txt", "a") as f:
                    f.write("=====" + str(lib) + "\n")
                    f.write(str(new_tuple) + "\n")
                f.close()

def save_lib_package(files, _type, classifier,version):
    file_list = json.loads(files)
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
                return file_util.get_lib_name(package_url)
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
        if page.status_code == 403:
            print("Exception status 403:" + path)
            os._exit(0)
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
                    file_util.save_lib(url, lib_dir + lib_package)
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
                    file_util.save_lib(url, lib_dir + lib_package)
                success = True
                break
    return success, package_url

def get_index():
    json_data = read_json("list_to_recrawl.txt")
    print(len(json_data))
    # for i in range(0, len(json_data)):
    #     jar_url = json_data[i]
    #     if jar_url == "cdk-morphlines-tika-core-0.4.0.jar":
    #         print(i)

def recrawl_lib_to_list():
    count = 0
    repo_dic = read_json("repo_dic.txt")
    result_dic = read_json("result_dic.txt")
    json_data = read_json("list_to_recrawl.txt")
    for i in range(0, len(json_data)):
        jar_url = json_data[i]
        # for jar_url in json_data:
        print(str(i) + "  " + jar_url)
        lib_array = result_dic[jar_url]
        count += len(lib_array)
        # for lib in lib_array:
        #     print(lib)
        #     groupId = lib[0]
        #     artifactId = lib[1]
        #     version = lib[2]
        #     _type = lib[3]
        #     classifier = lib[4]
        #     repo_url = lib[6]
    print(count)

def old_new_jar_dic():
    old_new_dic = {}
    lines = read_file("D:/data/new_update_jar/1result.txt")
    print(len(lines))
    old_tuple = None
    new_tuple = None
    for line in lines:
        if line.startswith("====="):
            old_tuple = str(tuple(eval(line[5:])))
        else:
            if old_tuple != line:
                old_new_dic[old_tuple] = line
    print(len(old_new_dic))
    print(old_new_dic)
    write_json("old_new_dic.txt",old_new_dic)


# collect_error_jars()
# repo_in_db()
# read_crawled_list()
# read_result_dic()
# add_left_jars_to_decompile()

# numa = int(sys.argv[1])
# numb = int(sys.argv[2])
# collect_jar_to_crawl(numa,numb)
# get_index()
# recrawl_lib_to_list()

# lines = read_file("D:/data/new_update_jar/2uncrawled_lib.txt")
# print(len(lines))
# old_new_jar_dic()
