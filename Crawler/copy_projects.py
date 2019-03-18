import os
import shutil

import database
from exception import CustomizeException
from file_util import read_json, write_json, read_file, write_json_format


def get_proj_not_in_three():
    three_month = read_json("three_month.txt")
    print(len(three_month))
    names = []
    for entry in three_month:
        name = entry["name"]
        names.append(name)

    total = read_json('E:/data/projs.8.11.time.json')
    print(len(total))
    result = []
    for entry in total:
        url = entry["url"]
        temp = url.replace("https://github.com/", "").replace("/", "__fdse__")
        if temp not in names:
            result.append(temp)
    print(len(result))
    write_json('E:/data/project_not_in_three_month.txt',result)

def get_local_addr():
    # result = {}
    # projs = read_json('E:/data/project_not_in_three_month.txt')
    # for entry in projs:
    #     name = entry
    #     if os.path.exists("H:/projects_last/gradle_maven200_500/" + name + ".zip"):
    #         local = "gradle_maven200_500/" + name
    #     elif os.path.exists("H:/projects_last/gradle_maven500/" + name + ".zip"):
    #         local = "gradle_maven500/" + name
    #     elif os.path.exists("H:/projects_last/gradle200_500/" + name + ".zip"):
    #         local = "gradle200_500/" + name
    #     elif os.path.exists("H:/projects_last/gradle500/" + name + ".zip"):
    #         local = "gradle500/" + name
    #     elif os.path.exists("H:/projects_last/maven200_500/" + name + ".zip"):
    #         local = "maven200_500/" + name
    #     elif os.path.exists("H:/projects_last/maven500/" + name + ".zip"):
    #         local = "maven500/" + name
    #     else:
    #         raise CustomizeException("Not in local:" + name)
    #     result[name] = local
    #     write_json('E:/data/local_path_not_in_three_month.txt', result)

    db = database.connectdb()
    result = {}
    projs = os.listdir('C:/data/commit_pair')
    for entry in projs:
        project_id = int(entry.replace(".txt", ""))
        sql = "SELECT url FROM project WHERE id = " + str(project_id)
        query_result = database.querydb(db, sql)
        url = query_result[0][0]
        name = url.replace("https://github.com/", "").replace("/", "__fdse__")
        if os.path.exists("H:/projects_last/gradle_maven200_500/" + name + ".zip"):
            local = "gradle_maven200_500/" + name
        elif os.path.exists("H:/projects_last/gradle_maven500/" + name + ".zip"):
            local = "gradle_maven500/" + name
        elif os.path.exists("H:/projects_last/gradle200_500/" + name + ".zip"):
            local = "gradle200_500/" + name
        elif os.path.exists("H:/projects_last/gradle500/" + name + ".zip"):
            local = "gradle500/" + name
        elif os.path.exists("H:/projects_last/maven200_500/" + name + ".zip"):
            local = "maven200_500/" + name
        elif os.path.exists("H:/projects_last/maven500/" + name + ".zip"):
            local = "maven500/" + name
        else:
            raise CustomizeException("Not in local:" + name)
        result[name] = local
        write_json('E:/data/proj_for_commit_pair.txt', result)

def copy_projs():
    # projs = read_json('E:/data/proj_for_commit_pair.txt')
    # print(len(projs))
    # for name in projs.keys():
    #     local = projs[name]
    #     shutil.copyfile("H:/projects_last/" + local + ".zip", "E:/projects/" + name + ".zip")
    projs = read_json('E:/data/200_plus.txt')
    print(len(projs))
    for entry in projs:
        name = entry["name"]
        if not os.path.exists("C:/projects_unzips/" + name):
            if os.path.exists("H:/projects_last/gradle_maven200_500/" + name + ".zip"):
                local = "gradle_maven200_500/" + name
            elif os.path.exists("H:/projects_last/gradle_maven500/" + name + ".zip"):
                local = "gradle_maven500/" + name
            elif os.path.exists("H:/projects_last/gradle200_500/" + name + ".zip"):
                local = "gradle200_500/" + name
            elif os.path.exists("H:/projects_last/gradle500/" + name + ".zip"):
                local = "gradle500/" + name
            elif os.path.exists("H:/projects_last/maven200_500/" + name + ".zip"):
                local = "maven200_500/" + name
            elif os.path.exists("H:/projects_last/maven500/" + name + ".zip"):
                local = "maven500/" + name
            else:
                raise CustomizeException("Not in local:" + name)
            shutil.copyfile("H:/projects_last/" + local + ".zip", "E:/projects/" + name + ".zip")

