import os
import database
from draw import draw_bar, draw_barh, draw_line
from file_util import read_json, write_json
from statics_3_new import data_group

db = database.connectdb()

def s_5_1_1():
    keys = [''] * 20
    values = [0] * 20
    for i in range(0, 19):
        start = i * 2
        end = i * 2 + 2
        keys[i+1] = str(start) + "-" + str(end)
    keys[0] = '0'
    values[0] = 722 - 228
    usage_count = read_json("D:/data/data_copy/figure/datas/Fig5-A-Data.json")
    usage_count = list(usage_count.values())
    print(len(usage_count))
    count = 0
    for num in usage_count:
        index = num // 2 + 1
        if num % 2 == 0:
            index -= 1
        values[index] += 1
    draw_bar(keys, values, "The Number of Severe Bugs in a Library Version Release (#)", "The Number of Library Version Releases (#)")

    # 59 + 20 + 21 + 29 + 29 + 22 + 89 + 87 + 67 + 96 + 56 + 76 + 20 + 25 + 26
    # usage_count = read_json("D:/data/data_copy/figure/datas/Fig5-A-Data.json")
    # usage_count = list(usage_count.values())
    # print(usage_count)
    # print(len(usage_count))
    # data_group(usage_count, 2, "The Number of Severe Bugs in a Library Version (#)", "The Number of Library Versions (#)", False)

def s_5_1_2():
    # usage_count = read_json("D:/data/data_copy/figure/datas/Fig5-B-Data2.json")
    # usage_count = list(usage_count.values())
    # print(usage_count)
    # print(len(usage_count))
    # data_group(usage_count, 2, "The Number of Projects Using a Library Version (#)", "The Number of Library Versions (#)", False)
    keys = [''] * 20
    values = [0] * 20
    for i in range(0, 10):
        start = i * 2
        end = i * 2 + 2
        keys[i+1] = str(start) + "-" + str(end)
    keys[11] = '20-30'
    keys[12] = '30-40'
    keys[13] = '40-50'
    keys[14] = '50-60'
    keys[15] = '60-70'
    keys[16] = '70-80'
    keys[17] = '80-90'
    keys[18] = '90-100'
    keys[19] = '>100'
    keys[0] = '0'
    values[0] = 108
    usage_count = read_json("D:/data/data_copy/figure/datas/Fig5-B-Data2.json")
    usage_count = list(usage_count.values())
    print(len(usage_count))
    count = 0
    for num in usage_count:
        if num > 100:
            values[19] += 1
        elif num > 90 and num <= 100:
            values[18] += 1
        elif num > 80 and num <= 90:
            values[17] += 1
        elif num > 70 and num <= 80:
            values[16] += 1
        elif num > 60 and num <= 70:
            values[15] += 1
        elif num > 50 and num <= 60:
            values[14] += 1
        elif num > 40 and num <= 50:
            values[13] += 1
        elif num > 30 and num <= 40:
            values[12] += 1
        elif num > 20 and num <= 30:
            values[11] += 1
        else:
            index = num // 2 + 1
            if num % 2 == 0:
                index -= 1
            # if index < 0:
            #     index = 0
            values[index] += 1
    draw_bar(keys, values, "The Number of Projects Using a Risky Library Version Release (#)", "The Number of Risky Library Version Releases (#)")

def prepare():
    lib_list = ['org.apache.httpcomponents:httpclient','commons-logging:commons-logging','commons-cli:commons-cli','commons-collections:commons-collections','commons-io:commons-io','commons-codec:commons-codec',"org.slf4j:slf4j-api","org.slf4j:slf4j-log4j12","org.slf4j:jcl-over-slf4j","org.slf4j:slf4j-simple","org.apache.logging.log4j:log4j-core","ch.qos.logback:logback-classic","org.apache.commons:commons-lang3","commons-lang:commons-lang","log4j:log4j"]
    print(len(lib_list))
    proj_set = set()
    for entry in lib_list:
        group = entry.split(":")[0]
        name = entry.split(":")[1]
        sql = "SELECT id FROM library WHERE group_str = '"+group+"' and name_str = '"+name+"'"
        query_result = database.querydb(db,sql)
        lib_id = query_result[0][0]
        sql = "SELECT distinct project_id FROM project_lib_usage WHERE library_id = " + str(lib_id)
        query_result = database.querydb(db, sql)
        for entry in query_result:
            proj_set.add(entry[0])
    print(len(proj_set))

# s_5_1_1()
s_5_1_2()
# prepare()
# print(59 + 20 + 21 + 29 + 29 + 22 + 89 + 87 + 67 + 96 + 56 + 76 + 20 + 25 + 26)