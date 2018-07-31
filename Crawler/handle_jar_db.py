import json

import os
import random

import requests
import time

import database
from exception import CustomizeException
from bs4 import BeautifulSoup

from file_util import save_lib, get_lib_name, read_json, read_file

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
db = database.connectdb()
repo_dir = "E:/data/repo"

def insert_project_lib_usage(project_id, version_type_id, module_):
    sql = "SELECT * FROM project_lib_usage WHERE project_id = '" + str(project_id) +"' and version_type_id = " + str(version_type_id)
    record = database.querydb(db, sql)
    if len(record) == 0:
        if module_ is None:
            sql = "INSERT INTO project_lib_usage (project_id,version_type_id) VALUES ('" + str(project_id) + "','" + str(version_type_id) + "')"
        else:
            sql = "INSERT INTO project_lib_usage (project_id,version_type_id,module) VALUES ('" + str(project_id) + "','" + str(version_type_id) + "','"+ str(module_) + "')"
        database.execute_sql(db, sql)
        print('======================== INSERT INTO project_lib_usage : ' + str(project_id) + "  " + str(version_type_id))


def insert_version_type(version_id,_type,classifier,jar_package_url):
    if classifier is None:
        sql = "INSERT INTO version_types" \
              "(version_id,type,classifier,jar_package_url) " \
              "VALUES (\'" \
              + str(version_id).replace("'", "''") + "\',\'" \
              + str(_type).replace("'", "''") + "\',NULL,\'" \
              + str(jar_package_url).replace("'", "''") + "\')"
    else:
        sql = "INSERT INTO version_types" \
              "(version_id,type,classifier,jar_package_url) " \
              "VALUES (\'" \
              + str(version_id).replace("'", "''") + "\',\'" \
              + str(_type).replace("'", "''") + "\',\'" \
              + str(classifier).replace("'", "''") + "\',\'" \
              + str(jar_package_url).replace("'", "''") + "\')"
    database.execute_sql(db, sql)
    print('======================== INSERT INTO version_types : ' + str(version_id) + "  " + str(_type)+"  " + str(classifier)+"  " + str(jar_package_url))
    sql = "SELECT LAST_INSERT_ID()"
    results = database.querydb(db, sql)
    return results[0][0]

def insert_library_version(group,name1,version1,version_url,license,categories,organization,home_page,date,files,repository,used_by,category_url):
    sql = "SELECT * FROM library_versions WHERE group_str = '" + str(group) + "' and name_str = '" + str(
        name1) + "' and version = '" + str(version1) + "'"
    version_info = database.querydb(db, sql)
    if len(version_info) != 0:
        return version_info[0][0]
    else:
        sql = "INSERT INTO library_versions" \
              "(group_str,name_str,version,url,license,categories,organization,home_page,date,files,repository,used_by,category_url) " \
              "VALUES (\'" \
              + str(group).replace("'", "''") + "\',\'" \
              + str(name1).replace("'", "''") + "\',\'" \
              + str(version1).replace("'", "''") + "\',\'" \
              + str(version_url).replace("'", "''") + "\',"

        if license is not None:
            sql += "\'" + str(license).replace("'", "''") + "\',"
        else:
            sql += "NULL,"
        if categories is not None:
            sql += "\'" + str(categories).replace("'", "''") + "\',"
        else:
            sql += "NULL,"
        if organization is not None:
            sql += "\'" + str(organization).replace("'", "''") + "\',"
        else:
            sql += "NULL,"
        if home_page is not None:
            sql += "\'" + str(home_page).replace("'", "''") + "\',"
        else:
            sql += "NULL,"
        if date is not None:
            sql += "\'" + str(date).replace("'", "''") + "\',"
        else:
            sql += "NULL,"
        if files is not None:
            sql += "\'" + str(files).replace("'", "''") + "\',"
        else:
            sql += "NULL,"
        if repository is not None:
            sql += "\'" + str(repository).replace("'", "''") + "\',"
        else:
            sql += "NULL,"
        if used_by is not None:
            sql += "\'" + str(used_by).replace("'", "''") + "\',"
        else:
            sql += "NULL,"
        if category_url is not None:
            sql += "\'" + str(category_url).replace("'", "''") + "\')"
        else:
            sql += "NULL)"
        database.execute_sql(db, sql)
        print('======================== INSERT INTO library_versions :' + str(group) + "  " + str(name1)+"  " + str(version1))
        sql = "SELECT LAST_INSERT_ID()"
        results = database.querydb(db, sql)
        return results[0][0]

