import datetime
import json
import os
import random

import requests
import time

import urllib3
from bs4 import BeautifulSoup

import database
from exception import CustomizeException
from file_util import read_json, write_json, read_file, get_lib_name, save_lib
from useragents import agents
import sys
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

crawled_repo = []
repo_array = []

library_versions_list = []
version_types_list = []
unsolved_lib_list = []

curr_project_id = -1

db = database.connectdb()
urllib3.disable_warnings()

def handle_lib_by_range(start, end):
    global curr_project_id
    json_data = read_json("dependencies_list.txt")
    print(len(json_data))
    for i in range(start, end):
        print("+++++++++++++++++++++++++++++++ " + str(i))
        curr_project_id = i
        handle_one_lib(json_data[i])

def handle_one_lib(id):
    sql = "SELECT * FROM library_versions WHERE id = " + str(id)
    version_info = database.querydb(db, sql)
    if len(version_info) != 0:
        date = version_info[0][11]
        if date is not None:
            return
        repository = version_info[0][13]
        groupId = version_info[0][2]
        artifactId = version_info[0][3]
        version = version_info[0][4]
        update_date = get_update_time_for_lib(repository, groupId, artifactId, version)
        if update_date is not None:
            sql = "UPDATE library_versions SET date = \'" + str(update_date).replace("'", "''") + "\' WHERE id =" + str(id)
        # groupUrl = groupId.replace('.', '/')
        # list_page_url = repository + "/" + groupUrl + "/" + artifactId + "/" + version

def get_update_time_for_lib(repository ,groupId, artifactId, version):
    groupUrl = groupId.replace('.', '/')
    vesion_page_url = repository + "/" + groupUrl + "/" + artifactId + "/" + version
    maven_metadata_url = vesion_page_url + "/" + "maven-metadata.xml"
    headers = {'User-Agent': random.choice(agents)}
    meta_data = requests.get(maven_metadata_url, headers=headers, verify=False)
    if meta_data is not None:
        meta_data_soup = BeautifulSoup(meta_data.text, 'xml');
        snapshot_date = None
        if meta_data_soup.find('timestamp') is not None:
            snapshot_date = meta_data_soup.find('timestamp').string
        elif meta_data_soup.find('lastUpdated') is not None:
            snapshot_date = meta_data_soup.find('lastUpdated').string
        if snapshot_date is not None:
            return snapshot_date

    headers = {'User-Agent': random.choice(agents)}
    versions_data = requests.get(vesion_page_url, headers=headers)
    # print(versions_data.text)
    versions_data_soup = BeautifulSoup(versions_data.text, 'xml');
    date, update_date = None, None
    a_links = versions_data_soup.find_all('a')
    for a in a_links:
        if a.next_sibling is not None:
            info_str = a.next_sibling.string.strip()
            info_array = info_str.split(" ")
            if len(info_array) > 0:
                date_str = info_array[0]
                if date_str != '':
                    try:
                        d1 = datetime.datetime.strptime(date_str, '%d-%b-%Y')
                        if date is None:
                            date = d1
                        elif d1 > date:
                            date = d1
                    except:
                        print("Exception : strptime error")
    if date is not None:
        update_date = date.strftime("%Y-%b-%d")
    return update_date

def get_update_time_for_lib1(repository ,groupId, artifactId, version):
    groupUrl = groupId.replace('.', '/')
    vesion_page_url = repository + "/" + groupUrl + "/" + artifactId + "/" + version
    maven_metadata_url = vesion_page_url + "/" + "maven-metadata.xml"
    headers = {'User-Agent': random.choice(agents)}
    meta_data = requests.get(maven_metadata_url, headers=headers, verify=False)
    if meta_data is not None:
        meta_data_soup = BeautifulSoup(meta_data.text, 'xml');
        snapshot_date = None
        if meta_data_soup.find('timestamp') is not None:
            snapshot_date = meta_data_soup.find('timestamp').string
        elif meta_data_soup.find('lastUpdated') is not None:
            snapshot_date = meta_data_soup.find('lastUpdated').string
        if snapshot_date is not None:
            return snapshot_date

    headers = {'User-Agent': random.choice(agents)}
    versions_data = requests.get(vesion_page_url, headers=headers)
    # print(versions_data.text)
    versions_data_soup = BeautifulSoup(versions_data.text, 'xml');
    date, update_date = None, None
    a_links = versions_data_soup.find_all('a')
    for a in a_links:
        if a.parent is not None:
            time_td = a.parent.find_next_sibling('td')
            if time_td is not None:
                time_str = time_td.string
                # print(time_str)
                time_array = time_str.split(' ')
                if len(time_array) == 6:
                    temp = time_array[2]+"-"+time_array[1]+"-"+time_array[5]
                    # print(temp)
                    d1 = datetime.datetime.strptime(temp, '%d-%b-%Y')
                    if date is None:
                        date = d1
                    elif d1 > date:
                        date = d1
                else:
                    raise CustomizeException("len("+str(time_str)+") != 6")
    if date is not None:
        update_date = date.strftime("%Y-%b-%d")
    # print(update_date)
    return update_date

def crawl_date_for_one_repo(num1,num2):
    # count = 0
    do = False
    for i in range(num1,num2):
        json_data = read_json(str(i)+"_repo.txt")
        # count += len(json_data)
        print(len(json_data))
        for data in json_data:
            print(data)
            id = data[0]
            if id == 197067:
                do =True
            if not do:
                continue
            groupId = data[1]
            artifactId = data[2]
            version = data[3]
            repository = data[4]
            update_time = get_update_time_for_lib1(repository, groupId, artifactId, version)
            if update_time is not None:
                print(update_time)
                # print(id)
                sql = "UPDATE library_versions set date = '" + str(update_time)+"' where id ="+str(id)
                # database.execute_sql(db,sql)
                with open("crawled_time.txt", "a") as f:
                    f.write(str(sql) + "\n")
                f.close()
            # break

# numa = sys.argv[2]
# numb = sys.argv[3]
# 206442
# crawl_date_for_one_repo(6,7)
# 4 9 14 17
# 5 6 #7 #8 #10 #12 #13 #15 #16
# handle_lib_by_range(int(numa),int(numb))
# save_lib_package("{\"View\":\"http://bits.netbeans.org/nexus/content/groups/netbeans/org/netbeans/modules/org-netbeans-modules-spi-actions/RELEASE82/\"}", "nbm-file", None,"RELEASE82")