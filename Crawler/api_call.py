import os
import database

from exception import CustomizeException
from file_util import read_json, write_json
from modifier_util import isAbstract, isInterface, isNative, isPublic
from rq1_statics import preprocess


def lib_api_preprocess():
    dir = "D:/data/data_copy/lib_to_field/lib_field"
    files = os.listdir(dir)
    for file in files:
        print(file)
        if os.path.exists("D:/data/data_copy/lib_to_field/preprocessed_api/" + file):
            continue
        api_set = set()
        json_data = read_json(os.path.join(dir, file))
        if json_data is not None:
            # count = 0
            for clazz in json_data:
                # print(clazz["className"])
                fields = clazz["fields"]
                # count += len(fields)
                for field in fields:
                    # print( clazz["className"] + "." + field["fieldName"])
                    modifiers = field["modifiers"]
                    if not isAbstract(modifiers) and not isInterface(modifiers) and not isNative(modifiers) and isPublic(modifiers):
                        api = clazz["className"] + "." + field["fieldName"]
                        api = api.replace("$", ".")
                        api_set.add(api)
                        # print(api)
                methods = clazz["methods"]
                # count += len(methods)
                for method in methods:
                    # print(method)
                    modifiers = method["modifiers"]
                    declaration = method["methodName"]
                    if not isAbstract(modifiers) and not isInterface(modifiers) and not isNative(
                            modifiers) and isPublic(modifiers):
                        index = declaration.find(": ")
                        new_method = declaration[index + 2:]
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
                        api_set.add(api)
                        # print(api)
            # print(count)
            # print(len(api_set))
            write_json("D:/data/data_copy/lib_to_field/preprocessed_api/" + file, list(api_set))
        # break

def merge_project_call():
    dir = "D:/data/data_copy/RQ1/project_call/call_add/call"
    file_list = os.listdir(dir)
    curr_id = None
    call_obj = {}
    for file in file_list:
        print(file)
        project_id = int(file.split("_")[0])
        # call_wangxin
        if project_id != 2979:
            continue
        content = read_json(os.path.join(dir, file))
        if content is None:
            raise CustomizeException("content is None")
            sys.exit(0)
            # continue
        callInParent = content["callInParent"]
        otherDeclaration = content["otherDeclaration"]
        call_list = []
        for key in callInParent.keys():
            new_obj = {}
            new_obj["className"] = key
            new_obj["call_list"] = callInParent[key]
            call_list.append(new_obj)
        if curr_id is None:
            curr_id = project_id
            call_obj["callInParent"] = call_list
            call_obj["otherDeclaration"] = otherDeclaration
        elif curr_id != project_id:
            write_json("D:/data/data_copy/RQ1/project_call/total/" + str(curr_id) + ".txt", call_obj)
            # break
            curr_id = project_id
            call_obj = {}
            call_obj["callInParent"] = call_list
            call_obj["otherDeclaration"] = otherDeclaration
        else:
            call_obj["callInParent"].extend(call_list)
            call_obj["otherDeclaration"].extend(otherDeclaration)
    write_json("D:/data/data_copy/RQ1/project_call/total/" + str(curr_id) + ".txt", call_obj)

def project_call_preprocess():
    # dir = "D:/data/data_copy/RQ1/project_call/total/"
    # file_list = os.listdir(dir)
    # for file in file_list:
    #     print(file)
    #     json_data = read_json(os.path.join(dir, file))
    #     callInParent = json_data["callInParent"]
    #     for entry in callInParent:
    #         new_list = []
    #         call_list = entry["call_list"]
    #         for call in call_list:
    #             print(call)
    #             new_call = preprocess(call)
    #             print(new_call)
    #             new_list.append(new_call)
    #         entry["call_list"] = new_list
    #     write_json("D:/data/data_copy/RQ1/project_call/total_new/"+ file, json_data)

    dir = "D:/data/data_copy/RQ1/project_call/total_new/"
    file_list = os.listdir(dir)
    for file in file_list:
        print("+++++++++++++++++++++++++++++++" + file)
        json_data = read_json(os.path.join(dir, file))
        callInParent = json_data["callInParent"]
        for entry in callInParent:
            new_list = []
            call_list = entry["call_list"]
            for call in call_list:
                call = call.replace(" ", "")
                obj = {}
                obj["api"] = call
                # obj["lib"] = lib
                new_list.append(obj)
            entry["call_list"] = new_list

        write_json("D:/data/data_copy/RQ1/project_call/total_final/" + file, json_data)
        # break

