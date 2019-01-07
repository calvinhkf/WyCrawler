import os
import shutil

import database

from exception import CustomizeException
from file_util import read_json, write_json

def combina_dependency():
    final_dic = {}
    write_to_final_jar(final_dic)

def write_to_final_jar(final_dic):
    dir = "I:/libs/lib_500-1000+/all/dependency_library_info"
    files = os.listdir(dir)
    for file in files:
        print("========================== " + dir + "/" + file)
        name = file.replace(".json", "")
        file_content = read_json(os.path.join(dir, file))
        version_list = file_content["version_types_list"]
        for version_type in version_list:
            version = version_type["version"]
            _type = version_type["_type"]
            classifier = version_type["classifier"]
            jar_package_url = version_type["jar_package_url"]
            key = name + " " + version + " " + _type
            if classifier is not None:
                key += " " + classifier
            if key not in final_dic:
                final_dic[key] = jar_package_url
            # else:
            #     raise CustomizeException("repeat key: " + key + "( " + final_dic[key] + "," + jar_package_url + " )")
    write_json("final_jar_dic.txt", final_dic)

def append_final_jar():
    final_dic = read_json("final_jar_dic.txt")
    print(len(final_dic))
    # write_to_final_jar(final_dic)

def proj_jar_list():
    db = database.connectdb()

    jars_dic = read_json("final_jar_dic.txt")

    dir = "D:/data/result"
    file_list = os.listdir(dir)
    for file in file_list:
        project_id = int(file.split("_")[0])
        sql = "SELECT * FROM project WHERE stars > 5000 and id = " + str(project_id)
        query_result = database.querydb(db,sql)
        if len(query_result) <= 0:
            continue
        print(project_id)
        file_jars = []
        print("++++++++++++++++++++++++++++ " + file)
        data = read_json(os.path.join(dir, file))
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
            if type(version) == list:
                continue
            key = groupId + " " + artifactId + " " + version + " " + type_
            if "classifier" in lib:
                classifier = lib["classifier"]
                key += " " + classifier
            if key in jars_dic:
                file_jars.append(jars_dic[key])
        file_jars = list(set(file_jars))
        write_json("D:/data/lib_list/"+file, file_jars)
        # break

def append_proj_jar_list_gradle():
    db = database.connectdb()

    jars_dic = read_json("final_jar_dic.txt")

    dir = "I:/RQ2-data/result_merge_gradle_id"
    file_list = os.listdir(dir)
    for file in file_list:
        project_id = int(file.replace(".txt",""))
        sql = "SELECT * FROM project WHERE stars > 5000 and id = " + str(project_id)
        query_result = database.querydb(db,sql)
        if len(query_result) <= 0:
            continue
        print(project_id)
        print("++++++++++++++++++++++++++++ " + file)
        data = read_json(os.path.join(dir, file))
        for commit in data.keys():
            if commit == "name":
                continue
            file_jars = []
            versions = data[commit]
            for lib in versions:
                groupId= lib["groupId"]
                artifactId = lib["artifactId"]
                version = lib["version"]
                type_ = "jar"
                key = groupId + " " + artifactId + " " + version + " " + type_
                if key in jars_dic:
                    file_jars.append(jars_dic[key])
            if len(file_jars) > 0:
                file_jars = list(set(file_jars))
                write_json("D:/data/lib_list_test/"+str(project_id) + "_" + str(commit) + ".txt", file_jars)
                # origin_path = "D:/data/lib_list/"+str(project_id) + "_" + str(commit) + ".txt"
                # if os.path.exists(origin_path):
                #     print(origin_path)
                #     origin = read_json(origin_path)
                #     file_jars.extend(origin)
                # file_jars = list(set(file_jars))
                # write_json(origin_path, file_jars)

