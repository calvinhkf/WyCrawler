import os
import sys
import database
from exception import CustomizeException

from file_util import read_json, write_json, read_file


def merge_project_call():
    dir = "E:/project_call/8_admin/call"
    file_list = os.listdir(dir)
    curr_id = None
    call_list = []
    for file in file_list:
        print(file)
        project_id = int(file.split("_")[0])
        if project_id == 2979:
            continue
        # if project_id == 2979 or project_id == 2944 or project_id == 271 or project_id == 565 or project_id == 1198 or project_id == 1238 or project_id == 1304 or project_id == 613:
        #     continue
        content = read_json(os.path.join(dir,file))
        if content is None:
            continue
        new_list = content[:-1]
        if curr_id is None:
            curr_id = project_id
            call_list.extend(new_list)
        elif curr_id != project_id:
            # if curr_id == 3755:
            #     print(call_list)
            write_json("E:/project_call/total/" + str(curr_id) + ".txt", call_list)
            curr_id = None
            call_list = []
        else:
            call_list.extend(new_list)
    print(call_list)
    write_json("E:/project_call/total/" + str(curr_id) + ".txt", call_list)

def filter_test_code():
    array = ["0_fdse", "1_Thinkpad", "2_11", "3_lj", "4_zfy", "5_ZW", "6_Thinkpad", "7_huangkaifeng", "8_admin", "9_huangkaifeng"]
    # array = ["1_Thinkpad", "2_11", "3_lj", "4_zfy", "5_ZW", "6_Thinkpad", "7_huangkaifeng", "8_admin",
    #          "9_huangkaifeng"]
    # array = [ "8_admin", "9_huangkaifeng"]
    for machine_str in array:
        dir = "E:/project_call/" + machine_str + "/call"
        # print(dir)
        file_list = os.listdir(dir)
        curr_id = None
        proj_content = {}
        for file in file_list:
            file_array = file.replace(".txt", "").split("_")
            project_id = file_array[0]
            if project_id not in ["3162", "4859", "2955"]:
                continue
            print(file)
            file_id = file_array[1]
            file_paths = read_json("F:/RQ1/file_path/" + str(project_id) + ".json")
            path = file_paths[file_id]
            if "\\src\\test\\" in path:
                continue
            # print(path)
            json_data = read_json(os.path.join(dir, file))
            # print(json_data)
            num = json_data[-1]
            json_data = json_data[:-1]
            # print(json_data)
            new_list = []
            for call in json_data:
                new_call = preprocess(call)
                new_list.append(new_call)
            new_list.append(num)
            # print(new_list)
            # write_json("E:/project_call/total_preprocessed_exclude_test/" + file, new_list)
            if curr_id is None:
                curr_id = project_id
                # if len(new_list) > 0:
                proj_content[file_id] = new_list
            elif curr_id != project_id:
                if os.path.exists("E:/project_call/total_preprocessed_exclude_test/" + str(curr_id) + ".txt"):
                    raise CustomizeException("repeat project id:" + curr_id)
                    sys.exit(0)
                write_json("E:/project_call/total_preprocessed_exclude_test/" + str(curr_id) + ".txt", proj_content)
                curr_id = project_id
                proj_content = {}
                proj_content[file_id] = new_list
            else:
                proj_content[file_id] = new_list
        if os.path.exists("E:/project_call/total_preprocessed_exclude_test/" + str(curr_id) + ".txt"):
            raise CustomizeException("repeat project id:" + curr_id)
            sys.exit(0)
        write_json("E:/project_call/total_preprocessed_exclude_test/" + str(curr_id) + ".txt", proj_content)

    #     content = read_json(os.path.join(dir, file))
    #     if content is None:
    #         continue
    #     new_list = content[:-1]
    #     if curr_id is None:
    #         curr_id = project_id
    #         call_list.extend(new_list)
    #     elif curr_id != project_id:
    #         write_json("E:/project_call/total_exclude_test/" + str(curr_id) + ".txt", call_list)
    #         curr_id = None
    #         call_list = []
    #     else:
    #         call_list.extend(new_list)
    # print(call_list)
    # write_json("E:/project_call/total/" + str(curr_id) + ".txt", call_list)