def insert_unsolved_library(group,name1,version1,_type,classifier,project_id):
    if classifier is None:
        sql = "SELECT * FROM unsolved_libraries WHERE group_str = '" + str(group) + "' and name_str = '" + str(
        name1) +"' and version = '"+str(version1)+"' and type = '"+str(_type)+"' and classifier = NULL"
    else:
        sql = "SELECT * FROM unsolved_libraries WHERE group_str = '" + str(group) + "' and name_str = '" + str(
        name1) +"' and version = '"+str(version1)+"' and type = '"+str(_type)+"' and classifier = '"+str(classifier)+"'"
    record = database.querydb(db, sql)
    if len(record) == 0:
        sql = "INSERT INTO unsolved_libraries" \
              "(project_id, group_str,name_str,version,type,classifier) " \
              "VALUES (\'" \
              + str(project_id).replace("'", "''") + "\',\'" \
              + str(group).replace("'", "''") + "\',\'" \
              + str(name1).replace("'", "''") + "\',\'" \
              + str(version1).replace("'", "''") + "\',\'" \
              + str(_type).replace("'", "''") + "\',"
        if classifier is not None:
            sql += "\'" + str(classifier).replace("'", "''") + "\')"
        else:
            sql += "NULL)"
        database.execute_sql(db, sql)
        print('======================== INSERT INTO unsolved_libraries :' + str(group) + "  " + str(name1)+"  " + str(version1)+"  " + str(_type)+"  " + str(classifier))

def download_lib_from_list(lib_list,page_path,_type,classifier):
    success = False
    package_url = None

    for lib_package in lib_list:
        if _type == "test-jar" and lib_package.endswith(
                ".jar") and "-sources" not in lib_package and "-javadoc" not in lib_package and "tests" in lib_package:
            url = None
            if classifier is not None:
                if classifier in lib_package:
                    url = page_path + "/" + lib_package
            else:
                url = page_path + "/" + lib_package
            if url is not None:
                package_url = lib_package
                if not os.path.exists("F:/GP/lib/" + lib_package):
                    save_lib(url, "F:/GP/lib/" + lib_package)
                success = True
                break
        elif lib_package.endswith("." + _type) and "-sources" not in lib_package and "-javadoc" not in lib_package:
            url = None
            if classifier is not None:
                if classifier in lib_package:
                    url = page_path + "/" + lib_package
            else:
                url = page_path + "/" + lib_package
            if url is not None:
                package_url = lib_package
                if not os.path.exists("F:/GP/lib/" + lib_package):
                    save_lib(url, "F:/GP/lib/" + lib_package)
                success = True
                break
    return success, package_url

def get_lib_from_list_page(page_path,_type,classifier):
    success = False
    package_url = None
    time.sleep(random.randint(2, 5))
    lib_list = get_lib_list_of_one_version(page_path)
    return download_lib_from_list(lib_list, page_path, _type, classifier)

def save_lib_package(files, version_id, _type, classifier, project_id, module_):
    file_list = json.loads(files)
    if _type in file_list:
        jar_url = file_list[_type]
        if not os.path.exists("F:/GP/lib/" + get_lib_name(jar_url)):
            save_lib(jar_url, "F:/GP/lib/" + get_lib_name(jar_url))
        version_type_id = insert_version_type(version_id, _type, classifier, get_lib_name(jar_url))
        insert_project_lib_usage(project_id, version_type_id, module_)
        return
    if _type == "tar.gz" or _type == "zip" or _type == "jar" or _type == "test-jar":
        if 'View' in file_list:
            page_url = file_list['View']
            success,package_url = get_lib_from_list_page(page_url, _type, classifier)
            if success:
                version_type_id = insert_version_type(version_id, _type, classifier, get_lib_name(package_url))
                insert_project_lib_usage(project_id, version_type_id, module_)
    # if _type == "xml":
    #     return
    else:
        # print("!!!!!!!!!!!!!!!!!!!! unhandled type: " + str(_type))
        raise (CustomizeException("!!!!!!!!!!!!!!!!!!!! unhandled type: " + str(_type)))

