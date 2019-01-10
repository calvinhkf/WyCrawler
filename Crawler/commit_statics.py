import os
import time

import database
from check_time import time_interval

from file_util import read_json, write_json


def get_all_commits():
    db = database.connectdb()
    dir = "F:/commit_update_call/proj_update_lib"
    file_list = os.listdir(dir)
    for file in file_list:
        project_id = int(file.replace(".txt", ""))
        json_data = read_json(os.path.join(dir, file))
        print(list(json_data.keys()))
        new_dic = {}
        for commit in json_data.keys():
            sql = "SELECT prev_time FROM lib_update where prev_commit = '" + commit + "' and project_id = " + str(project_id)
            query_result = database.querydb(db, sql)
            if len(query_result) > 0:
                time = query_result[0][0]
            else:
                sql = "SELECT curr_time FROM lib_update where curr_commit = '" + commit + "' and project_id = " + str(
                    project_id)
                query_result = database.querydb(db, sql)
                time = query_result[0][0]
            new_dic[commit] = time
        write_json("F:/commit_update_call/commit_time/" + file, new_dic)

def compare():
    dir = "F:/commit_update_call/proj_update_lib"
    file_list = os.listdir(dir)
    for file in file_list:
        json_data1 = read_json(os.path.join(dir, file))
        length1 = len(json_data1)
        json_data2= read_json(os.path.join("F:/commit_update_call/commit_time", file))
        length2 = len(json_data2)
        if length1 != length2:
            print(file)

def count():
    # 87500
    # count = 0
    # dir = "F:/commit_update_call/proj_update_lib"
    # file_list = os.listdir(dir)
    # for file in file_list:
    #     json_data = read_json(os.path.join(dir, file))
    #     count += len(json_data)
    # print(count)

    # 360 22519
    # 180 13080
    # 150 11402
    # 120 10078
    # 90 8488
    # 60 6563
    # time_str = time.strptime("2018-05-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    # final_time = int(time.mktime(time_str))
    # print(final_time)
    # count = 0
    # dir = "F:/commit_update_call/commit_time"
    # file_list = os.listdir(dir)
    # for file in file_list:
    #     json_data = read_json(os.path.join(dir, file))
    #     for commit in json_data.keys():
    #         if final_time - json_data[commit] <= time_interval(360):
    #             count += 1
    # print(count)

    count = 0
    # projs = [10, 115]
    # projs = [1659]
    projs = [1417]
    dir = "F:/commit_update_call/commit_time"
    file_list = os.listdir(dir)
    for file in file_list:
        project_id = int(file.replace(".txt", ""))
        if project_id in projs:
            json_data = read_json(os.path.join(dir, file))
            count += len(json_data)
    print(count)

def projects():
    result = []
    db = database.connectdb()
    dir = "F:/commit_update_call/proj_update_lib"
    files = os.listdir(dir)
    for file in files:
        id = file.replace(".txt", "")
        sql = "SELECT url FROM project WHERE stars > 500 and id = " + str(id)
        query_result = database.querydb(db, sql)
        if len(query_result) == 0:
            continue
        url = query_result[0][0]
        url = url.replace("https://github.com/", "").replace("/", "__fdse__")
        obj = {}
        obj["id"] = id
        obj["name"] = url
        result.append(obj)
    write_json("update_proj_500+.json", result)

# compare()
# get_all_commits()
# count()
# projects()
# data = read_json("update_proj_500+.json")
# print(len(data))