def extract_api_call_by_file():
    ssd_dir = "G:/"
    dir = "E:/project_call/total_preprocessed_exclude_test1"
    file_list = os.listdir(dir)
    for file in file_list:
        if os.path.exists("E:/project_call/api_call_exclude_test/" + file):
            continue
        print("+++++++++++++++++++++++++++++++" + file)
        project_api_call = {}
        project_id = int(file.replace(".txt", ""))
        calls_by_file = read_json(os.path.join(dir, file))
        lib_list = read_json("C:/lib_list/" + str(project_id) + ".json")
        for lib in lib_list:
            jar_dic = {}
            print(lib)
            if os.path.exists(ssd_dir + "RQ1-data/RQ1_Lib APIs/preprocessed_api/" + lib + ".json"):
                json_data = read_json(ssd_dir + "RQ1-data/RQ1_Lib APIs/preprocessed_api/" + lib + ".json")
                for file_id in calls_by_file.keys():
                    file_dic = {}
                    calls = calls_by_file[file_id][:-1]
                    # print(calls)
                    # print(calls_by_file[file_id])
                    for call in calls:
                        call = call.replace(" ", "").replace("$", ".")
                        for class_name in json_data.keys():
                            api_list = json_data[class_name][:-1]
                            if api_list is not None and call in api_list:
                                if call in file_dic:
                                    api_dic = file_dic[call]
                                    api_dic["count"] = api_dic["count"] + 1
                                else:
                                    api_dic = {}
                                    api_dic["count"] = 1
                                    api_dic["class"] = class_name
                                    file_dic[call] = api_dic
                                break
                    if len(file_dic) > 0:
                        jar_dic[file_id] = file_dic
            if len(jar_dic) > 0:
                project_api_call[lib] = jar_dic
        write_json("E:/project_call/api_call_exclude_test/" + file, project_api_call)

def check_project_length():
    # id = 258
    # data = read_json("E:/project_call/total_preprocessed_exclude_test/" + str(id) + ".txt")
    # print(len(data))
    # projs = set()
    # array = ["0_fdse", "1_Thinkpad", "2_11", "3_lj", "4_zfy", "5_ZW", "6_Thinkpad", "7_huangkaifeng", "8_admin",
    #          "9_huangkaifeng"]
    # for machine_str in array:
    #     dir = "E:/project_call/" + machine_str + "/call"
    #     # print(dir)
    #     file_list = os.listdir(dir)
    #     for file in file_list:
    #         print(file)
    #         file_array = file.replace(".txt", "").split("_")
    #         project_id = file_array[0]
    #         projs.add(project_id)
    # print(len(projs))
    # print(projs)
    # write_json("pj_exclude_test.txt", list(projs))
    # for pj in projs:
    #     if not os.path.exists("E:/project_call/total_preprocessed_exclude_test/" + str(pj) + ".txt"):
    #         print(pj)

    file_paths = read_json("F:/RQ1/file_path/4.json")

    machine_str = "0_fdse"
    dir = "E:/project_call/" + machine_str + "/call"
    file_list = os.listdir(dir)
    count = 0
    for file in file_list:
        # print(file)
        file_array = file.replace(".txt", "").split("_")
        project_id = file_array[0]
        file_id = file_array[1]
        if project_id == "4":
            path = file_paths[file_id]
            if "\\src\\test\\" in path:
                continue
            count += 1
    print(count)
    data = read_json("E:/project_call/total_preprocessed_exclude_test1/4.txt")
    print(len(data))

def project_num():
    ids = set()
    dir = "E:/project_call"
    dirs = os.listdir(dir)
    for file_dir in dirs:
        if file_dir != "total" and file_dir != "new":
            path = "E:/project_call/" + file_dir + "/call"
            file_list = os.listdir(path)
            for file in file_list:
                print(file)
                project_id = int(file.split("_")[0])
                ids.add(project_id)
    print(len(ids))
    dir = "E:/project_call/total"
    array = os.listdir(dir)
    com = set()
    for entry in array:
        project_id = int(entry.replace(".txt", ""))
        com.add(project_id)
    for id in ids:
        if id not in com:
            print(id)