def library_crawler(groupId, artifactId, version, _type, classifier, project_id, module_):
    print("groupId: " + str(groupId) + ", artifactId: " + str(artifactId) + ", version: " + str(
            version) + ", type: " + str(_type) + ", classifier: " + str(classifier)+ ", module: " + str(module_))
    version_url = "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId + "/" + version
    print(version_url)
    sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId)+"' and name_str = '"+str(artifactId)+"' and version = '"+str(version)+"'"
    version_info = database.querydb(db, sql)
    if len(version_info) != 0:
        version_id = version_info[0][0]

        print("+++++++++++++++++++++++++version_id:" +str(version_id))
        sql = "SELECT * FROM version_types WHERE version_id = " + str(version_id)
        types = database.querydb(db, sql)
        for t in types:
            if t[2] == _type:
                if (classifier is not None and classifier == t[3]) or (classifier == None and t[3] == None):
                    insert_project_lib_usage(project_id, t[0], module_)
                    return
        files = version_info[0][12]
        if files != None:
            save_lib_package(files, version_id, _type, classifier, project_id, module_)
        else:
            get_lib_from_other_repo(version_id, groupId, artifactId, version, _type, classifier, project_id, module_)

    else:
        get_lib_from_maven_repo(groupId, artifactId, version, _type, classifier, project_id, module_)
    # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

