import os
import shutil

import database

from exception import CustomizeException
from file_util import read_json, write_json, read_file, get_lib_name, save_lib

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
result_dir = "E:/data/curr_result_100_200_gradle_maven"
repo_dir = "D:/data/repo"

lib_dict = {}
prev_lib_dic = {}
db = database.connectdb()

def get_denpendencies_of_proj(start_id,end_id):
    for project_id in range(start_id, end_id):
        path = result_dir + "/" +str(project_id) + ".txt"
        if not os.path.exists(path):
            continue
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
            if "groupId" not in lib or "artifactId" not in lib or "version" not in lib or "type" not in lib:
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

            if type(version) == list:
                continue
            else:
                key = groupId + " " + artifactId
                value = version + " " + type_
                if classifier is not None:
                    value += " " + classifier
                if key in lib_dict.keys():
                    versions_array = lib_dict[key]['versions_array']
                    repo_array = lib_dict[key]['repo_array']
                    if value not in versions_array:
                        versions_array.append(value)
                    repo_file = repo_dir + "/" + str(project_id) + ".txt"
                    if os.path.exists(repo_file):
                        print("exists path " + str(project_id))
                        lines = read_file(repo_file)
                        for i in range(len(lines)):
                            repo_url = lines[i]
                            if not repo_url.startswith("https://") and not repo_url.startswith("http://"):
                                repo_url = "http://" + repo_url
                            if repo_url not in repo_array:
                                repo_array.append(repo_url)
                else:
                    lib_obj = {}
                    versions_array = []
                    versions_array.append(value)
                    lib_obj['versions_array'] = versions_array
                    repo_array = []
                    repo_file = repo_dir + "/" + str(project_id) + ".txt"
                    if os.path.exists(repo_file):
                        print("exists path " + str(project_id))
                        lines = read_file(repo_file)
                        for i in range(len(lines)):
                            repo_url = lines[i]
                            if not repo_url.startswith("https://") and not repo_url.startswith("http://"):
                                repo_url = "http://" + repo_url
                            repo_array.append(repo_url)
                    lib_obj['repo_array'] = repo_array
                    lib_dict[key] = lib_obj
    write_json("unduplicate_proj_dependencies3.txt", lib_dict)

def more_denpendencies_of_proj(start_id,end_id):
    global prev_lib_dic
    prev_lib_dic = read_json("unduplicate_proj_dependencies.txt")
    for project_id in range(start_id, end_id):
        path = result_dir + "/" +str(project_id) + ".txt"
        if not os.path.exists(path):
            continue
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
            if "groupId" not in lib or "artifactId" not in lib or "version" not in lib or "type" not in lib:
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

            if type(version) == list:
                continue
            else:
                key = groupId + " " + artifactId
                value = version + " " + type_
                if classifier is not None:
                    value += " " + classifier
                if key in prev_lib_dic.keys():
                    versions_array = prev_lib_dic[key]['versions_array']
                    if value in versions_array:
                        continue
                if key in lib_dict.keys():
                    versions_array = lib_dict[key]['versions_array']
                    repo_array = lib_dict[key]['repo_array']
                    if value not in versions_array:
                        versions_array.append(value)
                    repo_file = repo_dir + "/" + str(project_id) + ".txt"
                    if os.path.exists(repo_file):
                        print("exists path " + str(project_id))
                        lines = read_file(repo_file)
                        for i in range(len(lines)):
                            repo_url = lines[i]
                            if not repo_url.startswith("https://") and not repo_url.startswith("http://"):
                                repo_url = "http://" + repo_url
                            if repo_url not in repo_array:
                                repo_array.append(repo_url)
                else:
                    lib_obj = {}
                    versions_array = []
                    versions_array.append(value)
                    lib_obj['versions_array'] = versions_array
                    repo_array = []
                    repo_file = repo_dir + "/" + str(project_id) + ".txt"
                    if os.path.exists(repo_file):
                        print("exists path " + str(project_id))
                        lines = read_file(repo_file)
                        for i in range(len(lines)):
                            repo_url = lines[i]
                            if not repo_url.startswith("https://") and not repo_url.startswith("http://"):
                                repo_url = "http://" + repo_url
                            repo_array.append(repo_url)
                    lib_obj['repo_array'] = repo_array
                    lib_dict[key] = lib_obj
    write_json("more_proj_dependencies4.txt", lib_dict)

