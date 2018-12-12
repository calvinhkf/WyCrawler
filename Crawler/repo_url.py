import requests

import database
from exception import CustomizeException
from bs4 import BeautifulSoup

from file_util import write_json, read_json

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
repo_dir = "E:/data/repo"
db = database.connectdb()

def get_repo_url_from_maven(repo_page):
    repository_url = None
    repo_info = requests.get(repo_page, headers=headers)
    repo_soup = BeautifulSoup(repo_info.text, 'lxml');
    if repo_soup.find('table') is not None:
        table = repo_soup.find('table')
        if table.find('tr') is not None:
            tr = table.find('tr')
            # th = tr.find('th')
            td = tr.find('td')
            content = td.get_text().strip().replace("\\","/")
            if content.endswith("/"):
                content = content[:-1]
            if content.startswith("http"):
                repository_url = content
                # print(repository_url)
    else:
        raise CustomizeException("can't find tbody")
    return repository_url

def repo_url_in_db():
    repo_list = []
    sql = "SELECT DISTINCT (repository) FROM library_versions"
    query_result = database.querydb(db,sql)
    for record in query_result:
        url = record[0]
        print(url)
        repo_list.append(url)
    write_json("repo_list.txt",repo_list)

def repo_url_count():
    count = 0
    json_data = read_json("repo_list.txt")
    print(len(json_data))
    for record in json_data:
        # if record.startswith("http://mvnrepository.com/repos/"):
        print(record)
        count += 1
    print(count)

def crawl_maven_repo_url():
    repo_dict = {}
    count = 0
    json_data = read_json("repo_list.txt")
    print(len(json_data))
    for record in json_data:
        if record.startswith("http://mvnrepository.com/repos/"):
            print(record)
            repo_url = get_repo_url_from_maven(record)
            if repo_url is not None:
                repo_dict[record] = repo_url
                print("+++++++++++++++++++++++++ "+repo_url)
                count += 1
    print(count)
    write_json("repo_dic.txt", repo_dict)

def update_url_in_db():
    json_data = read_json("repo_dic.txt")
    print(len(json_data))
    for key in json_data.keys():
        print(key)
        value = json_data[key]
        print(value)
        sql = "UPDATE library_versions set repository = '"+value+"' where repository = '" + key +"'"
        database.execute_sql(db,sql)

def duplicate_repo_url_in_db():
    json_data = read_json("repo_list.txt")
    print(len(json_data))
    for url in json_data:
        if url.startswith("https"):
            new_url = url.replace("https", "http")
            if new_url in json_data:
                print(url)

def update_repo_url_dic():
    repo_dic = read_json("repo_dic.txt")
    print(len(repo_dic))
    repo_dic["http://mvnrepository.com/repos/locationtech-releases"] = "https://repo.locationtech.org/content/repositories/releases"
    repo_dic["http://mvnrepository.com/repos/onebusaway-releases"] = "http://nexus.onebusaway.org/nexus/content/repositories/releases"
    repo_dic["http://mvnrepository.com/repos/mapr-drill"] = "https://repository.mapr.com/nexus/content/repositories/drill"
    repo_dic["http://mvnrepository.com/repos/imagej-public"] = "https://maven.imagej.net/content/repositories/public"
    print(len(repo_dic))
    write_json("repo_dic.txt",repo_dic)

# get_repo_url_from_maven("http://mvnrepository.com/repos/boundless")
# duplicate_repo_url_in_db()
# repo_url_count()
# crawl_maven_repo_url()
# update_url_in_db()
# update_repo_url_dic()