import shutil
import time
import os

import database
from check_time import time_interval

from file_util import read_json, write_json, append_file, read_file


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
    time_str = time.strptime("2018-05-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    final_time = int(time.mktime(time_str))
    print(final_time)
    count = 0
    dir = "I:/commit_update_call/commit_time"
    file_list = os.listdir(dir)
    for file in file_list:
        json_data = read_json(os.path.join(dir, file))
        for commit in json_data.keys():
            if final_time - json_data[commit] <= time_interval(30):
                count += 1
    print(count)

    # count = 0
    # # projs = [10, 115]
    # # projs = [1659]
    # projs = [1417]
    # dir = "F:/commit_update_call/commit_time"
    # file_list = os.listdir(dir)
    # for file in file_list:
    #     project_id = int(file.replace(".txt", ""))
    #     if project_id in projs:
    #         json_data = read_json(os.path.join(dir, file))
    #         count += len(json_data)
    # print(count)

    # count = 0
    # dir = "F:/commit_update_call/proj_update_lib"
    # file_list = os.listdir(dir)
    # for file in file_list:
    #     json_data = read_json(os.path.join(dir, file))
    #     count += len(json_data)
    # print(count)

def generate_batch():
    first_list = read_json("I:/commit_update_call/batch_scope/200star/8.txt")
    # second_list = read_json("I:/commit_update_call/batch_scope/200star/8.txt")
    time_str = time.strptime("2018-05-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    final_time = int(time.mktime(time_str))
    dir = "I:/commit_update_call/batch/num"
    files = os.listdir(dir)
    for file in files:
        print(file)
        project_id = file.replace(".txt", "")
        if int(project_id) not in first_list:
            continue
        # if project_id != "130" and project_id != "1907" and project_id != "2594":
        #     continue
        commit_time = read_json("I:/commit_update_call/commit_time/" + project_id + ".txt")
        nums = read_json(os.path.join(dir, file))
        for commit in nums.keys():
            if final_time - commit_time[commit] <= time_interval(120) and final_time - commit_time[commit] > time_interval(90):
            # if final_time - commit_time[commit] <= time_interval(30):
                total_num = int(nums[commit])
                i = 0
                while i < total_num:
                    start = i
                    end = i + 100
                    if end > total_num:
                        end = total_num
                    cmd = "java -jar apicallupdate.jar " + project_id + " " + commit + " " + str(start) + " " + str(end)
                    append_file("I:/commit_update_call/batch_200star/new_batch_120/8/" + project_id + ".sh", cmd)
                    i += 100


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

def commit_count():
    # 2955
    # time_str = time.strptime("2018-05-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    # final_time = int(time.mktime(time_str))
    # count = 0
    # commits = set()
    # for i in range(0, 7):
    #     dir = "I:/commit_update_call/batch/" + str(i)
    #     files = os.listdir(dir)
    #     for file in files:
    #         if not file.endswith(".sh"):
    #             continue
    #         project_id = file.replace(".sh", "")
    #         commit_time = read_json("I:/commit_update_call/commit_time/" + project_id + ".txt")
    #         lines = read_file(os.path.join(dir, file))
    #         for line in lines:
    #             com = line.split(" ")[4]
    #             if final_time - commit_time[com] <= time_interval(30):
    #                 commits.add(project_id + " " + com)
    # print(len(commits))
    # write_json("commits.txt", list(commits))

    com_commits = read_json("commits.txt")
    count = 0
    commits = set()
    dir = "I:/commit_update_call/batch/new_batch_60"
    files = os.listdir(dir)
    for file in files:
        project_id = file.replace(".sh", "")
        lines = read_file(os.path.join(dir, file))
        for line in lines:
            com = line.split(" ")[4]
            commits.add(project_id + " " + com)
        # count += len(commits)
    print(len(commits))
    # for entry in com_commits:
    #     if entry not in commits:
    #         print(entry)

def divide_batch():
    # count = 0
    # dir = "I:/commit_update_call/batch_scope"
    # files = os.listdir(dir)
    # for file in files:
    #     json_data = read_json(os.path.join(dir, file))
    #     count += len(json_data)
    # print(count)

    # for i in range(0,3):
    #     path = "I:/commit_update_call/batch_scope/" + str(i) + ".txt"
    #     proj_list = read_json(path)
    #     print(proj_list)
    #     length = len(proj_list)
    #     index = int((length + 1)/ 2)
    #     print(len(proj_list))
    #     list1 = proj_list[:index]
    #     list2 = proj_list[index:]
    #     print(list1)
    #     print(len(list1))
    #     print(list2)
    #     print(len(list2))
    #     write_json("I:/commit_update_call/batch_scope/" + str(i) + ".txt", list1)
    #     write_json("I:/commit_update_call/batch_scope/" + str(i+7) + ".txt", list2)

    dir = "I:/commit_update_call/batch_scope"
    files = os.listdir(dir)
    for file in files:
        id = file.replace(".txt", "")
        if not os.path.exists("I:/commit_update_call/batch/new_batch_120/" + id):
            os.mkdir("I:/commit_update_call/batch/new_batch_120/" + id)
        proj_list = read_json(os.path.join(dir, file))
        for proj in proj_list:
            if os.path.exists("I:/commit_update_call/batch/new_batch_120/" + str(proj) + ".sh"):
                shutil.copyfile("I:/commit_update_call/batch/new_batch_120/" + str(proj) + ".sh","I:/commit_update_call/batch/new_batch_120/" + id + "/" + str(proj) + " .sh")

def handle_batch():
    for i in [2, 8]:
        dir = "J:/commit_update_call/batch_200star/" + str(i)
        files = os.listdir(dir)
        for file in files:
            if not file.endswith(".sh"):
                continue
            project_id = file.replace(".sh", "")
            print(file)
            num_dic = {}
            cmds = read_file(os.path.join(dir, file))
            for cmd in cmds:
                cmd_str = cmd.split(" ")
                commit = cmd_str[4]
                num = int(cmd_str[6])
                num_dic[commit] = num
            write_json("J:/commit_update_call/" + project_id + ".txt", num_dic)

# compare()
# get_all_commits()
# count()
# projects()
# data = read_json("update_proj_500+.json")
# print(len(data))
generate_batch()
# commit_count()
# divide_batch()
# handle_batch()