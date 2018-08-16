import os

import database
# from crawled_library_to_db import in_unsolved_table
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
    write_json("gradle.txt", array)

def save_project_info(dir_path):
    proj_types = {}
    json_data = read_json("E:/data/projs.json")
    for data in json_data:
        url = data["url"]
        proj_type = data["proj-type"]
        proj_type = proj_type.split(":")[-1].strip()
        proj_types[url] = proj_type
    gradle_array = []
    gradle_maven_array = []
    list = os.listdir(dir_path)
    for li in list:
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
        proj_obj["type"] = proj_types[query_result[0][2]]
        print(query_result[0][2])
        print(proj_obj["type"])
        if proj_obj["type"] == "gradle":
            gradle_array.append(proj_obj)
        if proj_obj["type"] == "maven-gradle":
            gradle_maven_array.append(proj_obj)
    print(len(gradle_array))
    print(len(gradle_maven_array))
    write_json("gradle.txt", gradle_array)
    write_json("gradle_maven.txt", gradle_maven_array)


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
    dir_path = "E:/data/curr_result_add/"
    proj_types = {}
    json_data = read_json("E:/data/projs.json")
    for data in json_data:
        url = data["url"]
        proj_type = data["proj-type"]
        proj_types[url] = proj_type
    # list = os.listdir("E:/data/curr_result_all")
    for id in range(4049,5600):
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
    dir_path = "E:/data/curr_result8.5(maven_gradle)/"
    proj_types = {}
    json_data = read_json("E:/data/projs.json")
    for data in json_data:
        url = data["url"]
        proj_type = data["proj-type"]
        proj_types[url] = proj_type
    # list = os.listdir("E:/data/curr_result_all")
    for id in range(0, 5600):
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

def check_maven_projs():
    count =0
    dir_path = "E:/data/curr_result_all/"
    proj_types = {}
    json_data = read_json("E:/data/projs.json")
    for data in json_data:
        url = data["url"]
        proj_type = data["proj-type"]
        proj_types[url] = proj_type
    # list = os.listdir("E:/data/curr_result_all")
    for id in range(0, 5600):
        if os.path.exists(dir_path + str(id) + ".txt"):
            print(id)
            sql = "SELECT * FROM project WHERE id = " + str(id)
            query_result = database.querydb(db, sql)
            if len(query_result) > 0:
                type = query_result[0][8]
                if type != "maven":
                    raise CustomizeException("not maven type :" + str(id))
            else:
                raise CustomizeException("not in db :" + str(id))
            # proj_obj = read_json(dir_path + str(id) + ".txt")
            # http_url = proj_obj[0]["url"]
            # if proj_types[http_url] == "proj-type: maven":
            #     count +=1
            #     print(str(id) + "    " + proj_types[http_url])
    print(count)


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

def delete_duplicate_file(start, end):
    # os.remove("E:/data/dependency_library_info/test.txt")
    json_data = read_json("dependencies_list.txt")
    print(len(json_data))
    for i in range(start, end):
        key = json_data[i]["lib_name"]
        # path = "E:/data/dependency_library_info/" + key + ".json"
        path = "H:/wangying/2018-8-3-分机器跑/dependency_library_info/" + key + ".json"
        if os.path.exists(path):
            print("+++++++++++++++++++++++++++++++ " + str(i))
            print(path)
            os.remove(path)

def get_maven_proj_url():
    sql = "SELECT * FROM project WHERE type = 'maven'"
    query_result = database.querydb(db, sql)
    print(len(query_result))
    with open("maven_url.txt", "a") as f:
        for result in query_result:
            f.write(str(result[0])+"\n")
            f.write(result[1]+"\n")
    f.close()

def projs_statics():
    gradle_count,maven_count,gradle_maven_count = 0,0,0
    new_array = []
    json_data = read_json("E:/data/projs.8.11.time.json")
    print(len(json_data))
    for proj in json_data:
        type_ = proj["proj-type"]
        if type_ == "proj-type: gradle":
            gradle_count += 1
        if type_ == "proj-type: maven":
            maven_count += 1
        if type_ == "proj-type: maven-gradle":
            gradle_maven_count += 1
    #     url = proj["url"]
    #     sql = "SELECT * FROM project WHERE url = '" + url + "'"
    #     query_result = database.querydb(db, sql)
    #     if len(query_result) > 0:
    #         new_array.append(proj)
    # print(len(new_array))
    # write_json("E:/data/projs8.11.json",new_array)
    print(gradle_count)
    print(maven_count)
    print(gradle_maven_count)

def update_projs_in_db():
    count = 0
    proj_types = {}
    json_data = read_json("E:/data/projs.json")
    for data in json_data:
        url = data["url"]
        proj_type = data["proj-type"]
        proj_types[url] = proj_type
    sql = "SELECT * FROM project where type = 'maven'"
    query_result = database.querydb(db,sql)
    print(len(query_result))
    for record in query_result:
        url = record[1]
        if url not in proj_types:
            count += 1
            print(url)
            # sql = "DELETE FROM project where id = "+str(record[0])
            # database.execute_sql(db,sql)
    print(count)

def delete_projs_result(dir_path):
    count = 0
    file_list = os.listdir(dir_path)
    for li in file_list:
        path = os.path.join(dir_path, li)
        if li.endswith(".txt"):
            li = li[:-4]
        li = li.replace("__fdse__", "/")
        github_url = "https://github.com/" + li
        sql = "SELECT * FROM project WHERE url = '" + str(github_url) + "'"
        query_result = database.querydb(db,sql)
        if len(query_result) <= 0:
            count += 1
            print(github_url)
            os.remove(path)
    print(count)

def check_unsolved_maven_gradle_proj():
    proj_types = {}
    json_data = read_json("E:/data/projs.8.11.time.json")
    for data in json_data:
        url = data["url"]
        proj_type = data["proj-type"]
        proj_types[url] = proj_type
    sql = "SELECT * FROM project where type ='gradle'"
    query_result = database.querydb(db,sql)
    # print(len(query_result))
    for record in query_result:
        id = record[0]
        url = record[1]
        if proj_types[url] == "proj-type: maven-gradle":
            print(id)
            print(url)


# collect_project()
# project_info_to_db("gradle_maven.txt")
# save_project_info("E:/data/dependency/maven_gradle200_500","maven-gradle")
# browse_maven_gradle_projs()
# project_dependency_usage_to_db("E:/data/curr_result_all")
# delete_duplicate_file(2501, 3001)
# check_maven_projs()
# browse_maven_projs()
# get_maven_proj_url()
# save_project_info("E:/data/diff")
# update_projs()
# update_projs_in_db()
# delete_projs_result("E:/data/dependency/maven_gradle200_500")
# check_unsolved_maven_gradle_proj()
# projs_statics()
# project_dependency_usage_to_db(dir_path)