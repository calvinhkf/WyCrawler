import os

import database
from crawled_library_to_db import in_unsolved_table
from exception import CustomizeException
from file_util import read_json, write_json

db = database.connectdb()
from handle_jar_db import insert_project_lib_usage

def search_library_version_in_db(groupId,artifactId,version):
    sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
        artifactId) + "' and version = '" + str(version) + "'"
    version_info = database.querydb(db, sql)
    if len(version_info) != 0:
        return version_info[0][0]
    return -1

def search_version_type_in_db(version_id,type_,classifier):
    sql = "SELECT * FROM version_types WHERE type = '" + str(type_) + "' and version_id = " + str(version_id)
    types = database.querydb(db, sql)
    for t in types:
        if (classifier is not None and classifier == t[3]) or (classifier == None and t[3] == None):
            return t[0]
    return -1

def search_unsolved_lib(group,name1,version1,_type,classifier):
    if classifier is None:
        sql = "SELECT * FROM unsolved_libraries WHERE group_str = '" + str(group) + "' and name_str = '" + str(
        name1) +"' and version = '"+str(version1)+"' and type = '"+str(_type)+"' and classifier is NULL"
    else:
        sql = "SELECT * FROM unsolved_libraries WHERE group_str = '" + str(group) + "' and name_str = '" + str(
        name1) +"' and version = '"+str(version1)+"' and type = '"+str(_type)+"' and classifier = '"+str(classifier)+"'"
    record = database.querydb(db, sql)
    if len(record) > 0:
        return record[0][0],record[0][1]
    return -1,None

def update_project_id_for_unsolved_lib(unsolved_id,project_id):
    sql = "UPDATE unsolved_libraries set project_id = " + project_id + " WHERE id = " + unsolved_id
    database.execute_sql(db,sql)

def collect_project():
    json_data = read_json("E:/data/projs.json");
    print(len(json_data))

def save_project_info(dir_path,_type):
    array = []
    list = os.listdir(dir_path)
    for li in list:
        # path = os.path.join(dir_path, li)
        if li.endswith(".txt"):
            li = li[:-4]
        li = li.replace("__fdse__", "/")
        github_url = "https://github.com/" + li
        sql = "SELECT * FROM repository_high_quality WHERE url = '" + str(github_url) + "'"
        query_result = database.querydb(db,sql)
        if len(query_result) <= 0:
            raise CustomizeException("No url:"+github_url)
        proj_obj = {}
        proj_obj["id"] = query_result[0][0]
        proj_obj["repositoryid"] = query_result[0][1]
        proj_obj["url"] = query_result[0][2]
        proj_obj["stars"] = query_result[0][3]
        proj_obj["commit_count"] = query_result[0][4]
        proj_obj["sizes"] = query_result[0][5]
        proj_obj["fork"] = query_result[0][6]
        proj_obj["repos_addr"] = query_result[0][9]
        proj_obj["type"] = _type
        array.append(proj_obj)

    print(len(array))
    write_json("pros_maven_gradle_200_500.txt", array)


def project_info_to_db(path):
    json_data = read_json(path)
    for proj_obj in json_data:
        id = proj_obj["id"]
        sql = "SELECT * FROM project WHERE id = " + str(id)
        query_result = database.querydb(db, sql)
        if len(query_result) > 0:
            raise CustomizeException("duplicate id:" + str(id))
        sql = "INSERT INTO project" \
              "(id,url,stars,commit_count,sizes,fork,repos_addr,repository_id,type) " \
              "VALUES (\'" \
              + str(proj_obj["id"]).replace("'", "''") + "\',\'" \
              + str(proj_obj["url"]).replace("'", "''") + "\',\'" \
              + str(proj_obj["stars"]).replace("'", "''") + "\',\'" \
              + str(proj_obj["commit_count"]).replace("'", "''") + "\',\'" \
              + str(proj_obj["sizes"]).replace("'", "''") + "\',\'" \
              + str(proj_obj["fork"]).replace("'", "''") + "\',\'" \
              + str(proj_obj["repos_addr"]).replace("'", "''") + "\',\'" \
              + str(proj_obj["repositoryid"]).replace("'", "''") + "\',\'" \
              + str(proj_obj["type"]).replace("'", "''") + "\')"
        database.execute_sql(db, sql)

def browse_maven_projs():
    dir_path = "E:/data/curr_result_all/"
    proj_types = {}
    json_data = read_json("E:/data/projs.json")
    for data in json_data:
        url = data["url"]
        proj_type = data["proj-type"]
        proj_types[url] = proj_type
    # list = os.listdir("E:/data/curr_result_all")
    for id in range(5339,5600):
        if os.path.exists(dir_path+str(id) +".txt"):
            print(id)
            sql = "SELECT * FROM project WHERE id = " + str(id)
            query_result = database.querydb(db, sql)
            if len(query_result) > 0:
                raise CustomizeException("exists :" + str(id))
                type = query_result[0][8]
                if type != "maven-gradle":
                    raise CustomizeException("not maven_gradle type :" + str(id))
            else:
                proj_obj = read_json(dir_path+str(id) +".txt")
                http_url = proj_obj[0]["url"]
                if proj_types[http_url] != "proj-type: maven":
                    raise CustomizeException("not maven:" + str(id) + "  " + http_url)
                sql = "INSERT INTO project" \
                      "(id,url,stars,commit_count,sizes,fork,repos_addr,repository_id,type) " \
                      "VALUES (\'" \
                      + str(proj_obj[0]["id"]).replace("'", "''") + "\',\'" \
                      + str(proj_obj[0]["url"]).replace("'", "''") + "\',\'" \
                      + str(proj_obj[0]["stars"]).replace("'", "''") + "\',\'" \
                      + str(proj_obj[0]["commit_count"]).replace("'", "''") + "\',\'" \
                      + str(proj_obj[0]["sizes"]).replace("'", "''") + "\',\'" \
                      + str(proj_obj[0]["fork"]).replace("'", "''") + "\',\'" \
                      + str(proj_obj[0]["local_addr"]).replace("'", "''") + "\',\'" \
                      + str(proj_obj[0]["repository_id"]).replace("'", "''") + "\',\'maven\')"
                database.execute_sql(db, sql)