def check():
    dir = "D:/data/data_copy/RQ1/project_call/total"
    file_list = os.listdir(dir)
    for file in file_list:
        print(file)
        project_id = int(file.replace(".txt", ""))
        if project_id != 2979:
            continue
        content = read_json(os.path.join(dir, file))
        callInParent = content["callInParent"]
        otherDeclaration = content["otherDeclaration"]
        one_count = 0
        two_count = 0
        new_dir = "D:/data/data_copy/RQ1/project_call/call_add/call"
        new_list = os.listdir(new_dir)
        for f in new_list:
            # print(os.path.join(new_dir, f))
            id = int(f.split("_")[0])
            if id == project_id:
                data = read_json(os.path.join(new_dir, f))
                one_count += len(data["callInParent"])
                two_count += len(data["otherDeclaration"])
        if one_count != len(callInParent):
            raise CustomizeException("one_count = " + str(one_count) + " len"
                                                        "(callInParent) = " + str(len(callInParent)))
            sys.exit(0)
        if two_count != len(otherDeclaration):
            raise CustomizeException("two_count = " + str(two_count) + " len(otherDeclaration) = " + str(len(otherDeclaration)))
            sys.exit(0)
        print(str(one_count) + " " + str(two_count))
        # break

def unsolved_proj():
    db = database.connectdb()
    sql = "SELECT DISTINCT project_id FROM project_lib_usage"
    query_result = database.querydb(db, sql)
    proj_ids = []
    for entry in query_result:
        proj_id = entry[0]
        proj_ids.append(proj_id)
    print(len(proj_ids))
    print(proj_ids)
    count = 0
    for id in proj_ids:
        if not os.path.exists("D:/data/data_copy/RQ1/project_call/total/" + str(id) + ".txt"):
            count += 1
            print(id)
    print(count)

def extract_api_call():
    dir = "D:/data/data_copy/RQ1/project_call/total_final/"
    file_list = os.listdir(dir)
    for file in file_list:
        if os.path.exists("D:/data/data_copy/RQ1/project_call/api_call/" + file):
            continue
        print("+++++++++++++++++++++++++++++++" + file)
        project_id = int(file.replace(".txt", ""))
        json_data = read_json(os.path.join(dir, file))
        callInParent = json_data["callInParent"]
        lib_list = read_json("D:/data/data_copy/RQ1/lib_list/" + str(project_id) + ".json")
        for lib in lib_list:
            print(lib)
            if os.path.exists("D:/data/data_copy/lib_to_field/preprocessed_api/" + lib + ".json"):
                api_list = read_json("D:/data/data_copy/lib_to_field/preprocessed_api/" + lib + ".json")
                if api_list is not None:
                    for entry in callInParent:
                        call_list = entry["call_list"]
                        for call_obj in call_list:
                            call = call_obj["api"]
                            if call in api_list:
                                call_obj["lib"] = lib
        write_json("D:/data/data_copy/RQ1/project_call/api_call/" + file, json_data)
        # break

def get_api_list_of_lib(lib):
    # dir_path = "F:/"
    json_data = set()
    if os.path.exists("D:/data/data_copy/lib_to_field/preprocessed_api/" + lib + ".json"):
        data = read_json("D:/data/data_copy/lib_to_field/preprocessed_api/" + lib + ".json")
        return set(data)
    return json_data



# print(isAbstract(1))
# print(isInterface(1))
# print(isNative(1))
# print(isPublic(1))
# print(not isAbstract(2) and not isInterface(2) and not isNative(2) and isPublic(2))
# print(isPublic(2))
# lib_api_preprocess()
# merge_project_call()
# check()
# unsolved_proj()
# project_call_preprocess()
extract_api_call()