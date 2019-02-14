import os
import shutil

from crawled_library_to_db import in_version_type_table
from exception import CustomizeException
from file_util import read_json, read_file, write_json
import database

def android_proj():
    android_count = 0
    no_count = 0
    m_g_count = 0
    lines = read_file("H:/wangying/中间过程统计数据/200-500.txt")
    for line in lines:
        if line == "proj-type: android":
            android_count += 1
        elif line == "proj-type: no":
            no_count += 1
        elif line == "proj-type: maven" or line == "proj-type: gradle" or line == "proj-type: maven-gradle":
            m_g_count += 1
        elif line.startswith("proj-type"):
            print(line)

    lines = read_file("H:/wangying/中间过程统计数据/500p.txt")
    for line in lines:
        if line == "proj-type: android":
            android_count += 1
        elif line == "proj-type: no":
            no_count += 1
        elif line == "proj-type: maven" or line == "proj-type: gradle" or line == "proj-type: maven-gradle":
            m_g_count += 1
        elif line.startswith("proj-type:"):
            print(line)
    #
    print(android_count)
    print(no_count)
    print(m_g_count)

def divide_batch():
    for i in range(0,6):
        if not os.path.exists("F:/rq1_batch/" + str(i)):
            os.mkdir("F:/rq1_batch/" + str(i))
        data = read_json("G:/data/rq1_1274_"+str(i)+".json")
        for proj in data:
            project_id = proj["id"]
            if os.path.exists("F:/rq1_batch/" + str(project_id) + ".sh"):
                if not os.path.exists("F:/rq1_batch/" + str(i) + "/" + str(project_id) + ".sh"):
                    shutil.copyfile("F:/rq1_batch/" + str(project_id) + ".sh", "F:/rq1_batch/" + str(i) + "/" + str(project_id) + ".sh" )
            else:
                print("F:/rq1_batch/" + str(project_id) + ".sh")
    # db = database.connectdb()
    # sql = "SELECT distinct(repository) FROM library_versions"
    # query_result = database.querydb(db, sql)
    # print(len(query_result))
    # for entry in query_result:
    #     print(entry[0])

def collect_projs():
    db = database.connectdb()
    dir = "E:/data/dependency/gradle_all"
    files = os.listdir(dir)
    for file in files:
        name = "https://github.com/" + file.replace(".txt", "").replace("__fdse__", "/")
        sql = "SELECT * FROM project where url = '" + name + "' and stars > 200"
        query_result = database.querydb(db, sql)
        id = query_result[0][0]
        shutil.copyfile(dir + "/" + file, "E:/data/dependency/gradle_id/" + str(id) + ".txt")
        # _type = query_result[0][8]
        # # print(_type)
        # if _type != "gradle":
        #     print(file)