def get_not_three_month():
    result = []
    db = database.connectdb()
    projs = read_json('E:/data/local_path_not_in_three_month.txt')
    for name in projs.keys():
        local = projs[name]
        url = "https://github.com/" + name.replace("__fdse__", "/")
        sql = "SELECT id FROM project WHERE url = '" + url + "'"
        query_result = database.querydb(db, sql)
        project_id = query_result[0][0]
        obj = {}
        obj["id"] = project_id
        obj["name"] = name
        obj["local_addr"] = local
        result.append(obj)
    write_json('E:/data/not_in_three_month.txt', result)

def top50():
    db = database.connectdb()
    libraries = read_json("F:/libraries.txt")
    print(len(libraries))
    usage_count = {}
    for entry in libraries:
        groupId = entry[0]
        artifactId = entry[1]
        sql = "SELECT DISTINCT(project_id) FROM `usage` WHERE group_str = '" +groupId + "' and name_str = '" + artifactId + "'"
        usage_info = database.querydb(db, sql)
        name = groupId + " " + artifactId
        usage_count[name] = len(usage_info)
    sorted_usage = sorted(usage_count.items(), key=lambda d: d[1], reverse=True)
    sorted_usage = sorted_usage[:50]
    print(sorted_usage)
    write_json("E:/data/top50.txt", sorted_usage)

def get_gradle():
    result = []
    db = database.connectdb()
    json_data = read_json("E:/data/not_in_three_month.txt")
    print(len(json_data))
    for entry in json_data:
        id = entry['id']
        sql = "SELECT type FROM project WHERE id = " + str(id)
        query_result = database.querydb(db, sql)
        _type = query_result[0][0]
        if _type == 'gradle' or _type == 'maven-gradle':
            result.append(entry)
    write_json("E:/data/not_in_three_month_gradle.txt", result)

def get_commit_pair_for_project():
    dir = "F:/shibowen/lib_update_gradle"
    files = os.listdir(dir)
    for file in files:
        print("+++++++++++++++++ " + file)
        project_id = file.replace(".txt", "")
        lines = read_file(os.path.join(dir, file))
        proj_pairs = set()
        for line in lines:
            value = line.split(" VALUES ")[1]
            value = value.replace("NULL", "'NULL'")
            value = tuple(eval(value.strip()))
            # print(value)
            prev_commit = value[8]
            curr_commit = value[9]
            proj_pairs.add((prev_commit, curr_commit))
            # print(prev_commit + " " + curr_commit)
        write_json("C:/data/commit_pair_2/" + file, list(proj_pairs))

def get_commit_pair_from_db():
    db = database.connectdb()
    sql = "SELECT distinct project_id FROM lib_update"
    query_result = database.querydb(db, sql)
    projs = []
    for entry in query_result:
        project_id = entry[0]
        projs.append(project_id)
    print(projs)
    print(len(projs))

    for project_id in projs:
        print("++++++++++++++++++ " + str(project_id))
        sql = "SELECT distinct prev_commit,curr_commit FROM lib_update WHERE project_id = " + str(project_id)
        query_result = database.querydb(db, sql)
        # print(list(query_result))
        write_json("C:/data/commit_pair_db/" + str(project_id) + ".txt", list(query_result))
        # break