def extract_commit_api_call():
    total_count = 0
    error_count = 0
    commit_update_call_dir = "F:/"
    lib_file_dir = "G:/"
    dir = commit_update_call_dir +"commit_update_call/result/60/call_8"
    if not os.path.exists(dir + "/result"):
        os.mkdir(dir + "/result")
    file_list = os.listdir(dir)
    for file in file_list:
        if not file.endswith(".txt"):
            continue
        print("+++++++++++++++++++++++++++++++" + file)
        project_api_call = {}
        temp = file.replace(".txt", "").split("_")
        project_id = int(temp[0])
        commit = temp[1]
        calls = []
        lines = read_file(os.path.join(dir, file))
        for line in lines:
    #         one_num = list(eval(line))[-2]
    #         # print(one_num)
    #         temp = one_num.split(" ")
    #         error_count += int(temp[0])
    #         total_count += int(temp[1])
    # print(error_count)
    # print(total_count)
    # print(error_count/total_count)
            one_list = list(eval(line))[:-2]
            # print(one_list)
            for each in one_list:
                new_call = preprocess(each)
                calls.append(new_call)
        commit_dic = read_json(commit_update_call_dir + "commit_update_call/proj_update_lib/" + str(project_id) + ".txt")
        if commit in commit_dic:
            lib_dic = commit_dic[commit]
            for key in lib_dic.keys():
                lib = lib_dic[key]
                print(lib)
                api_list = get_api_list_of_lib(lib, lib_file_dir)
                if api_list is not None:
                    # print(api_list)
                    api_call_dic = {}
                    for call in calls:
                        call = call.replace(" ", "")
                        if call in api_list:
                            if call in api_call_dic:
                                api_call_dic[call] = api_call_dic[call] + 1
                            else:
                                api_call_dic[call] = 1
                    if len(api_call_dic) > 0:
                        project_api_call[lib] = api_call_dic
        write_json(dir + "/result/" + file, project_api_call)

def extract_api_call():
    dir = "E:/project_call/new"
    file_list = os.listdir(dir)
    for file in file_list:
        if os.path.exists("E:/project_call/api_call/" + file):
            continue
        print("+++++++++++++++++++++++++++++++" + file)
        project_api_call = {}
        project_id = int(file.replace(".txt", ""))
        calls = read_json(os.path.join(dir, file))
        lib_list = read_json("C:/lib_list/" + str(project_id) + ".json")
        for lib in lib_list:
            print(lib)
            api_list = get_api_list_of_lib(lib, "F:/")
            if api_list is not None:
                # print(api_list)
                api_call_dic = {}
                for call in calls:
                    call = call.replace(" ", "")
                    if call in api_list:
                        if call in api_call_dic:
                            api_call_dic[call] = api_call_dic[call] + 1
                        else:
                            api_call_dic[call] = 1
                if len(api_call_dic) > 0:
                    project_api_call[lib] = api_call_dic
        write_json("E:/project_call/api_call/" + file, project_api_call)

def get_api_list_of_lib(lib, dir_path):
    # dir_path = "F:/"
    json_data = None
    if os.path.exists(dir_path + "RQ1-data/RQ1_Lib APIs/LibToFieldsAll/lib_field/" + lib + ".json"):
        json_data = read_json(dir_path + "RQ1-data/RQ1_Lib APIs/LibToFieldsAll/lib_field/" + lib + ".json")
    elif os.path.exists(dir_path + "RQ1-data/RQ1_Lib APIs/lib_fieldaaa/" + lib + ".json"):
        json_data = read_json(dir_path + "RQ1-data/RQ1_Lib APIs/lib_fieldaaa/" + lib + ".json")
    if json_data is not None:
        api_list = set()
        for clazz in json_data:
            class_name = clazz["className"].replace("$", ".")
            fields = clazz["fields"]
            for field in fields:
                api = class_name + "." + field["fieldName"]
                api_list.add(api)
                # print(api)
            methods = clazz["methods"]
            for method in methods:
                # print(method)
                method = method.replace("$", ".")
                index = method.find(": ")
                new_method = method[index + 2:]
                new_method = new_method[new_method.find(" ") + 1:-1]
                api = method[1:index] + "." + new_method
                api_list.add(api)
                # print(api)
    else:
        return None
    return api_list