def divide_to_machine():
    # db = database.connectdb()
    # total_list = []
    # dir = "H:/proj_update_lib"
    # file_list = os.listdir(dir)
    # for file in file_list:
    #     name = file.replace(".txt", "")
    #     projectId = int(name)
    #     sql = "SELECT * FROM project WHERE stars > 5000 and id = " + str(projectId)
    #     query_result = database.querydb(db, sql)
    #     if len(query_result) > 0:
    #         total_list.append(projectId)
    # print(total_list)
    # print(len(total_list))
    #
    # dir = "I:/分机器跑的数据/data"
    # for i in range(0,10):
    #     new_list = []
    #     path = dir + "/rq1_" + str(i) + ".json"
    #     # print(path)
    #     json_data = read_json(path)
    #     for data in json_data:
    #         url = data["url"]
    #         sql = "SELECT id FROM project WHERE url  = '" + url + "'"
    #         query_result = database.querydb(db, sql)
    #         id = query_result[0][0]
    #         if id in total_list:
    #             new_list.append(id)
    #     write_json("H:/api_call_update/batch_scope/"+str(i)+".txt",new_list)

    dir = "H:/api_call_update/batch_scope"
    file_list = os.listdir(dir)
    for file in file_list:
        num = int(file.replace(".txt", ""))
        json_data = read_json(os.path.join(dir, file))
        if len(json_data) > 0:
            if os.path.exists(dir + "/" + str(num)):
                os.mkdir(dir + "/" + str(num))
            for id in json_data:
                shutil.copyfile("H:/api_call_update/batch/"+str(id)+".sh", dir + "/" + str(num) + "/"+str(id)+".sh")

def jars_to_diff_machine():
    # projs = [1107, 1109, 1213, 130, 138, 180, 193, 197, 2, 20, 205, 223, 258, 262, 270, 271, 279, 30, 34, 346, 347, 351, 359,
    #  38, 388, 4, 446, 447, 556, 591, 6, 654, 660, 68, 692, 709, 797, 8, 84, 966]
    # print(len(projs))
    dir = "H:/api_call_update/batch_scope"
    file_list = os.listdir(dir)
    for file in file_list:
        num = int(file.replace(".txt", ""))
        proj_list = read_json(os.path.join(dir, file))
        if len(proj_list) > 0:
            print(proj_list)
            result = []
            jars_files = os.listdir("D:/data/lib_list")
            for entry in jars_files:
                project_id = int(entry.split("_")[0])
                # print(project_id)
                if project_id in proj_list:
                    result.extend(read_json(os.path.join("D:/data/lib_list", entry)))
            result = list(set(result))
            write_json("H:/api_call_update/batch_scope/" + str(num) + "_jar.txt",result)

def move_jars():
    src_dir = "H:/api_call_update/batch/"
    dst_dir = ""
    jars = read_json("H:/api_call_update/batch_scope/0_jar.txt")
    for jar in jars:
        shutil.copyfile("I:/libs/lib_5000Plus/all/lib/ " + jar, ".sh")


def proj():
    data = read_json("proj_in_usage.txt")
    print(len(data))
    # result = []
    # db = database.connectdb()
    # sql = "SELECT * FROM project"
    # query_result = database.querydb(db, sql)
    # for entry in query_result:
    #     url = entry[1]
    #     id = entry[0]
    #     url = url.replace("https://github.com/","").replace("/","__fdse__")
    #     print(url)
    #     obj = {}
    #     obj["id"] = id
    #     obj["local_addr"] = url
    #     result.append(obj)
    # write_json("proj_in_usage.txt",result)

def jar_url():
    final_dic = {}
    dir = "F:/libs/lib_500-1000/all/lib"
    jars = os.listdir(dir)
    for jar in jars:
        if jar.endswith(".jar"):
            if jar not in final_dic:
                final_dic[jar] = "libs/lib_500-1000/all/lib"
            else:
                raise CustomizeException("contains key : " + jar)
    write_json("meta.json")

def db_jar_list():
    # final_dic = read_json("final_jar_dic.txt")
    # print(len(final_dic))

    final_dic = {}

    db = database.connectdb()
    sql = "SELECT * FROM version_types"
    query_result = database.querydb(db, sql)
    for entry in query_result:
        jar_name = entry["jar_package_url"]
        _type = entry["type"]
        classifier = entry["classifier"]
        version_id = entry["version_id"]
        sql = "SELECT * FROM library_versions where id = " + str(version_id)
        query_result = database.querydb(db, sql)
        groupId = query_result[0][1]
        artifactId = query_result[0][2]
        version = query_result[0][3]
        key = groupId + " " + artifactId + " " + version + " " + _type
        if classifier is not None:
            key += " " + classifier
        if key not in final_dic:
            final_dic[key] = jar_name
    print(len(final_dic))
    write_json("final_jar_test.txt", final_dic)


# combina_dependency()
# final_count()
# proj_jar_list()
# append_proj_jar_list_gradle()
# divide_to_machine()
# append_final_jar()
# proj()
# jars_to_diff_machine()
db_jar_list()