def more_denpendencies_from_list(origin_path,list_path):
    prev_lib_dic = read_json(origin_path)
    json_data = read_json(list_path)
    for lib_obj in json_data:
        key = lib_obj['lib_name']
        versions = lib_obj['versions_array']
        repos = lib_obj['repo_array']
        for value in versions:
            if key in prev_lib_dic.keys():
                versions_array = prev_lib_dic[key]['versions_array']
                if value in versions_array:
                    continue
            if key in lib_dict.keys():
                versions_array = lib_dict[key]['versions_array']
                repo_array = lib_dict[key]['repo_array']
                if value not in versions_array:
                    versions_array.append(value)
                for repo_url in repos:
                    if not repo_url.startswith("https://") and not repo_url.startswith("http://"):
                        repo_url = "http://" + repo_url
                    if repo_url not in repo_array:
                        repo_array.append(repo_url)
            else:
                lib_obj = {}
                versions_array = []
                versions_array.append(value)
                lib_obj['versions_array'] = versions_array
                repo_array = []
                for repo_url in repos:
                    if not repo_url.startswith("https://") and not repo_url.startswith("http://"):
                        repo_url = "http://" + repo_url
                    if repo_url not in repo_array:
                        repo_array.append(repo_url)
                lib_obj['repo_array'] = repo_array
                lib_dict[key] = lib_obj
    # write_json("more_proj_dependencies2.txt", lib_dict)
    write_json("12.21.temp.txt", lib_dict)

def combine_more_proj_denpendencies():
    lib_dict = read_json("10.15.txt")
    json_data = read_json("10.15.temp.txt")
    for key in json_data.keys():
        versions = json_data[key]['versions_array']
        repos = json_data[key]['repo_array']
        for value in versions:
            if key in lib_dict.keys():
                versions_array = lib_dict[key]['versions_array']
                repo_array = lib_dict[key]['repo_array']
                if value not in versions_array:
                    versions_array.append(value)
                for repo_url in repos:
                    if not repo_url.startswith("https://") and not repo_url.startswith("http://"):
                        repo_url = "http://" + repo_url
                    if repo_url not in repo_array:
                        repo_array.append(repo_url)
            else:
                lib_obj = {}
                versions_array = []
                versions_array.append(value)
                lib_obj['versions_array'] = versions_array
                repo_array = []
                for repo_url in repos:
                    if not repo_url.startswith("https://") and not repo_url.startswith("http://"):
                        repo_url = "http://" + repo_url
                    if repo_url not in repo_array:
                        repo_array.append(repo_url)
                lib_obj['repo_array'] = repo_array
                lib_dict[key] = lib_obj
    write_json("10.15.temp.txt", lib_dict)

def dependency_dict_to_list(dic_path,list_path):
    json_data = read_json(dic_path)
    print(len(json_data))
    lib_list = []
    for key in json_data:
        lib_obj = {}
        lib_obj['lib_name'] = key
        lib_obj['versions_array'] = json_data[key]['versions_array']
        lib_obj['repo_array'] = json_data[key]['repo_array']
        lib_list.append(lib_obj)
    write_json(list_path, lib_list)

def dependency_list_to_dict(list_path,dic_path):
    count = 0
    json_data = read_json(list_path)
    print(len(json_data))
    lib_dic = {}
    for lib_obj in json_data:
        key = lib_obj['lib_name']
        dic_obj = {}
        dic_obj['versions_array'] = lib_obj['versions_array']
        if 'repo_array' not in lib_obj:
            dic_obj['repo_array'] = []
        else:
            dic_obj['repo_array'] = lib_obj['repo_array']
        lib_dic[key] = dic_obj
    write_json(dic_path, lib_dic)