def dependency_statics():
    # db = database.connectdb()
    # count = 0
    # dir = "D:/data/data_copy/RQ1/dependency/maven_or_both"
    # files = os.listdir(dir)
    # for file in files:
    #     data = read_json(os.path.join(dir, file))
    #     for lib in data:
    #         if 'id' in lib:
    #             project_id = lib["id"]
    #             print("-------------------- project_id: " + str(project_id))
    #             continue
    #         count += 1
    # print(count)
    #
    # dir = "D:/data/data_copy/RQ1/dependency/gradle_or_both"
    # files = os.listdir(dir)
    # for file in files:
    #     print("-------------------- project_id: " + str(file))
    #     dependency_list = read_json(os.path.join(dir, file))
    #     # dependency_list = json_data["dependencyUrls"]
    #     count += len(dependency_list)
    #     # for lib in dependency_list:
    #     #     count +=
    # print(count)

    # new_list = []
    # # new_list = read_json("D:/data/data_copy/RQ1/dependency/total.txt")
    # # print(len(new_list))
    # dir = "D:/data/data_copy/RQ1/dependency/maven_or_both"
    # files = os.listdir(dir)
    # for file in files:
    #     project_id = int(file.replace(".txt", ""))
    #     data = read_json(os.path.join(dir, file))
    #     for lib in data:
    #         if 'id' in lib:
    #             project_id = lib["id"]
    #             print("-------------------- project_id: " + str(project_id))
    #             continue
    #         lib["project_id"] = project_id
    #         new_list.append(lib)
    # print(len(new_list))
    # # write_json("D:/data/data_copy/RQ1/dependency/total.txt", new_list)
    #
    # dir = "D:/data/data_copy/RQ1/dependency/gradle_or_both"
    # files = os.listdir(dir)
    # for file in files:
    #     project_id = int(file.replace(".txt", ""))
    #     print("-------------------- project_id: " + str(file))
    #     dependency_list = read_json(os.path.join(dir, file))
    #     for lib in dependency_list:
    #         lib["classifier"] = None
    #         lib["module"] = lib["path"]
    #         lib.pop("path")
    #         lib["project_id"] = project_id
    #         new_list.append(lib)
    # write_json("D:/data/data_copy/RQ1/dependency/total.txt", new_list)

    new_list = read_json("D:/data/data_copy/RQ1/dependency/total.txt")
    print(len(new_list))
    count = 0
    snapcount = 0
    final = []
    for lib in new_list:
        if "groupId" not in lib or "artifactId" not in lib or "version" not in lib or "type" not in lib:
            print(False)
            continue
        groupId= lib["groupId"]
        artifactId = lib["artifactId"]
        version = lib["version"]
        type_ = lib["type"]
        if groupId is None or artifactId is None or version is None or type_ is None or '${' in groupId or '${' in artifactId or '${' in version or '${' in type_ or '@' in groupId or '@' in artifactId or '@' in version or '@' in type_:
            print("groupId: " + str(groupId) +"   artifactId: " + str(artifactId)+"   version: " + str(version)+"   type: " + str(type_) )
            print(False)
            continue
        if type(version) == list:
            continue
        if "classifier" in lib:
            classifier = lib["classifier"]
            if classifier is not None and ('${' in classifier or '@' in classifier):
                continue
        count += 1

        if version.endswith("SNAPSHOT"):
            snapcount += 1
        final.append(lib)
    print(count)
    print(snapcount)
    write_json("D:/data/data_copy/RQ1/dependency/final.txt", final)
    #     classifier = None
    #     if "classifier" in lib:
    #         classifier = lib["classifier"]
    #         if '${' in classifier:
    #             print("groupId: " + str(groupId) + "   artifactId: " + str(artifactId) + "   version: " + str(
    #                 version) + "   type: " + str(type_) + "   classifier: " + str(classifier))
    #             print(False)
    #             continue
    #     if type(version) == list:
    #         continue
    #     version_ids = set()
    #     library_ids = set()
    #     sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
    #         artifactId) + "' and version = '" + str(version) + "'"
    #     version_info = database.querydb(db, sql)
    #     version_id = None
    #     if len(version_info) != 0:
    #         version_id = version_info[0][0]
    #         version_ids.add(version_id)
    #         library_id = version_info[0][1]
    #         library_ids.add(library_id)
    # write_json("E:/data/curr_result_statics/versions.txt", list(version_ids))
    # write_json("E:/data/curr_result_statics/libraries.txt", list(library_ids))

def gradle_dependency_process():
    count = 0
    db = database.connectdb()
    dir = "D:/data/data_copy/RQ1/dependency/rq1_output/normal"
    files = os.listdir(dir)
    for file in files:
        print(file)
        url = "https://github.com/" + file.replace(".txt","").replace("__fdse__","/")
        sql = "SELECT * FROM project WHERE url = '" + url + "'"
        query_result = database.querydb(db, sql)
        project_id = query_result[0][0]
        data = read_json(os.path.join(dir, file))
        if not "dependencyUrlList" in data:
            count += 1
            continue
    # print(count)
        dependency_list = data["dependencyUrlList"]
        record_dic = {}
        new_list = []
        for dependency in dependency_list:
            groupId = dependency["groupId"]
            artifactId = dependency["artifactId"]
            _type = dependency["type"]
            version = dependency["version"]
            path = dependency["path"]
            value = groupId + " " + artifactId + " " + version + " " + _type
            if path in record_dic:
                if not value in record_dic[path]:
                    record_dic[path].append(value)
                    new_list.append(dependency)
            else:
                array = []
                array.append(value)
                record_dic[path] = array
                new_list.append(dependency)
        write_json("D:/data/data_copy/RQ1/dependency/gradle_or_both/" + str(project_id) + ".txt", new_list)
        # break