def get_change_info_from_db():
    db = database.connectdb()
    # sql = "SELECT distinct project_id,prev_commit,curr_commit FROM lib_update"
    # query_result = database.querydb(db, sql)
    # write_json("E:/data/change_info_in_db.txt", list(query_result))

    json_data = read_json("E:/data/change_info_in_db.txt")
    final = {}
    for entry in json_data:
        project_id = entry[0]
        prev_commit = entry[1]
        curr_commit = entry[2]
        key = str(project_id) + "__fdse__" + prev_commit + "__fdse__" + curr_commit
        print("+++++++++++++++++++ " + key)
        sql = "SELECT group_str,name_str,prev_version,curr_version FROM lib_update WHERE project_id = " + str(project_id) + " and prev_commit = '" + prev_commit + "' and curr_commit = '" + curr_commit + "'"
        query_result = database.querydb(db, sql)
        for entry in query_result:
            groupId = entry[0]
            artifactId = entry[1]
            prev_version = entry[2]
            curr_version = entry[3]
            lib = groupId + "__fdse__" + artifactId
            value = prev_version + "__fdse__" + curr_version
            if key in final:
                if lib in final[key]:
                    if value not in final[key][lib]:
                        final[key][lib].append(value)
                else:
                    final[key][lib] = [value]
            else:
                final[key] = {}
                final[key][lib] = [value]
    write_json("E:/data/change_json.txt", final)

def get_change_info_from_project():
    final = read_json("E:/data/change_json1.txt")
    print(len(final))
    dir = "F:/shibowen/lib_update_gradle"
    files = os.listdir(dir)
    for file in files:
        print("+++++++++++++++++ " + file)
        project_id = file.replace(".txt", "")
        lines = read_file(os.path.join(dir, file))
        proj_pairs = set()
        for line in lines:
            value = line.split(" VALUES ")[1]
            value = value.replace("NULL", "'NULL'")
            value = tuple(eval(value.strip()))
            # print(value)
            project_id = value[0]
            groupId = value[2]
            artifactId = value[3]
            prev_version = value[4]
            curr_version = value[5]
            prev_commit = value[8]
            curr_commit = value[9]
            key = str(project_id) + "__fdse__" + prev_commit + "__fdse__" + curr_commit
            lib = groupId + "__fdse__" + artifactId
            value = prev_version + "__fdse__" + curr_version
            if key in final:
                if lib in final[key]:
                    if value not in final[key][lib]:
                        final[key][lib].append(value)
                else:
                    final[key][lib] = [value]
            else:
                final[key] = {}
                final[key][lib] = [value]
    write_json("E:/data/change_json2.txt", final)

def get_jar_list():
    result = {}
    db = database.connectdb()
    sql = "SELECT version_id,jar_package_url FROM version_types"
    query_result = database.querydb(db, sql)
    for entry in query_result:
        print(entry)
        version_id = entry[0]
        jar_package_url = entry[1]
        if jar_package_url.endswith(".jar"):
            sql = "SELECT group_str,name_str FROM library_versions WHERE id = " + str(version_id)
            version_info = database.querydb(db, sql)
            groupId = version_info[0][0]
            artifactId = version_info[0][1]
            key = groupId + "__fdse__" + artifactId
            if key in result:
                result[key].append(jar_package_url)
            else:
                result[key] = [jar_package_url]
    write_json_format("E:/data/lib_jar.txt", result)

def proj_200_plus():
    db = database.connectdb()
    sql = "SELECT DISTINCT project_id FROM project_lib_usage"
    query_result = database.querydb(db, sql)
    result = []
    for entry in query_result:
        project_id = entry[0]
        sql = "SELECT url FROM project WHERE id = " + str(project_id)
        url_info = database.querydb(db, sql)
        url = url_info[0][0]
        name = url.replace("https://github.com/", "").replace("/", "__fdse__")
        obj = {}
        obj["id"] = project_id
        obj["name"] = name
        result.append(obj)
    write_json("E:/data/200_plus.txt", result)


# get_proj_not_in_three()
# get_local_addr()
copy_projs()
# get_not_three_month()
# top50()
# get_gradle()
# result = read_json("E:/data/not_in_three_month_gradle.txt")
# print(len(result))
# get_commit_pair_for_project()
# get_commit_pair_from_db()
# get_change_info_from_db()
# get_change_info_from_project()
# get_jar_list()
# proj_200_plus()