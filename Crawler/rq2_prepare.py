import os
import database
from file_util import write_json, read_json


def collect_update_entry():
    db = database.connectdb()
    sql = "SELECT id,project_id,prev_commit,curr_commit,prev_type_id,curr_type_id FROM lib_update WHERE prev_type_id is not null and curr_type_id is not null"
    query_result = database.querydb(db, sql)
    print(query_result)
    result = []
    for entry in query_result:
        print(list(entry))
        result.append(list(entry))
    write_json("lib_update_entry.txt", result)

def generate_data():
    lib_update_dic = {}
    db = database.connectdb()
    entries = read_json("lib_update_entry.txt")
    print(len(entries))
    for entry in entries:
        print(entry)
        id = entry[0]
        project_id = entry[1]
        prev_commit = entry[2]
        curr_commit = entry[3]
        prev_type_id = entry[4]
        curr_type_id = entry[5]
        key = str(project_id) + " " + prev_commit + " " + curr_commit
        sql = "SELECT jar_package_url FROM version_types WHERE type_id = " + str(prev_type_id)
        query_result = database.querydb(db, sql)
        prev_jar = query_result[0][0]
        sql = "SELECT jar_package_url FROM version_types WHERE type_id = " + str(curr_type_id)
        query_result = database.querydb(db, sql)
        curr_jar = query_result[0][0]
        value = prev_jar + " " + curr_jar
        if key in lib_update_dic:
            lib_update_dic[key].append(value)
        else:
            new_array = [value]
            lib_update_dic[key] = new_array
    write_json("lib_update_dic.txt", lib_update_dic)

def get_jar_call_list():
    api_call_path = "F:/commit_update_call/result/api_call"
    json_data = read_json("lib_update_dic.txt")
    for key in json_data.keys():
        key_array = key.split(" ")
        project_id = key_array[0]
        prev_commit = key_array[1]
        curr_commit = key_array[2]
        values = json_data[key]
        new_result = []
        for value in values:
            value_array = value.split(" ")
            prev_jar = value_array[0]
            curr_jar = value_array[1]
            prev_list = None
            curr_list = None
            if os.path.exists(api_call_path + "/" + project_id + "_" + prev_commit + ".txt"):
                prev_list = []
                call_dic = read_json(api_call_path + "/" + project_id + "_" + prev_commit + ".txt")
                if prev_jar in call_dic:
                    for entry in call_dic[prev_jar].keys():
                        prev_list.append(entry)
            if os.path.exists(api_call_path + "/" + project_id + "_" + curr_commit + ".txt"):
                curr_list = []
                call_dic = read_json(api_call_path + "/" + project_id + "_" + curr_commit + ".txt")
                if curr_jar in call_dic:
                    for entry in call_dic[curr_jar].keys():
                        curr_list.append(entry)
            if prev_list is not None and curr_list is not None:
                obj = {}
                obj["prev_jar"] = prev_jar
                obj["curr_jar"] = curr_jar
                obj["prev_api_call_list"] = prev_list
                obj["curr_api_call_list"] = curr_list
                new_result.append(obj)
        if len(new_result) > 0:
            write_json("F:/commit_update_call/result/compare_list/" + key + ".txt", new_result)


# collect_update_entry()
# generate_data()
get_jar_call_list()