def get_denpendencies_of_commit_of_proj():
    id_list = []
    sql = "select * from project where stars > 500"
    query_result = database.querydb(db,sql)
    for proj in query_result:
        id = proj[0]
        id_list.append(id)
    print(id_list)
    print(len(id_list))
    # return
    dir  = "D:/data/result"
    file_list = os.listdir(dir)
    for file in file_list:
        proj_id = int(file.split("_")[0])
        if proj_id not in id_list:
            # print(proj_id)
            continue
        # if file.startswith("32_"):
        #    continue
        print("++++++++++++++ "+file)
        data = read_json(os.path.join(dir,file))
    # for project_id in range(start_id, end_id):
    #     path = result_dir + "/" +str(project_id) + ".txt"
    #     if not os.path.exists(path):
    #         continue
    #     print()
    #     data = read_json(path)
        project_id = None
        module_ = None
        do = False
        for lib in data:
            if 'id' in lib:
                project_id = lib["id"]
                print("-------------------- project_id: " + str(project_id))
                continue
            if "groupId" not in lib or "artifactId" not in lib or "version" not in lib or "type" not in lib:
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

            if type(version) == list:
                continue
            else:
                key = groupId + " " + artifactId
                value = version + " " + type_
                if classifier is not None:
                    value += " " + classifier
                if key in lib_dict.keys():
                    versions_set = lib_dict[key]['versions_set']
                    repo_set = lib_dict[key]['repo_set']
                    versions_set.add(value)
                    repo_file = repo_dir + "/" + str(project_id) + ".txt"
                    if os.path.exists(repo_file):
                        print("exists path " + str(project_id))
                        lines = read_file(repo_file)
                        for i in range(len(lines)):
                            repo_url = lines[i]
                            if not repo_url.startswith("https://") and not repo_url.startswith("http://"):
                                repo_url = "http://" + repo_url
                            repo_set.add(repo_url)
                else:
                    lib_obj = {}
                    versions_set = set()
                    versions_set.add(value)
                    lib_obj['versions_set'] = versions_set
                    repo_set = set()
                    repo_file = repo_dir + "/" + str(project_id) + ".txt"
                    if os.path.exists(repo_file):
                        print("exists path " + str(project_id))
                        lines = read_file(repo_file)
                        for i in range(len(lines)):
                            repo_url = lines[i]
                            if not repo_url.startswith("https://") and not repo_url.startswith("http://"):
                                repo_url = "http://" + repo_url
                            repo_set.add(repo_url)
                    lib_obj['repo_set'] = repo_set
                    lib_dict[key] = lib_obj
    write_json("unduplicate_proj_dependencies5.txt", lib_dict)

def dereplication():
    old_lines = read_file("C:/Users/yw/Desktop/commit_pom/unsolved_cmd1.txt")
    print(len(old_lines))
    old_dic = set(old_lines)
    print(len(old_dic))
    new_lines = read_file("C:/Users/yw/Desktop/commit_pom/unsolved_cmd.txt")
    print(len(new_lines))
    new_dic = set(new_lines)
    print(len(new_dic))
    result = old_dic | new_dic
    print(len(result))
    write_json("C:/Users/yw/Desktop/commit_pom/unsolved_cmd_merge.txt",list(result))

