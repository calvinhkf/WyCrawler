import os
import json
import time
import datetime
import sys

import database
from exception import CustomizeException

db = database.connectdb()

def output_download_timeas_str(m_dict):
    for entry in m_dict:
        path = entry['url']
        tmp = path.split('/')
        line = '/home/fdse/data/prior_repository/' + tmp[-2] + '/' + tmp[-1]
        if not os.path.exists(line):
            print('err')
            break
        # print(line)
        sh = 'stat ' + line
        ff = os.popen(sh)
        result = ff.read()
        data = result.split('\n')
        date = ''
        for line in data:
            if line.startswith('Change: '):
                date = line.strip('\n')[8:]
                break
        m_time = date.split('.')[0]
        # print(m_time)
        entry['download_time'] = m_time


def output_repo_time_as_str(m_dict):
    for entry in m_dict:
        path = entry['url']
        tmp = path.split('/')
        line = '/home/fdse/data/prior_repository/' + tmp[-2] + '/' + tmp[-1]
        if not os.path.exists(line):
            print('err')
            break
        # print(line)
        sh = 'git --git-dir=' + line + '/.git log -n 1 --date=iso'
        ff = os.popen(sh)
        result = ff.read()
        data = result.split('\n')
        date = ''
        for line in data:
            if line.startswith('Date'):
                date = line.strip('\n')
                break
        m_time = date.split('te:')[1][0:-6]
        entry['head_commit_time'] = m_time.strip(' ')


# def threshold_time(weekNum):
#     delta_one_year = (datetime.datetime.now()+datetime.timedelta(weeks=weekNum)).strftime("%Y-%m-%d %H:%M:%S")
#     now = time.time()
#     thtime = time.strptime(delta_one_year,'%Y-%m-%d %H:%M:%S')
#     thstamp = int(time.mktime(thtime))
#     return thstamp

def input_repo_time_compare(num):
    with open('E:/data/projs.8.11.time.json', 'r') as f:
        content = f.read()
        m_dict = json.loads(content)
    cnt = 0
    print(len(m_dict))
    for entry in m_dict:
        download_time = entry['download_time']
        head_commit_time = entry['head_commit_time']
        download_time2 = time.strptime(download_time, '%Y-%m-%d %H:%M:%S')
        head_commit_time2 = time.strptime(head_commit_time, '%Y-%m-%d %H:%M:%S')
        download_time3 = int(time.mktime(download_time2))
        head_commit_time3 = int(time.mktime(head_commit_time2))

        if download_time3 - head_commit_time3 > time_interval(num):
            # print(threshold_time(time, 52))
            cnt += 1

    print(cnt)


def time_interval(days):
    prev_time = time.strptime("2018-07-20 02:44:16", '%Y-%m-%d %H:%M:%S')
    curr_time = time.strptime("2018-07-21 02:44:16", '%Y-%m-%d %H:%M:%S')
    prev_time_num = int(time.mktime(prev_time))
    curr_time_num = int(time.mktime(curr_time))
    one_day = curr_time_num - prev_time_num
    return one_day * days


def get_maven_proj_update_within_three_months(num):
    gradle_array = []
    with open('E:/data/projs.8.11.time.json', 'r') as f:
        content = f.read()
        m_dict = json.loads(content)
    cnt = 0
    print(len(m_dict))
    for entry in m_dict:
        download_time = entry['download_time']
        head_commit_time = entry['head_commit_time']
        download_time2 = time.strptime(download_time, '%Y-%m-%d %H:%M:%S')
        head_commit_time2 = time.strptime(head_commit_time, '%Y-%m-%d %H:%M:%S')
        download_time3 = int(time.mktime(download_time2))
        head_commit_time3 = int(time.mktime(head_commit_time2))

        if download_time3 - head_commit_time3 <= time_interval(num):
            type_ = entry["proj-type"]
            # if type_ == "proj-type: maven":
            # if type_ == "proj-type: maven-gradle":
            if type_ == "proj-type: maven-gradle":
                url = entry["url"]
                sql = "SELECT * FROM project WHERE url = '" + url + "'"
                query_result = database.querydb(db, sql)
                if len(query_result) > 0:
                    gradle_array.append(url)
                    # with open("gradle_maven_url_three_months.txt", "a") as f:
                    #     f.write(str(query_result[0][0]) + "\n")
                    #     f.write(query_result[0][1] + "\n")
                    # f.close()
                else:
                    raise CustomizeException("Not in db:" + url)
                cnt += 1
    print(cnt)

    return gradle_array


# arg = sys.argv[1]
# input_repo_time_compare(int(arg))

# def a1():
#     with open('projs.json' ,'r') as f:
#         content = f.read()
#         m_dict = json.loads(content)
#     output_repo_time_as_str(m_dict)
#     output_download_timeas_str(m_dict)
#     with open('projs2.json','w') as f:
#             json.dump(m_dict,f)
# a1()

# input_repo_time_compare(52)
# input_repo_time_compare(90)

get_maven_proj_update_within_three_months(90)