def maven_dependency_process():
    count = 0
    db = database.connectdb()
    dir = "D:/data/data_copy/RQ1/dependency/test"
    files = os.listdir(dir)
    for file in files:
        print("+++++++++++++++++++++++ " + file)
        record_dic = {}
        new_list = []
        dependency_list = read_json(os.path.join(dir, file))
        for dependency in dependency_list:
            if 'id' in dependency:
                continue
            groupId = dependency["groupId"]
            artifactId = dependency["artifactId"]
            _type = dependency["type"]
            if "version" not in dependency:
                version = "null"
            else:
                version = str(dependency["version"])
            module_ = dependency["module"]
            value = groupId + " " + artifactId + " " + version + " " + _type
            classifier = None
            if "classifier" in dependency:
                value += " " + dependency["classifier"]
            if module_ in record_dic:
                if not value in record_dic[module_]:
                    record_dic[module_].append(value)
                    new_list.append(dependency)
                else:
                    print(module_ + " : " + value)
            else:
                array = []
                array.append(value)
                record_dic[module_] = array
                new_list.append(dependency)
        if len(dependency_list)-1 != len(new_list):
            print(str(len(dependency_list)-1) + " || " + str(len(new_list)))
        write_json("D:/data/data_copy/RQ1/dependency/test_new/" + file, new_list)
        # break

def project_lib_usage_to_db(project_id, path):
    if not os.path.exists(path):
        return
    print("+++++++++++++++++++++++++++++++++++" + str(path))
    data = read_json(path)
    module_ = None
    do = False
    # print(len(data))
    for lib in data:
        # print(lib)
        # if 'id' in lib:
        #     project_id = lib["id"]
        #     print("-------------------- project_id: " + str(project_id))
        #     continue
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
        elif "path" in lib:
            module_ = lib["path"].replace("I:\\projects\\", "")
        if type(version) == list:
            continue
        else:
            search_before_insert(project_id, groupId, artifactId, version, type_, classifier, module_)

def project_lib_usage_to_db_gradle():
    dir = "D:/data/data_copy/RQ1/dependency/gradle_or_both"
    files = os.listdir(dir)
    for file in files:
        project_id = int(file.replace(".txt", ""))
        # if project_id != 359:
        #     continue
        print("+++++++++++++++++++++++++++++++++++" + str(file))
        data = read_json(os.path.join(dir, file))
        for lib in data:
            if "groupId" not in lib or "artifactId" not in lib or "version" not in lib or "type" not in lib:
                raise CustomizeException("need value")
            groupId = lib["groupId"]
            artifactId = lib["artifactId"]
            version = lib["version"]
            type_ = lib["type"]
            if groupId is None or artifactId is None or version is None or type_ is None:
                raise CustomizeException("None value(groupId: " + str(groupId) + "   artifactId: " + str(artifactId) + "   version: " + str(
                    version) + "   type: " + str(type_))
            if project_id is None:
                raise CustomizeException("no project id")
            classifier = None

            if "classifier" in lib:
                classifier = lib["classifier"]
            if "module" in lib:
                module_ = lib["module"]
            elif "path" in lib:
                module_ = lib["path"].replace("I:\\projects\\", "")
            if type(version) == list:
                continue
            else:
                search_before_insert(project_id, groupId, artifactId, version, type_, classifier, module_)

def search_before_insert(project_id, groupId, artifactId, version, type_, classifier, module_):
    # print("----------------------- " + str(project_id) + " " + str(groupId) + " " + str(artifactId) + " " + str(version) + " " + str(type_) + " " + str(classifier) + " " + str(module_))
    sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
        artifactId) + "' and version = '" + str(version) + "'"
    version_info = database.querydb(db, sql)
    version_id = None
    if len(version_info) != 0:
        version_id = version_info[0][0]
    if version_id is None:
        return
    version_type_id = in_version_type_table(version_id, type_, classifier)
    if version_type_id < 0:
        return
    # print(str(project_id) + " " + str(version_type_id) + " " + module_)
    insert_project_lib_usage(project_id, version_type_id, module_)