def browse_maven_gradle_projs():
    dir_path = "E:/data/curr_result8.5/"
    proj_types = {}
    json_data = read_json("E:/data/projs.json")
    for data in json_data:
        url = data["url"]
        proj_type = data["proj-type"]
        proj_types[url] = proj_type
    # list = os.listdir("E:/data/curr_result_all")
    for id in range(5400, 5600):
        if os.path.exists(dir_path + str(id) + ".txt"):
            print(id)
            sql = "SELECT * FROM project WHERE id = " + str(id)
            query_result = database.querydb(db, sql)
            if len(query_result) > 0:
                type = query_result[0][8]
                if type != "maven-gradle":
                    raise CustomizeException("not maven_gradle type :" + str(id))
            else:
                raise CustomizeException("not in db :" + str(id))

def project_dependency_usage_to_db(dir_path):
    file_list = os.listdir(dir_path)
    for file in file_list:
        whole_path = os.path.join(dir_path,file)
        data = read_json(whole_path)
        project_id = None
        module_ = None
        do = False
        for lib in data:
            if 'id' in lib:
                project_id = lib["id"]
                print("-------------------- project_id: " + str(project_id))
                continue
            if "groupId" not in lib or "artifactId" not in lib or "version" not in lib or "type" not in lib:
                print(False)
                continue
            groupId = lib["groupId"]
            artifactId = lib["artifactId"]
            version = lib["version"]
            type_ = lib["type"]
            if groupId is None or artifactId is None or version is None or type_ is None or '${' in groupId or '${' in artifactId or '${' in version or '${' in type_:
                print("groupId: " + str(groupId) + "   artifactId: " + str(artifactId) + "   version: " + str(
                    version) + "   type: " + str(type_))
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
            if type(version) == list:
                continue
            version_id = search_library_version_in_db(groupId, artifactId, version)
            if version_id > 0:
                type_id = search_version_type_in_db(version_id, type_, classifier)
                if type_id > 0:
                    insert_project_lib_usage(project_id, type_id, module_)
                    continue

            unsolved_id, recorded_proj_id = search_unsolved_lib(groupId, artifactId, version, type_, classifier)
            if unsolved_id < 0:
                raise CustomizeException(
                    "unrecorded library: " + "groupId: " + str(groupId) + "   artifactId: " + str(
                        artifactId) + "   version: " + str(version) + "   type: " + str(
                        type_) + "   classifier: " + str(classifier))
            elif recorded_proj_id is None:
                    update_project_id_for_unsolved_lib(unsolved_id, project_id)


def other_project_dependency_usage_to_db(dir_path):
    file_list = os.listdir(dir_path)
    for file in file_list:
        github_url = file
        if github_url.endswith(".txt"):
            github_url = github_url[:-4]
        github_url = github_url.replace("__fdse__", "/")
        github_url = "https://github.com/" + github_url
        sql = "SELECT * FROM project WHERE url = '" + str(github_url) + "'"
        query_result = database.querydb(db, sql)
        if len(query_result) <= 0:
            raise CustomizeException("No url:" + github_url)
        project_id = query_result[0][0]
        whole_path = os.path.join(dir_path,file)
        json_data = read_json(whole_path)
        dependency_list = json_data["dependencyUrls"]
        for lib in dependency_list:
            groupId = lib["groupId"]
            artifactId = lib["artifactId"]
            version = lib["version"]
            type_ = "jar"
            classifier = None
            module_ = ""
            if project_id is None:
                continue

            version_id = search_library_version_in_db(groupId, artifactId, version)
            if version_id > 0:
                type_id = search_version_type_in_db(version_id, type_, classifier)
                if type_id > 0:
                    insert_project_lib_usage(project_id, type_id, module_)
                    continue

            unsolved_id, recorded_proj_id = search_unsolved_lib(groupId, artifactId, version, type_, classifier)
            if unsolved_id < 0:
                raise CustomizeException(
                    "unrecorded library: " + "groupId: " + str(groupId) + "   artifactId: " + str(
                        artifactId) + "   version: " + str(version) + "   type: " + str(
                        type_) + "   classifier: " + str(classifier))
            elif recorded_proj_id is None:
                update_project_id_for_unsolved_lib(unsolved_id, project_id)


# collect_project()
# project_info_to_db("pros_maven_gradle_200_500.txt")
# save_project_info("E:/data/dependency/maven_gradle200_500","maven-gradle")
# browse_maven_gradle_projs()
# project_dependency_usage_to_db("E:/data/curr_result_all")