def lib_api_preprocess():
    dir = "G:/RQ1-data/RQ1_Lib APIs/LibToFieldsAll/lib_field"
    files = os.listdir(dir)
    for file in files:
        print(file)
        if os.path.exists("G:/RQ1-data/RQ1_Lib APIs/preprocessed_api/" + file):
            continue
        api_dic = {}
        json_data = read_json(os.path.join(dir, file))
        if json_data is not None:
            class_names = set()
            for clazz in json_data:
                class_names.add(clazz["className"])
            for clazz in json_data:
                # print(clazz["className"])
                class_name = get_class_name(clazz["className"], class_names)
                if class_name in api_dic:
                    api_list = api_dic[class_name]
                else:
                    api_list = []
                    api_dic[class_name] = api_list
                fields = clazz["fields"]
                for field in fields:
                    # print( clazz["className"] + "." + field["fieldName"])
                    api = clazz["className"] + "." + field["fieldName"]
                    api = api.replace("$", ".")
                    api_list.append(api)
                    # print(api)
                methods = clazz["methods"]
                for method in methods:
                    # print(method)
                    index = method.find(": ")
                    new_method = method[index + 2:]
                    new_method = new_method[new_method.find(" ") + 1:-1]
                    start = new_method.find("(")
                    method_name = new_method[:start]
                    if method_name == "<init>":
                        dot_index = clazz["className"].rfind(".")
                        if dot_index < 0:
                            new_method = clazz["className"] + new_method[start:]
                        else:
                            new_method = clazz["className"][dot_index+1:] + new_method[start:]
                    api = clazz["className"] + "." + new_method
                    api = api.replace("$", ".")
                    # print(api)
                    api_list.append(api)
                    # print(api)
        write_json("G:/RQ1-data/RQ1_Lib APIs/preprocessed_api/" + file, api_dic)
        # break

def get_class_name(curr_name, class_names):
    # print("++++++++++++++ " + curr_name)
    for name in class_names:
        if curr_name.startswith(name):
            if name + "." in curr_name or name + "$" in curr_name:
                curr_name = name
    # print(curr_name)
    return curr_name

def project_call_preprocess():
    dir = "E:/project_call/total"
    file_list = os.listdir(dir)
    for file in file_list:
        print(file)
        json_data = read_json(os.path.join(dir, file))
        new_list = []
    #     json_data = read_json("E:/project_call/total/834.txt")
        for call in json_data:
            print(call)
            new_call = preprocess(call)
            print(new_call)
            new_list.append(new_call)
        write_json("E:/project_call/new/" + file, new_list)

def preprocess(call):
    call = call.replace("...", "[]")
    new_call = call
    if "<" in call:
        start = call.find("(")
        end = call.find(")", 1)
        arguments = call[start + 1:end]
        # print(arguments)
        new_argu = remove_generics(arguments)
        # print(new_argu)
        new_call = call[:start + 1] + new_argu + call[end:]
    new_call = new_call.replace(" ", "")
    return new_call

def remove_generics(arguments):
    # print(arguments)
    stack = []
    result = []
    for i in range(len(arguments)):
        char = arguments[i]
        if char == "<":
            stack.append(i)
        elif char == ">":
            start = stack.pop(-1)
            if len(stack) == 0:
                result.append((start, i))
        else:
            continue
    length = 0
    for pairs in result:
        # print(pairs)
        arguments = arguments[0:pairs[0]-length] + arguments[pairs[1]-length+1:]
        length += pairs[1] - pairs[0] + 1
    # print(arguments)
    return arguments

def version_time_gap():
    db = database.connectdb()
    sql = "SELECT * FROM project_lib_usage"
    query_result = database.querydb(db, sql)
    for entry in query_result:
        project_id = entry[0]
        version_type_id = entry[1]
        version_id = entry[4]
        # print(version_id)
        sql = "SELECT library_id,repository,parsed_date date FROM library_versions where id = " + str(version_id)
        version_info = database.querydb(db, sql)
        library_id = version_info[0][0]
        repository = version_info[0][1]
        parsed_date = version_info[0][2]
        print(str(library_id) + " " + repository)
        sql = "SELECT count(*) FROM library_versions where library_id = " + str(library_id) + " and repository = '" + repository+ "'"
        total_result = database.querydb(db, sql)
        total_count = total_result[0][0]
        sql = "SELECT count(*) FROM library_versions where library_id = " + str(
            library_id) + " and repository = '" + repository + "' and parsed_date > '" + parsed_date + "'"
        new_result = database.querydb(db, sql)
        new_count = new_result[0][0]