def get_lib_from_maven_repo(groupId, artifactId, version, _type, classifier, project_id, module_):
    version_url = "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId + "/" + version
    library_version = requests.get(version_url, headers=headers)
    library_soup = BeautifulSoup(library_version.text, 'lxml');
    category_url = None
    if library_soup.find('h2', class_='im-title') is None:
        print("can't find h2 'im-title' class")
        get_lib_from_other_repo(-1, groupId, artifactId, version, _type, classifier, project_id, module_)
        return
    titles = library_soup.find('h2', class_='im-title').find_all('a')
    if titles[len(titles) - 1].get_text() == version:
        if len(titles) - 2 >= 0:
            category_url = "https://mvnrepository.com" + titles[len(titles) - 2]["href"]
            print("category_url:" + category_url)
    results = library_soup.find('div', class_='im')
    if results is None:
        print("can't find 'im' class")
        get_lib_from_other_repo(-1, groupId, artifactId, version, _type, classifier, project_id, module_)
        return
        # raise (CustomizeException("can't find 'im' class"))
    time.sleep(random.randint(10, 18))
    results = results.find_next_sibling(class_='grid')
    information_trs = results.find_all('tr')
    license, categories, organization, home_page, files, used_by = None, None, None, None, None, None
    for tr in information_trs:
        if 'License' == tr.th.string:
            license = ''
            spans = tr.td.find_all('span')
            for span in spans:
                license = license + span.string + ','
            if license[len(license) - 1] == ',':
                license = license[:-1].replace('\n', '')
        if 'Categories' == tr.th.string:
            categories = "{\"" + tr.td.a.string.replace('\n', '') + "\":\"" + "http://mvnrepository.com" + tr.td.a[
                "href"] + "\"}"
        if 'Organization' == tr.th.string:
            if tr.td.a is None:
                organization = "{\"" + tr.td.string.replace('\n', '') + "\":\"\"}"
            else:
                organization = "{\"" + tr.td.a.string.replace('\n', '') + "\":\"" + tr.td.a["href"] + "\"}"
        if 'HomePage' == tr.th.string:
            if tr.td.a is None:
                home_page = tr.td.string.replace('\n', '')
            else:
                home_page = tr.td.a["href"]
        if 'Date' == tr.th.string:
            date = tr.td.string
        if 'Files' == tr.th.string:
            entries = tr.td.find_all('a')
            if entries is not None:
                files = "{"
                for each in entries:
                    file_type = each.get_text().replace('\n', '').split(' ')[0]
                    files = files + "\"" + file_type + "\":\"" + each["href"] + "\","
                if files[len(files) - 1] == ",":
                    files = files[:-1]
                files = files + "}"
        # if 'Repositories' == tr.th.string:
        #     entries = tr.td.find_all('a')
        #     if entries is not None:
        #         repository = "{"
        #         for each in entries:
        #             repository = repository + "\"" + each.string.replace('\n',
        #                                                                  '') + "\":\"" + "http://mvnrepository.com" + \
        #                          each["href"] + "\","
        #         if repository[len(repository) - 1] == ",":
        #             repository = repository[:-1]
        #             repository = repository + "}"
        if 'Used By' == tr.th.string:
            used_by = "{\"" + tr.td.a.string.replace('\n', '') + "\":\"" + "http://mvnrepository.com" + tr.td.a[
                "href"] + "\"}"
    print('    license:' + str(license))
    print('    categories:' + str(categories))
    print('    organization:' + str(organization))
    print('    home_page:' + str(home_page))
    print('    date:' + str(date))
    print('    files:' + str(files))
    print('    used_by:' + str(used_by))
    repository = None
    time.sleep(random.randint(15, 20))
    library = requests.get("https://mvnrepository.com/artifact/" + groupId + "/" + artifactId, headers=headers)
    library_soup = BeautifulSoup(library.text, 'lxml');
    results = library_soup.find('ul', class_='tabs').find_all('li')
    for tab in results:
        temp = get_other_library_versions_in_maven("http://mvnrepository.com" + tab.a["href"], "https://mvnrepository.com/artifact/" + groupId + "/" + artifactId,groupId,artifactId,version)
        if temp is not None:
            repository = temp

    version_id = insert_library_version(groupId, artifactId, version, version_url, license, categories, organization,
                                        home_page, date,
                                        files, repository, used_by, category_url)
    save_lib_package(files, version_id, _type, classifier, project_id, module_)

