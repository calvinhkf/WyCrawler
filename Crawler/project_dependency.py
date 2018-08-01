import os

from exception import CustomizeException
from file_util import read_json, write_json, read_file, get_lib_name, save_lib

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
result_dir = "E:/data/curr_result_all"
repo_dir = "E:/data/repo"

lib_dict = {}

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
    write_json("unduplicate_proj_dependencies.txt", lib_dict)

def dependency_dict_to_list():
    json_data = read_json("unduplicate_proj_dependencies.txt")
    lib_list = []
    for key in json_data:
        lib_obj = {}
        lib_obj['lib_name'] = key
        lib_obj['versions_array'] = json_data[key]['versions_array']
        lib_obj['repo_array'] = json_data[key]['repo_array']
        lib_list.append(lib_obj)
    write_json("dependencies_list.txt", lib_list)

def handle_lib_by_range(start,end):
    json_data = read_json("dependencies_list.txt")
    for i in range(start,end):
        handle_one_lib(json_data[i])

def handle_one_lib(lib_obj):
    key = lib_obj['lib_name']
    versions_array = lib_obj['versions_array']
    repo_array = lib_obj['repo_array']
    names = key.split(' ')
    if len(names) != 2:
        raise (CustomizeException("names length != 2"))
    groupId = names[0]
    artifactId = names[1]
    print(groupId + "====" + artifactId)
    for version_info in versions_array:
        values = version_info.split(' ')
        if len(values) != 2 and len(values) != 3:
            raise (CustomizeException("values length != 2 or 3:" + str(version_info)))
        version = values[0]
        type_ = values[1]
        classifier = None
        if len(values) == 3:
            classifier = values[2]
        print(version + "====" + type_ + "====" + str(classifier))


# get_denpendencies_of_proj(4,5539)
# get_denpendencies_of_proj(4, 5539)
# print(len(lib_dict))
# dependency_dict_to_list()
# handle_lib_by_range(1,4)
