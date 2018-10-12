import os

from exception import CustomizeException
from file_util import read_json, write_json, read_file, get_lib_name, save_lib

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
result_dir = "E:/data/curr_result_all"
repo_dir = "E:/data/repo"

lib_dict = {}

import os

from exception import CustomizeException
from file_util import read_json, write_json, read_file, get_lib_name, save_lib

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
result_dir = "E:/data/curr_result_100_200"
repo_dir = "E:/data/repo_solve"

lib_dict = {}
prev_lib_dic = {}

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
    write_json("more_proj_dependencies1.txt", lib_dict)

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
    write_json("temp.txt", lib_dict)

def combine_more_proj_denpendencies():
    lib_dict = read_json("10.12.txt")
    json_data = read_json("temp.txt")
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
    write_json("10.12.temp.txt", lib_dict)

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
    json_data = read_json(list_path)
    print(len(json_data))
    lib_dic = {}
    for lib_obj in json_data:
        key = lib_obj['lib_name']
        dic_obj = {}
        dic_obj['versions_array'] = lib_obj['versions_array']
        dic_obj['repo_array'] = lib_obj['repo_array']
        lib_dic[key] = dic_obj

    write_json(dic_path, lib_dic)


# get_denpendencies_of_proj(0, 7000)
# lib_dict = read_json("10.12.temp.txt")
# print(len(lib_dict))
# dependency_dict_to_list()
# handle_lib_by_range(1,4)
# more_denpendencies_of_proj(4, 5539)
# more_denpendencies_from_list("unduplicate_proj_dependencies.txt", "C:/Users/yw/Desktop/gradle100_200result.txt")
# more_denpendencies_from_list("8.10.dic.txt", "temp.txt")
# dependency_dict_to_list("8.7.dic.txt","temp.txt")
# combine_more_proj_denpendencies()

# dependency_dict_to_list("combined_proj_dependencies.txt", "test.txt")
# dependency_dict_to_list("10.12.temp.txt", "10.12.txt")
# dependency_list_to_dict("temp.txt","temp.txt")