def get_other_library_versions_in_maven(tab_url, category_url,groupId,artifactId, target_version):
    target_version_repo = None
    time.sleep(random.randint(12, 15))
    print('------------------------- tab_url:'+tab_url)
    library_tab = requests.get(tab_url, headers=headers)
    library_soup = BeautifulSoup(library_tab.text, 'lxml');
    results = library_soup.find(class_='grid versions')
    version_idx, repository_idx, usages_idx, date_idx = -1, -1, -1, -1
    ths = results.thead.find_all('th')
    for i in range(0, len(ths)):
        if 'Version' == ths[i].string:
            version_idx = i
        if 'Repository' == ths[i].string:
            repository_idx = i
        if 'Usages' == ths[i].string:
            usages_idx = i
        if 'Date' == ths[i].string:
            date_idx = i
    if (version_idx == -1 or repository_idx == -1 or usages_idx == -1 or date_idx == -1):
        raise (CustomizeException("Version Repository Usages Date imcomplete"))
    tbodys = results.find_all('tbody')
    # bi = 0
    for body in tbodys:
        # bi = bi + 1
        # if bi < 21:
        #     continue
        trs = body.find_all('tr')
        # tri = 0
        for tr in trs:
            # tri = tri + 1
            # if bi == 21 and tri < 29:
            # # if tri < 6:
            #     continue
            tds = tr.find_all('td')
            tr_version = version_idx
            tr_repository = repository_idx
            tr_usages = usages_idx
            tr_date = date_idx
            if(ths[0].string is None):
                if (tds[0].a is not None):
                    tr_version = tr_version - 1
                    tr_repository = tr_repository - 1
                    tr_usages = tr_usages - 1
                    tr_date = tr_date - 1
            version_url = category_url[0:category_url.rindex('/')] + '/' + tds[tr_version].a["href"]
            version = tds[tr_version].a.string.replace('\n', '')
            repository = "http://mvnrepository.com" + tds[tr_repository].a["href"]
            usages = None
            if tds[tr_usages].a is None:
                usages = "{'" + tds[tr_usages].get_text().replace('\n', '') + "':''}"
            else:
                usages = "{'" + tds[tr_usages].a.string.replace('\n', '') + "':'" + category_url + tds[tr_usages].a["href"] + "'}"
            date = tds[tr_date].string.replace('\n', '')
            time.sleep(random.randint(8, 10))
            library_version = requests.get(version_url, headers=headers)
            page = library_version.text
            library_soup = BeautifulSoup(library_version.text, 'lxml');
            results = library_soup.find('div', class_='im')
            if results is None:
                raise (CustomizeException("can't find 'im' class"))
                # print("can't find 'im' class")
                # return
            results = results.find_next_sibling(class_='grid')
            information_trs = results.find_all('tr')
            license, categories, organization, home_page, files, used_by = None, None, None, None, None, None
            for tr in information_trs:
                if 'License' == tr.th.string:
                    license =''
                    spans = tr.td.find_all('span')
                    for span in spans:
                        license = license + span.string + ','
                    if license[len(license)-1] == ',':
                        license = license[:-1].replace('\n', '')
                if 'Categories' == tr.th.string:
                    categories = "{'" + tr.td.a.string.replace('\n', '') + "':'" + "http://mvnrepository.com" + tr.td.a["href"] + "'}"
                if 'Organization' == tr.th.string:
                    if tr.td.a is None:
                        organization = "{'" + tr.td.string.replace('\n', '') + "':''}"
                    else:
                        organization = "{'" + tr.td.a.string.replace('\n', '') + "':'" + tr.td.a["href"] + "'}"
                if 'HomePage' == tr.th.string:
                    if tr.td.a is None:
                        home_page = tr.td.string.replace('\n', '')
                    else:
                        home_page = tr.td.a["href"]
                if 'Date' == tr.th.string:
                    date = tr.td.string
                if 'Files' == tr.th.string:
                    entries = tr.td.find_all('a')
                    if entries is not None:
                        files = "{"
                        for each in entries:
                            files = files + "'" + each.get_text().replace('\n', '') + "':'" + each["href"] + "',"
                        if files[len(files) - 1] == ",":
                            files = files[:-1]
                        files = files + "}"
                if 'Used By' == tr.th.string:
                    used_by = "{'" + tr.td.a.string.replace('\n', '') + "':'" + "http://mvnrepository.com" + tr.td.a["href"] + "'}"
            print('    license:', end="")
            print(license)
            print('    categories:', end="")
            print(categories)
            print('    organization:', end="")
            print(organization)
            print('    home_page:', end="")
            print(home_page)
            print('    date:', end="")
            print(date)
            print('    files:', end="")
            print(files)
            print('    repository:', end="")
            print(repository)
            print('    used_by:', end="")
            print(used_by)
            if target_version == version:
                target_version_repo = repository
            else:
                insert_library_version(groupId, artifactId, version, version_url, license, categories, organization,
                                   home_page, date,files, repository, used_by, category_url)
    return target_version_repo

def get_lib_from_other_repo(version_id,groupId, artifactId, version, _type, classifier, project_id, module_):
    success = False
    repo_file = repo_dir + "/" + str(project_id) + ".txt"
    if os.path.exists(repo_file):
        lines = read_file(repo_file)
        for i in range(len(lines)):
            repo_url = lines[i]
            # groupUrl = groupId.replace('.', '/')
            # list_page_url = repo_url + "/" + groupUrl + "/" + artifactId + "/" + version
            if not repo_url.startswith("https://") and not repo_url.startswith("http://"):
                repo_url = "http://" + repo_url
            success = save_lib_in_other_repo(repo_url, version_id, groupId, artifactId, version, _type, classifier,
                                   project_id, module_)
            if success:
                break
    if not success:
        insert_unsolved_library(groupId, artifactId, version, _type, classifier, project_id)