def insert_project_lib_usage(project_id, version_type_id, module_):
    sql = "SELECT * FROM project_lib_usage WHERE project_id = " + str(
        project_id) + " and version_type_id = " + str(version_type_id) + " and module = '" + module_ + "'"
    record = database.querydb(db, sql)
    if len(record) == 0:
        if module_ is None:
            raise CustomizeException("module_ is None : " + str(project_id) + " " + str(version_type_id))
            # sql = "INSERT INTO project_lib_usage (project_id,version_type_id) VALUES ('" + str(
            #     project_id) + "','" + str(version_type_id) + "')"
        else:
            sql = "INSERT INTO project_lib_usage (project_id,version_type_id,module) VALUES (" + str(
                project_id) + "," + str(version_type_id) + ",'" + str(module_) + "')"
            database.execute_sql(db, sql)
            print('======================== INSERT INTO project_lib_usage : ' + str(project_id) + "  " + str(
            version_type_id))
    else:
        raise CustomizeException("repeat : " + str(project_id) + " " + str(version_type_id) + " " + str(module_))

def compare():
    count = 0
    curr_list = []
    sql = "SELECT distinct project_id FROM project_lib_usage"
    curr = database.querydb(db, sql)
    for entry in curr:
        proj_id = entry[0]
        curr_list.append(proj_id)
    sql = "SELECT distinct project_id FROM `project_lib_usage_1.30`"
    prev = database.querydb(db, sql)
    for entry in prev:
        proj_id = entry[0]
        if proj_id not in curr_list:
            print(proj_id)
            count += 1
    print(count)

def check_data():
    projs = []
    sql = "SELECT distinct project_id FROM `project_lib_usage_1.30`"
    result = database.querydb(db, sql)
    for entry in result:
        proj_id = entry[0]
        # sql = "SELECT * FROM project WHERE type = 'maven' AND id = " + str(proj_id)
        # result = database.querydb(db, sql)
        # if len(result) <= 0:
        #     continue
        projs.append(proj_id)
    print(projs)
    print(len(projs))

    count = 0
    new_list = []
    for proj_id in projs:
        sql = "SELECT distinct version_type_id FROM `project_lib_usage_1.30` where project_id = " + str(proj_id)
        query_result1 = database.querydb(db, sql)
        sql = "SELECT distinct version_type_id FROM `project_lib_usage` where project_id = " + str(proj_id)
        query_result2 = database.querydb(db, sql)
        if len(set(query_result1).difference(set(query_result2))) != 0:
        # if len(set(query_result1).difference(set(query_result2))) != 0 or len(set(query_result2).difference(set(query_result1))) != 0:
            print("-------------------- " + str(proj_id))
            print(set(query_result1).difference(set(query_result2)))
            # print(set(query_result2).difference(set(query_result1)))
            count += 1
            new_list.append(proj_id)
        # if len(query_result1) != len(query_result2):
        #     count += 1
        #     # if len(query_result1) > len(query_result2):
        #     print("-------------------- " + str(proj_id))
        #     if len(set(query_result1).difference(set(query_result2))) != 0:
        #
        #         print(set(query_result1).difference(set(query_result2)))
        #         print(set(query_result2).difference(set(query_result1)))
    print(count)
    print(new_list)

