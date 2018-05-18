import json
import random

import requests
import time
from bs4 import BeautifulSoup

import database
from exception import CustomizeException

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
# db = database.connectdb()

lib_list = []

def update_release_time():
    for i in range(21135, 100000):
        print("+++++++++++++++++++++++++ " + str(i))
        sql = "SELECT * FROM lib_update WHERE id = " + str(i)
        update = database.querydb(db, sql)
        if len(update) != 0:
            group = update[0][4]
            name = update[0][5]
            prev_version = update[0][6]
            curr_version = update[0][7]
            # print("+++++++++++++++++++++++++group:" + str(group))
            # print("+++++++++++++++++++++++++name:" + str(name))
            # print("+++++++++++++++++++++++++prev_version:" + str(prev_version))
            # print("+++++++++++++++++++++++++curr_version:" + str(curr_version))
            time1 = get_time(group, name, prev_version)
            time2 = get_time(group, name, curr_version)
            # sql = "UPDATE lib_update SET prev_release_time = '"+str(time1) +"', curr_release_time= '"+str(time2)+"' WHERE id = "+ str(i)
            sql = "UPDATE lib_update SET prev_release_time = "
            if time1 is None:
                sql += "NULL"
            else:
                sql += "'"+str(time1) +"'"
            sql += ", curr_release_time="
            if time2 is None:
                sql += "NULL"
            else:
                sql += "'"+str(time2) +"'"
            sql +=  " WHERE id = "+ str(i)
            database.execute_sql(db, sql)



def get_time(groupId,artifactId,version):
    key = str(groupId) + " " + str(artifactId) + " " + str(version)
    sql = "SELECT * FROM lib_release_time WHERE lib_name = '" + key + "'"
    realease_time = database.querydb(db, sql)
    if len(realease_time) != 0:
        _time = realease_time[0][1]
    else:
        _time = get_time_from_maven(groupId,artifactId,version)
        if _time is None:
            sql = "INSERT INTO lib_release_time (lib_name,time) VALUES ('" + key + "',NULL)"
        else:
            sql = "INSERT INTO lib_release_time (lib_name,time) VALUES ('" + key + "','" + str(_time)+ "')"
        database.execute_sql(db, sql)
    return _time

def get_time_from_maven(groupId,artifactId,version):
    version_url = "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId + "/" + version
    library_version = requests.get(version_url, headers=headers)
    library_soup = BeautifulSoup(library_version.text, 'lxml');
    if library_soup.find('h2', class_='im-title') is None:
        print("can't find h2 'im-title' class")
        return
    results = library_soup.find('div', class_='im')
    if results is None:
        print("can't find 'im' class")
        return
    time.sleep(random.randint(3, 6))
    results = results.find_next_sibling(class_='grid')
    information_trs = results.find_all('tr')
    datetime = None
    for tr in information_trs:
        if 'Date' == tr.th.string:
            datetime = tr.td.string
            break
    return datetime


# update_release_time()