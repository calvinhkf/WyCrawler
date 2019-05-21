import os
import random
import time

import requests
from bs4 import BeautifulSoup

import database
from exception import CustomizeException
from file_util import read_json, write_json
from useragents import agents

new_data_dir = "E:/data/ASE2019/"
db = database.connectdb()

url = "https://mvnrepository.com"
res = requests.get(url)
cookies = dict(res.cookies.items())

def get_category():
    data = read_json(new_data_dir + "library_ids.txt")
    unsolved_ids = set()
    for id in data:
        sql = "SELECT distinct categories FROM library_versions WHERE library_id = " + str(id) + " and categories is not null"
        query_result = database.querydb(db, sql)
        if len(query_result) > 1:
            raise CustomizeException("category duplicate : " + str(id))
        elif len(query_result) <= 0:
            unsolved_ids.add(id)
        else:
            sql = "UPDATE library SET category = '" + query_result[0][0] + "' WHERE id = " + str(id)
            database.execute_sql(db, sql)
    print(len(unsolved_ids))
    write_json(new_data_dir + "unsolved_library_ids.txt", list(unsolved_ids))

def crawl_category():
    # data = read_json(new_data_dir + "library_ids.txt")
    # print(len(data))
    # # return
    # final = []
    # for id in data:
    #     if os.path.exists(new_data_dir + "category/" + str(id) + ".txt"):
    #         continue
    #     # if id < 8534:
    #     #     continue
    #     sql = "SELECT group_str,name_str FROM library WHERE id = " + str(id)
    #     lib_info = database.querydb(db, sql)
    #     groupId = lib_info[0][0]
    #     artifactId = lib_info[0][1]

    data = read_json(new_data_dir + "category/to_do_list.txt")
    go = False
    for entry in data:
        if entry == "org.geowebcache__fdse__gwc-sqlite":
            go = True
        if not go:
            continue
        groupId = entry.split("__fdse__")[0]
        artifactId = entry.split("__fdse__")[1]
        time.sleep(random.randint(2, 4))
        headers = {'User-Agent': random.choice(agents), 'Referer': 'https://mvnrepository.com/'}
        print(entry + " : " + "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId)
        library = requests.get("https://mvnrepository.com/artifact/" + groupId + "/" + artifactId, headers=headers, cookies=cookies)
        if library.status_code == 403:
            print("Exception status 403:" + "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId)
            os._exit(0)
        library_soup = BeautifulSoup(library.text, 'lxml')

        # library_soup = BeautifulSoup(library.text, 'lxml');
        name = None
        description = None
        results = library_soup.find(class_='im-title')
        if results is not None and results.a is not None:
            name = results.a.string.replace('\n', '')
        results = library_soup.find(class_='im-description')
        if results is not None:
            description = results.string
        if library_soup.find(class_='grid') is None:
            continue
        results = library_soup.find(class_='grid').find_all('tr')
        # license = None
        categories = []
        # tags = None
        for tr in results:
            if tr.th is not None:
                # if tr.th.string == 'License':
                #     license = tr.td.span.string.replace('\n', '')
                if tr.th.string == 'Categories':
                    if tr.td.a is not None:
                        categories.append(tr.td.a.string.replace('\n', ''))
                        # categories = "{'" + tr.td.a.string.replace('\n', '') + "':'" + "http://mvnrepository.com" + \
                        #              tr.td.a["href"] + "'}"
                # elif tr.th.string == 'Tags':
                #     entries = tr.td.find_all('a')
                #     if entries is not None:
                #         tags = "{"
                #         for each in entries:
                #             tags = tags + "'" + each.string.replace('\n', '') + "':'" + "http://mvnrepository.com" + \
                #                    each["href"] + "',"
                #         if tags[len(tags) - 1] == ",":
                #             tags = tags[:-1]
                #         tags = tags + "}"
        # obj = {}
        # obj["id"] = id
        # obj["groupId"] = groupId
        # obj["artifactId"] = artifactId
        # obj["name"] = name
        # obj["description"] = description
        # obj["license"] = license
        # obj["categories"] = categories
        # obj["tags"] = tags
        if len(categories) > 0:
            write_json(new_data_dir + "category/new/" + entry + ".txt", categories)
        # final.append(obj)
        # break


# get_category()
crawl_category()