def save_lib_in_other_repo(repo_url, version_id, groupId, artifactId, version, _type, classifier, project_id, module_):
    groupUrl = groupId.replace('.', '/')
    list_page_url = repo_url + "/" + groupUrl + "/" + artifactId + "/" + version
    lib_list = get_lib_list_of_one_version(list_page_url)
    maven_metadata_url = list_page_url + "/" + "maven-metadata.xml"
    snapshot_date = None
    success = False
    try:
        meta_data = requests.get(maven_metadata_url, headers=headers)
        if meta_data is not None:
            meta_data_soup = BeautifulSoup(meta_data.text, 'xml');
            snapshot_date = None
            if meta_data_soup.find('timestamp') is not None:
                snapshot_date = meta_data_soup.find('timestamp').string
            snapshot_versions = meta_data_soup.find_all('snapshotVersion')
            for snapshot_version in snapshot_versions:
                snapshot_type = snapshot_version.extension.string
                if snapshot_type == _type:
                    snapshot_classifier = None
                    if snapshot_version.classifier is not None:
                        snapshot_classifier = snapshot_version.classifier.string

                    version_num = snapshot_version.value.string
                    package_url = None
                    if classifier is None and snapshot_classifier is None:
                        package_url = artifactId + "-" + version_num + "." + _type
                    elif classifier is not None and snapshot_classifier is not None and classifier == snapshot_classifier:
                        package_url = artifactId + "-" + version_num + "-" + classifier + "." + _type
                    if package_url is None:
                        continue

                    print(package_url)
                    lib_name = None
                    if package_url in lib_list:
                        if not os.path.exists("F:/GP/lib/" + package_url):
                            save_lib(list_page_url + "/" + package_url, "F:/GP/lib/" + package_url)
                        success = True
                        lib_name = package_url
                    else:
                        success, lib_name = download_lib_from_list(lib_list, list_page_url, _type, classifier)
                    if success:
                        if version_id < 0:
                            # other versions
                            library_url = list_page_url[0:list_page_url.rindex('/')]
                            get_other_library_versions_in_other_repo(repo_url,library_url, groupId, artifactId, version)

                            version_id = insert_library_version(groupId, artifactId, version, list_page_url, None,
                                                                None, None, None, snapshot_date, None, repo_url,
                                                                None, None)

                        sql = "SELECT * FROM version_types WHERE version_id = " + str(version_id)
                        types = database.querydb(db, sql)
                        for t in types:
                            if t[2] == _type:
                                if (classifier is not None and classifier == t[3]) or (
                                        classifier == None and t[3] == None):
                                    insert_project_lib_usage(project_id, t[0], module_)
                                    return success
                        version_type_id = insert_version_type(version_id, _type, classifier,
                                                              get_lib_name(lib_name))
                        insert_project_lib_usage(project_id, version_type_id, module_)


                    break
    except Exception as e:
        meta_data = None
    return success

def get_other_library_versions_in_other_repo(repo_url,library_url, groupId,artifactId, target_version):
    versions_meta_url = library_url + "/" + "maven-metadata.xml"
    try:
        time.sleep(random.randint(3, 6))
        versions_meta_data = requests.get(versions_meta_url, headers=headers)
        if versions_meta_data is not None:
            meta_data_soup = BeautifulSoup(versions_meta_data.text, 'xml');
            versions = meta_data_soup.find_all('version')
            version_list = []
            for v in versions:
                version_list.append(v.string)
            for ver in version_list:
                if ver != target_version:
                    version_detail_url = library_url + "/" + ver
                    version_detail_meta_url = version_detail_url + "/" + "maven-metadata.xml"
                    time.sleep(random.randint(3, 6))
                    versions_meta_data = requests.get(version_detail_meta_url, headers=headers)
                    meta_data_soup = BeautifulSoup(versions_meta_data.text, 'xml');
                    update_date = None
                    if meta_data_soup.find('timestamp') is not None:
                        update_date = meta_data_soup.find('timestamp').string
                    insert_library_version(groupId, artifactId, ver, version_detail_url, None,
                                                    None, None, None, update_date, None, repo_url,
                                                    None, None)
    except Exception as e:
        versions_meta_data = None

