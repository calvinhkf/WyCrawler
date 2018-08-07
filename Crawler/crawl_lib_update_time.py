import datetime
import json
import os
import random

import requests
import time

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

# db = database.connectdb()

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
    headers = {'User-Agent': random.choice(agents)}
    versions_data = requests.get(vesion_page_url, headers=headers)
    print(versions_data.text)
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
                    d1 = datetime.datetime.strptime(date_str, '%d-%b-%Y')
                    if date is None:
                        date = d1
                    elif d1 > date:
                        date = d1
    if date is not None:
        update_date = date.strftime("%Y-%b-%d")
    return update_date

# numa = sys.argv[2]
# numb = sys.argv[3]
get_update_time_for_lib("https://repo.boundlessgeo.com/main", "org.geotools", "gt-arcsde-common", "12.0")
# handle_lib_by_range(int(numa),int(numb))
# save_lib_package("{\"View\":\"http://bits.netbeans.org/nexus/content/groups/netbeans/org/netbeans/modules/org-netbeans-modules-spi-actions/RELEASE82/\"}", "nbm-file", None,"RELEASE82")