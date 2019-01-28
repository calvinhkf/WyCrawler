import os
import shutil

import database
from file_util import read_json, read_file


def android_proj():
    android_count = 0
    no_count = 0
    m_g_count = 0
    lines = read_file("H:/wangying/中间过程统计数据/200-500.txt")
    for line in lines:
        if line == "proj-type: android":
            android_count += 1
        elif line == "proj-type: no":
            no_count += 1
        elif line == "proj-type: maven" or line == "proj-type: gradle" or line == "proj-type: maven-gradle":
            m_g_count += 1
        elif line.startswith("proj-type"):
            print(line)

    lines = read_file("H:/wangying/中间过程统计数据/500p.txt")
    for line in lines:
        if line == "proj-type: android":
            android_count += 1
        elif line == "proj-type: no":
            no_count += 1
        elif line == "proj-type: maven" or line == "proj-type: gradle" or line == "proj-type: maven-gradle":
            m_g_count += 1
        elif line.startswith("proj-type"):
            print(line)
    #
    print(android_count)
    print(no_count)
    print(m_g_count)

def divide_batch():
    for i in range(0,6):
        if not os.path.exists("F:/rq1_batch/" + str(i)):
            os.mkdir("F:/rq1_batch/" + str(i))
        data = read_json("G:/data/rq1_1274_"+str(i)+".json")
        for proj in data:
            project_id = proj["id"]
            if os.path.exists("F:/rq1_batch/" + str(project_id) + ".sh"):
                if not os.path.exists("F:/rq1_batch/" + str(i) + "/" + str(project_id) + ".sh"):
                    shutil.copyfile("F:/rq1_batch/" + str(project_id) + ".sh", "F:/rq1_batch/" + str(i) + "/" + str(project_id) + ".sh" )
            else:
                print("F:/rq1_batch/" + str(project_id) + ".sh")
    # db = database.connectdb()
    # sql = "SELECT distinct(repository) FROM library_versions"
    # query_result = database.querydb(db, sql)
    # print(len(query_result))
    # for entry in query_result:
    #     print(entry[0])


android_proj()
# json_data = read_json("E:/data/projs.json");
# print(len(json_data))
# divide_batch()