def get_update_projs():
    proj_dic = {}
    json_data = read_json("E:/Workspace_eclipse/ThirdPartyLibraryAnalysis/proj_in_usage.txt")
    for data in json_data:
        id = data["id"]
        path = data["local_addr"].replace("F:/wangying/projects_last_unzips/","").replace("D:/", "").replace("E:/", "").replace("F:/", "")
        proj_dic[id] = path
    dir = "E:/data/proj_update_lib"
    files = os.listdir(dir)
    new_dic = {}
    for file in files:
        project_id = int(file.replace(".txt", ""))
        if project_id == 1492:
            path = "maven500/belaban__fdse__JGroups"
        elif project_id == 5422:
            path = "gradle200_500/rsocket__fdse__rsocket-java"
        else:
            path = proj_dic[project_id]
        new_dic[project_id] = path

    print(len(new_dic))
    write_json("C:/RQ1/update_projs.json", new_dic)

def get_all_calls_contain_dollar():
    result = []
    dir = "E:/project_call/total_preprocessed_exclude_test"
    files = os.listdir(dir)
    for file in files:
        json_data = read_json(os.path.join(dir, file))
        for key in json_data.keys():
            call_list = json_data[key]
            for call in call_list:
                if "$" in call:
                    result.append(call)
    write_json("E:/project_call/dollar.txt", result)

def project_percent():
    dir = ""
    files = os.listdir(dir)
    for file in files:
        project_count = 0
        proj_dic = read_json(os.path.join(dir, file))
        for lib in proj_dic.keys():
            lib_dic = proj_dic[lib]
            for file_id in lib_dic.keys():
                file_dic = lib_dic[file_id]
                for api in file_dic.keys():
                    api_dic = file_dic[api]
                    count = api_dic["count"]
                    project_count += count
        project_call = read_json("E:/project_call/total_preprocessed_exclude_test")

def test_proj():
    # result = {}
    # count = 0
    # dir = "F:/RQ1/file_path"
    # files = os.listdir(dir)
    # print(len(files))
    # for file in files:
    #     project_id = file.replace(".json", "")
    #     contain = False
    #     data = read_json(os.path.join(dir, file))
    #     for key in data.keys():
    #         if "\\src\\test\\" in data[key]:
    #             count += 1
    #             contain = True
    #             break
    #     if not contain:
    #         result[project_id] = data
    # print(count)
    # write_json("F:/RQ1/no_test.txt", result)

    result = {}
    count = 0
    json_data = read_json("F:/RQ1/no_test6.txt")
    print(len(json_data))
    # for project_id in json_data.keys():
    #     contain = False
    #     data = json_data[project_id]
    #     for key in data.keys():
    #         # \\test\\ \\tests\\ \\javatests\\ \\Tests\\ tests\\ test\\
    #         if "test\\" in data[key]:
    #             count += 1
    #             contain = True
    #             break
    #     if not contain:
    #         result[project_id] = data
    # print(count)
    # write_json("F:/RQ1/no_test6.txt", result)

def no_test_proj():
    result = []
    json_data = read_json("F:/RQ1/no_test6.txt")
    print(len(json_data))
    for key in json_data.keys():
        result.append(int(key))
    result.append(3162)
    result.append(4859)
    result.append(2955)
    result = list(set(result))
    print(result)
    print(len(result))
    write_json("no_test_proj.txt", result)

def delete_no_test_project():
    count = 0
    no_test_proj = read_json("no_test_proj.txt")
    # dir = "F:/commit_update_call/proj_update_lib"
    for i in [2, 5, 6, 8]:
        dir = "F:/commit_update_call/batch_200star/new_batch_120/" + str(i)
        print(dir)
        files = os.listdir(dir)
        for file in files:
            project_id = int(file.replace(".sh", "").strip())
            if project_id in no_test_proj:
                print(project_id)
                os.remove(os.path.join(dir, file))
                count += 1
    print()
    print(count)


# version_time_gap()
# get_update_projs()
# filter_test_code()
# check_project_length()
# lib_api_preprocess()
# get_all_calls_contain_dollar()
# check_project_length()
# extract_api_call_by_file()
# test_proj()
# no_test_proj()
delete_no_test_project()
#130 126（2）
# merge_project_call()
# extract_api_call()
# content = read_json("E:/project_call/6_Thinkpad/call/2979_1513.txt")
# project_num()
# project_call_preprocess()
# extract_commit_api_call()
# remove_generics("java.lang.Iterable<java.lang.String>, java.util.List<java.lang.String>")
# remove_generics("java.util.Deque<java.util.List<org.openjdk.source.tree.AnnotationTree<Aaaa>>>, org.openjdk.source.tree.Tree<pack.Test<1233>>")