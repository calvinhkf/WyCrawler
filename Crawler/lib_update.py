import database
import json

import database
from exception import CustomizeException
from file_util import read_json
from lib_release_time import get_time_from_maven

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
db = database.connectdb()

lib_list = []
# result_list = []

def get_no_duplicated_lib():
    # for i in range(40001, 810000):
    for i in range(60001, 810000):
        print("++++++++++++++++"+str(i))
        sql = "SELECT * FROM lib_update WHERE id = " + str(i)
        update = database.querydb(db, sql)
        if len(update) != 0:
            group = update[0][4]
            name = update[0][5]
            prev_version = update[0][6]
            curr_version = update[0][7]
            lib1 = group + " " + name + " " + prev_version
            if lib1 not in lib_list:
                lib_list.append(lib1)
            lib2 = group + " " + name + " " + curr_version
            if lib2 not in lib_list:
                lib_list.append(lib2)
    print(len(lib_list))
    id = 0
    result = []
    for lib in lib_list:
        print(lib)
        id += 1
        lib_dic = {}
        lib_dic["id"] = id
        array = lib.split()
        if len(array) != 3:
            raise (CustomizeException("len(array) != 3"))
        lib_dic["groupId"] = array[0]
        lib_dic["artifactId"] = array[1]
        lib_dic["version"] = array[2]
        result.append(lib_dic)
    print(len(result))
    with open("lib.txt", 'w') as file_object:
        json.dump(result, file_object)

def handle_lib_by_id(start,end):
    data = read_json("lib.txt")
    for lib_dic in data:
        if "id" in lib_dic:
            id = lib_dic["id"]
            if id <= end and id >= start:
                if "groupId" not in lib_dic or "artifactId" not in lib_dic or "version" not in lib_dic:
                    continue
                groupId =lib_dic["groupId"]
                artifactId =lib_dic["artifactId"]
                version = lib_dic["version"]
                print("-------------id :"+str(id))
                print(str(groupId)+"  "+ str(artifactId)+"  "+ str(version))
                _time = get_time_from_maven(groupId, artifactId, version)
                if _time is not None:
                    with open("output.txt", 'a') as file_object:
                        file_object.write(str(id)+"+++"+str(groupId)+"+++"+str(artifactId)+"+++"+str(version)+"+++"+str(_time)+"\n")
                    # lib_dic["time"] = _time
                    # result_list.append(lib_dic)
    # if len(result_list) != 0:
    #     with open("output.txt", 'w') as file_object:
    #         json.dump(result_list, file_object)

handle_lib_by_id(12, 13)
# get_no_duplicated_lib()