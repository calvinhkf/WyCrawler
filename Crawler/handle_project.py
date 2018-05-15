import json
import mysql.connector

import database
import time

from bs4 import BeautifulSoup

from handle_jar import download_lib
from file_util import read_json

db = database.connectdb()


def read_project_lib_from_file(path):
    data = read_json(path)
    for lib in data:
        if 'id' in lib:
            continue
        groupId = lib["groupId"]
        artifactId = lib["artifactId"]
        version = lib["version"]
        _type = None
        classifier=None
        if 'type' in lib:
            _type = lib["type"]
        if 'classifier' in lib:
            classifier = lib["classifier"]
        download_lib(groupId, artifactId, version, _type,classifier)


def connect_server_db():
    print('连接到mysql服务器...')
    db = mysql.connector.connect(host="10.141.221.73", port="3306", user="root", passwd="root", database="codehub")
    print('连接成功!')
    return db


def get_project_path_from_db():
    list = []
    for i in range(90001, 120001):
        sql = "SELECT id,repository_id,local_addr,git_addr,stars,forks_count,watchers_count,issues_count FROM repository_java WHERE id = " + str(
            i)
        print('\n++++++++++++++++++++++++++++++++++++++++++++ id : ' + str(i))
        results = database.querydb(db, sql)
        for item in results:
            # print(item)
            info = {}
            info["id"] = item[0]
            info["repository_id"] = item[1]
            info["local_addr"] = item[2]
            info["git_addr"] = item[3]
            info["stars"] = item[4]
            info["forks_count"] = item[5]
            info["watchers_count"] = item[6]
            info["issues_count"] = item[7]
            # print(item[2])
            # print(item[3])
            # print(item[4])
            list.append(info)
    jsonStr = json.dumps(list)
    f = open("project.txt", 'w', encoding='utf-8')
    f.write(jsonStr)
    f.close()
    # def write_file(file_path, content):
    #     f = open(file_path, 'w', encoding='utf-8')
    #     f.write(content)
    #     f.close()


def read_library_url_from_db():
    for i in range(1, 10001):
        sql = "SELECT * FROM library_versions1 WHERE id = " + str(i)
        print('\n++++++++++++++++++++++++++++++++++++++++++++ ' + str(i))
        results = database.querydb(db, sql)
        for item in results:
            soup = BeautifulSoup(item[13], 'lxml');
            maven = soup.find(id='maven-a').string
            # print(maven)
            soup = BeautifulSoup(maven, 'xml');
            group = soup.find('groupId').string
            name = soup.find('artifactId').string
            version = soup.find('version').string
            print(group)
            print(name)
            print(version)
            # print(item[1])
            sql = "INSERT INTO library_versions" \
                  "(category_id,group_str,name_str,version,url,usages,license,categories,organization,home_page,date,files,repository,used_by,declarations," \
                  "compile_dependencies_table," \
                  "provided_dependencies_table," \
                  "test_dependencies_table," \
                  "managed_dependencies_table," \
                  "licenses_table," \
                  "developers_table," \
                  "mailing_lists_table," \
                  "page) " \
                  "VALUES (\'" \
                  + str(item[1]).replace("'", "''") + "\',\'" \
                  + str(group).replace("'", "''") + "\',\'" \
                  + str(name).replace("'", "''") + "\',\'" \
                  + str(version).replace("'", "''") + "\',\'" \
                  + str(item[3]).replace("'", "''") + "\',\'" \
                  + str(item[4]).replace("'", "''") + "\',\'" \
                  + str(item[5]).replace("'", "''") + "\',\'" \
                  + str(item[6]).replace("'", "''") + "\',\'" \
                  + str(item[7]).replace("'", "''") + "\',\'" \
                  + str(item[8]).replace("'", "''") + "\',\'" \
                  + str(item[9]).replace("'", "''") + "\',\'" \
                  + str(item[10]).replace("'", "''") + "\',\'" \
                  + str(item[11]).replace("'", "''") + "\',\'" \
                  + str(item[12]).replace("'", "''") + "\',\'" \
                  + str(item[13]).replace("'", "''") + "\',\'" \
                  + str(item[14]).replace("'", "''") + "\',\'" \
                  + str(item[15]).replace("'", "''") + "\',\'" \
                  + str(item[16]).replace("'", "''") + "\',\'" \
                  + str(item[17]).replace("'", "''") + "\',\'" \
                  + str(item[18]).replace("'", "''") + "\',\'" \
                  + str(item[19]).replace("'", "''") + "\',\'" \
                  + str(item[20]).replace("'", "''") + "\',\'" \
                  + str(item[21]).replace("'", "''") + "\')"
            database.execute_sql(db, sql)
            print('======================== INSERT INTO library_versions ')
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def query_test():
    sql = "SELECT id,category_id FROM library_versions WHERE group_str = \'org.slf4j\' and name_str=\'slf4j-api\' and version=\'1.6.6\'"
    results = database.querydb(db, sql)
    for item in results:
        print(item[0])


# read_project_lib_from_file("C:/Users/yw/Desktop/result/414.txt")