# divide_batch()
# android_proj()
# json_data = read_json("E:/data/projs.json");
# print(len(json_data))
# collect_projs()
# dependency_statics()
# gradle_dependency_process()
# maven_dependency_process()
# db = database.connectdb()
# sql = "SELECT distinct(project_id) FROM project_lib_usage"
# projs_result = database.querydb(db, sql)
# projs = []
# for entry in projs_result:
#     proj_id = entry[0]
#     projs.append(proj_id)
# # print(projs)
# print(len(projs))
#
# new_list = []
# dir = "D:/data/data_copy/RQ1/dependency/test_new"
# files = os.listdir(dir)
# print(len(files))
# count = 0
# for file in files:
#     # print(file)
#     project_id = int(file.replace(".txt", ""))
#     sql = "SELECT * FROM project WHERE type = 'maven' AND id = " + str(project_id)
#     result = database.querydb(db, sql)
#     if len(result) <= 0:
# #         new_list.append(project_id)
# # print(new_list)
# # print(len(new_list))
#         continue
#     count += 1
#     if project_id == 2871:
#         print(file)
#     #     continue
#         project_lib_usage_to_db(project_id, os.path.join(dir, file))
# print(count)

# project_lib_usage_to_db_gradle()
# compare()
# path = "E:/Workspace_eclip/ThirdPartyLibraryAnalysis/proj_in_usage.txt"
# data = read_json(path)
# print(len(data))

# check_data()

# projs = []
# sql = "SELECT distinct project_id FROM `project_lib_usage_1.30`"
# result = database.querydb(db, sql)
# for entry in result:
#     proj_id = entry[0]
#     sql = "SELECT * FROM project WHERE type = 'maven' AND id = " + str(proj_id)
#     result = database.querydb(db, sql)
#     if len(result) <= 0:
#         continue
#     projs.append(proj_id)
# print(projs)
# print(len(projs))
#
# count = 0
# sql = "SELECT * FROM `project_lib_usage_1.30`"
# result = database.querydb(db, sql)
# for entry in result:
#     project_id = entry[0]
#     if project_id in projs:
#         count += 1
# print(count)

# new_list = [32, 83, 85, 148, 155, 163, 174, 318, 349, 361, 376, 383, 508, 534, 584, 602, 678, 692, 707, 709, 741, 759, 816, 1107, 1156, 1207, 1342, 1362, 1383, 1391, 1399, 1461, 1464, 1493, 1517, 1520, 1521, 1558, 1573, 1585, 1655, 1659, 1691, 1702, 1755, 1770, 1792, 1798, 1799, 1806, 1840, 1886, 1996, 2004, 2081, 2116, 2413, 2450, 2528, 2661, 2663, 2802, 2808, 2871, 3105, 3186, 3214, 3244, 3370, 3417, 3437, 3568, 3609, 3683, 3739, 4153, 4161, 4191, 4408, 4500, 4600, 4672, 5027, 5330, 5412, 5479]
# print(len(new_list))
# for proj_id in new_list:
#     sql = "delete from project_lib_usage where project_id = " + str(proj_id)
#     database.execute_sql(db, sql)

def get_library():
    db = database.connectdb()
    cursor = db.cursor()
    usage_values = []
    json_data = read_json("D:/data/data_copy/RQ1/dependency/final.txt")
    print(len(json_data))
    for lib in json_data:
        groupId= lib["groupId"]
        artifactId = lib["artifactId"]
        version = lib["version"]
        type_ = lib["type"]
        classifier = None
        if "classifier" in lib:
            classifier = lib["classifier"]
        if "module" in lib:
            module_ = lib["module"]
        elif "path" in lib:
            module_ = lib["path"].replace("I:\\projects\\", "")
        if module_ is None:
            raise CustomizeException(groupId + " " + groupId + " " + artifactId + " " + version + " " + type_ + " " + str(classifier))
        project_id = lib["project_id"]

        usage_values.append((project_id, groupId, artifactId, version, type_, classifier, module_))
        if len(usage_values) == 5000:
            cursor.executemany(
                'INSERT INTO `usage` (`project_id`, `group_str`, `name_str`, `version`, `type`, `classifier`, `module`) VALUE (%s,%s,%s,%s,%s,%s,%s)',
                usage_values)
            db.commit()
            usage_values = []
            print(5000)
    cursor.executemany(
        'INSERT INTO `usage` (`project_id`, `group_str`, `name_str`, `version`, `type`, `classifier`, `module`) VALUE (%s,%s,%s,%s,%s,%s,%s)',
        usage_values)
    db.commit()

get_library()