def get_denpendencies_of_500():
    id_list = []
    sql = "select * from project where stars > 500 and stars <= 1000"
    query_result = database.querydb(db, sql)
    for proj in query_result:
        id = proj[0]
        id_list.append(id)
    print(id_list)
    print(len(id_list))
    # return
    dir = "H:/RQ2-data/result_merge_maven"
    file_list = os.listdir(dir)
    for file in file_list:
        proj_id = int(file.replace(".txt", ""))
        print(proj_id)
        if proj_id not in id_list or proj_id == 85:
            # print(proj_id)
            continue
        # if file.startswith("32_"):
        #    continue
        print("++++++++++++++ " + file)
        data = read_json(os.path.join(dir, file))
        data = data["dependency"]
        project_id = proj_id
        module_ = None
        do = False
        for lib in data:
            if "groupId" not in lib or "artifactId" not in lib or "version" not in lib or "type" not in lib:
                print(False)
                continue
            groupId = lib["groupId"]
            artifactId = lib["artifactId"]
            version = lib["version"]
            type_ = lib["type"]
            if groupId is None or artifactId is None or version is None or type_ is None or '${' in groupId or '${' in artifactId or '${' in version or '${' in type_:
                print("groupId: " + str(groupId) + "   artifactId: " + str(artifactId) + "   version: " + str(
                    version) + "   type: " + str(type_))
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

            if type(version) == list:
                continue
            else:
                key = groupId + " " + artifactId
                value = version + " " + type_
                if classifier is not None:
                    value += " " + classifier
                if key in lib_dict.keys():
                    versions_set = lib_dict[key]['versions_set']
                    repo_set = lib_dict[key]['repo_set']
                    versions_set.add(value)
                    repo_file = repo_dir + "/" + str(project_id) + ".txt"
                    if os.path.exists(repo_file):
                        print("exists path " + str(project_id))
                        lines = read_file(repo_file)
                        for i in range(len(lines)):
                            repo_url = lines[i]
                            if not repo_url.startswith("https://") and not repo_url.startswith("http://"):
                                repo_url = "http://" + repo_url
                            repo_set.add(repo_url)
                else:
                    lib_obj = {}
                    versions_set = set()
                    versions_set.add(value)
                    lib_obj['versions_set'] = versions_set
                    repo_set = set()
                    repo_file = repo_dir + "/" + str(project_id) + ".txt"
                    if os.path.exists(repo_file):
                        print("exists path " + str(project_id))
                        lines = read_file(repo_file)
                        for i in range(len(lines)):
                            repo_url = lines[i]
                            if not repo_url.startswith("https://") and not repo_url.startswith("http://"):
                                repo_url = "http://" + repo_url
                            repo_set.add(repo_url)
                    lib_obj['repo_set'] = repo_set
                    lib_dict[key] = lib_obj
        if not os.path.exists("H:/RQ2-data/result_merge_gradle_id/"+str(project_id)+".txt"):
            continue
        content = read_json("H:/RQ2-data/result_merge_gradle_id/"+str(project_id)+".txt")
        print("result_merge_gradle_id : " + "H:/RQ2-data/result_merge_gradle_id/"+str(project_id)+".txt")
        for key in content.keys():
            if key != "name":
                data = content[key]
                for lib in data:
                    groupId = lib["groupId"]
                    artifactId = lib["artifactId"]
                    version = lib["version"]
                    type_ = "jar"
                    if groupId is None or artifactId is None or version is None or type_ is None or '${' in groupId or '${' in artifactId or '${' in version or '${' in type_:
                        print("groupId: " + str(groupId) + "   artifactId: " + str(artifactId) + "   version: " + str(
                            version) + "   type: " + str(type_))
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
                    else:
                        key = groupId + " " + artifactId
                        value = version + " " + type_
                        if classifier is not None:
                            value += " " + classifier
                        if key in lib_dict.keys():
                            versions_set = lib_dict[key]['versions_set']
                            repo_set = lib_dict[key]['repo_set']
                            versions_set.add(value)
                        else:
                            lib_obj = {}
                            versions_set = set()
                            versions_set.add(value)
                            lib_obj['versions_set'] = versions_set
                            repo_set = set()
                            lib_obj['repo_set'] = repo_set
                            lib_dict[key] = lib_obj
    for entry in lib_dict.keys():
        lib_obj = lib_dict[entry]
        new_obj = {}
        new_obj['versions_array'] = list(lib_obj['versions_set'])
        new_obj['repo_array'] = list(lib_obj['repo_set'])
        lib_dict[entry] = new_obj
    write_json("unduplicate_proj_dependencies500-1000.txt", lib_dict)

def rename():
    dir = "H:/RQ2-data/result_merge_gradle"
    files = os.listdir(dir)
    for file in files:
        name = "https://github.com/" + file.replace("__fdse__","/").replace(".txt","")
        print(name)
        sql = "select * from project where url = '" + name + "'"
        query_result = database.querydb(db, sql)
        project_id = query_result[0][0]
        shutil.copyfile(os.path.join(dir,file), "H:/RQ2-data/result_merge_gradle_id/"+str(project_id)+".txt")


# get_denpendencies_of_proj(0, 7000)
# lib_dict = read_json("unduplicate_proj_dependencies.txt")
# print(len(lib_dict))
# dependency_dict_to_list()
# handle_lib_by_range(1,4)
# more_denpendencies_of_proj(5000, 7000)
# more_denpendencies_from_list("10.15.dic.txt", "12.21.temp.txt")
# dependency_dict_to_list("12.21.temp.txt","12.21.temp.txt")
# combine_more_proj_denpendencies()

# dependency_dict_to_list("combined_proj_dependencies.txt", "test.txt")
# dependency_list_to_dict("10.15.txt", "10.15.dic.txt")
# dependency_list_to_dict("C:/Users/yw/Desktop/gr
# dereplication()adle_maven100_200result.txt", "10.15.temp.txt")
# get_denpendencies_of_commit_of_proj()
# rename()
get_denpendencies_of_500()