def get_lib_list_of_one_version(path):
    newlist = []
    try:
        time.sleep(random.randint(2, 5))
        page = requests.get(path, headers=headers)
        soup = BeautifulSoup(page.text, 'lxml');
        list = soup.find_all('a')
        for li in list:
            newlist.append(li.get_text())
    except Exception as e:
        print('no use repo: '+str(path))
    return newlist

def get_lib_usedby_project(path):
    if not os.path.exists(path):
        return
    print()
    data = read_json(path)
    project_id = None
    module_ = None
    do = False
    for lib in data:
        if 'id' in lib:
            project_id = lib["id"]
            print("-------------------- project_id: " + str(project_id))
            continue
        if "groupId" not in lib or "artifactId" not in lib or "version" not in lib:
            print(False)
            continue
        groupId= lib["groupId"]
        artifactId = lib["artifactId"]
        version = lib["version"]
        type_ = lib["type"]
        if groupId is None or artifactId is None or version is None or type_ is None or '${' in groupId or '${' in artifactId or '${' in version or '${' in type_:
            print("groupId: " + str(groupId) +"   artifactId: " + str(artifactId)+"   version: " + str(version)+"   type: " + str(type_) )
            print(False)
            continue
        if project_id is None:
            continue
        classifier = None

        if "classifier" in lib:
            classifier = lib["classifier"]
            if '${' in classifier:
                print("groupId: " + str(groupId) + "   artifactId: " + str(artifactId) + "   version: " + str(
                    version) + "   type: " + str(type_) + "   classifier: " + str(classifier))
                print(False)
                continue
        if "module" in lib:
            module_ = lib["module"]
        # if not do:
        #     if artifactId == "apex-common" and groupId == "org.apache.apex":
        #         do = True
        #     else:
        #         continue
        # if do:
        if type(version) == list:
            continue
            # for ver in version:
            #     save_version_information(groupId, artifactId, ver, type_, classifier, project_id, module_)
        else:
            library_crawler(groupId, artifactId, version, type_, classifier, project_id, module_)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# save_version_information("org.apache.mina", "mina-integration-beans", "2.0.17", "jar", None,1)
# read_used_library()
#1139 649 1213 492 654 1261 1265
# for i in range(1, 2):
#     get_lib_usedby_project("E:/data/curr_result_all/"+str(i)+".txt")
# print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
# get_lib_usedby_project("C:/Users/yw/Desktop/result/"+str(4)+".txt")
# package = requests.get("https://oss.sonatype.org/content/repositories/snapshots/consulting/omnia/util/util-io/1.0-SNAPSHOT/util-io-1.0-20150804.045928-1.pom", headers=headers)
# print(package.content)
# print(package.text)
# page = requests.get("http://central.maven.org/maven2/org/apache/zookeeper/zookeeper/3.4.10/", headers=headers)
# soup = BeautifulSoup(page.text, 'lxml');
# list = soup.find_all('a')
# newlist = []
# for li in list:
#     newlist.append(li.get_text())
#     print(li.get_text())
# print("zookeeper-3.4.10-javadoc.jar" in newlist)
# print("zar" in newlist)
# insert_library_version("test", "test", "test", "test", None,None, None, None, "test", None, None,
#                                                                 None, None)
# get_lib_from_maven_repo("com.actionbarsherlock", "actionbarsherlock", "4.4.0", "apklib", None, 1, "actionbarsherlock-samples/demos")

# get_lib_from_other_repo(-1,"capital.scalable", "spring-auto-restdocs-core", "1.0.14-SNAPSHOT", "jar", None, 1, "")
# save_lib_in_other_repo("https://oss.sonatype.org/content/repositories/snapshots",-1,"capital.scalable", "spring-auto-restdocs-core", "1.0.14-SNAPSHOT", "jar", None, 1, "")