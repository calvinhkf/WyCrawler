import os

from file_util import read_json, write_json


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
            json_data = None
            if os.path.exists("F:/RQ1-data/RQ1_Lib APIs/LibToFieldsAll/lib_field/" + lib + ".json"):
                json_data = read_json("F:/RQ1-data/RQ1_Lib APIs/LibToFieldsAll/lib_field/" + lib + ".json")
            elif os.path.exists("F:/RQ1-data/RQ1_Lib APIs/lib_fieldaaa/" + lib + ".json"):
                json_data = read_json("F:/RQ1-data/RQ1_Lib APIs/lib_fieldaaa/" + lib + ".json")
            if json_data is not None:
                api_list = set()
    #             json_data = read_json("D:/WeChat/WeChat Files/WeChat Files/clewang1026/Files/abdera-core-1.1.3.jar.json")
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
            call = call.replace("...", "[]")
            new_call = call
            if "<" in call:
                start = call.find("(")
                end = call.find(")", 1)
                arguments = call[start+1:end]
                # print(arguments)
                new_argu = remove_generics(arguments)
                # print(new_argu)
                new_call = call[:start+1] + new_argu + call[end:]
            new_call = new_call.replace(" ","")
            print(new_call)
            new_list.append(new_call)
        write_json("E:/project_call/new/" + file, new_list)


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
extract_api_call()
# content = read_json("E:/project_call/6_Thinkpad/call/2979_1513.txt")
# project_num()
# project_call_preprocess()
# remove_generics("java.lang.Iterable<java.lang.String>, java.util.List<java.lang.String>")
# remove_generics("java.util.Deque<java.util.List<org.openjdk.source.tree.AnnotationTree<Aaaa>>>, org.openjdk.source.tree.Tree<pack.Test<1233>>")