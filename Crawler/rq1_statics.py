import os

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

#130 126（2）
# merge_project_call()
# extract_api_call()
# content = read_json("E:/project_call/6_Thinkpad/call/2979_1513.txt")
# project_num()
# project_call_preprocess()
extract_commit_api_call()
# remove_generics("java.lang.Iterable<java.lang.String>, java.util.List<java.lang.String>")
# remove_generics("java.util.Deque<java.util.List<org.openjdk.source.tree.AnnotationTree<Aaaa>>>, org.openjdk.source.tree.Tree<pack.Test<1233>>")