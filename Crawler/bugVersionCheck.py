import os

import database
from exception import CustomizeException
from file_util import read_json, write_json

db = database.connectdb()

def parse_bug_info():
    version_dic = {}
    version_dic["CLI"] = "commons-cli commons-cli"
    version_dic["CODEC"] = "commons-codec commons-codec"
    version_dic["COLLECTIONS"] = "commons-collections commons-collections"
    version_dic["COMMON-IO"] = "commons-io commons-io"
    version_dic["HTTPCLIENT"] = "org.apache.httpcomponentnents httpclient"
    version_dic["LOGBACK"] = "ch.qos.logback logback-classic"
    version_dic["LOGGING"] = "commons-logging commons-logging"

    bug_info_dir = "C:/RQ3"
    bug_files = os.listdir(bug_info_dir)
    for file in bug_files:
        file_name = file.replace(".txt","")
        result = []
        if file_name not in version_dic:
            continue
        name_str = version_dic[file_name]
        if os.path.exists("C:/RQ3/" + name_str + ".txt"):
            continue
        # name_str.split(" : ")
        bugs = read_json(os.path.join(bug_info_dir,file))
        for key in bugs.keys():
            if key == "size":
                continue
            bug_list = bugs[key]["bugs"]
            for bug in bug_list:
                print(bug)
                affectsVersions = bug["affectsVersions"]
                versions = affectsVersions.split(",")
                for version in versions:
                    version = version.strip()
                    if version not in result:
                        result.append(version)
        print("C:/RQ3/" + name_str + ".txt")
        write_json("C:/RQ3/" + name_str + ".txt", result)
        print(result)
        # break

def parse_for_LANG():
    result = []
    result3 = []
    name_str = "commons-lang commons-lang"
    name_str3 = "org.apache.commonsmons commons-lang3"
    bug_info_dir = "C:/RQ3"
    bug_files = os.listdir(bug_info_dir)
    for file in bug_files:
        if file == "LANG.txt":
            bugs = read_json(os.path.join(bug_info_dir, file))
            for key in bugs.keys():
                if key == "size":
                    continue
                bug_list = bugs[key]["bugs"]
                for bug in bug_list:
                    print(bug)
                    affectsVersions = bug["affectsVersions"]
                    versions = affectsVersions.split(",")
                    for version in versions:
                        version = version.strip()
                        if version.startswith("2"):
                            if version not in result:
                                result.append(version)
                        else:
                            if version not in result3:
                                result3.append(version)
            # print("C:/RQ3/" + name_str + ".txt")
            write_json("C:/RQ3/" + name_str + ".txt", result)
            write_json("C:/RQ3/" + name_str3 + ".txt", result3)
            # print(result)

def parse_for_LOG4J2():
    result = []
    result_core = []
    name_str = "log4j log4j"
    core_str = "org.apache.logging.log4j log4j-core"
    bug_info_dir = "C:/RQ3"
    bug_files = os.listdir(bug_info_dir)
    for file in bug_files:
        if file == "LOG4J2.txt":
            bugs = read_json(os.path.join(bug_info_dir, file))
            for key in bugs.keys():
                if key == "size":
                    continue
                bug_list = bugs[key]["bugs"]
                for bug in bug_list:
                    print(bug)
                    components = bug["components"]
                    components_array = components.split(",")
                    affectsVersions = bug["affectsVersions"]
                    versions = affectsVersions.split(",")
                    for version in versions:
                        version = version.strip()
                        for com in components_array:
                            com = com.strip()
                            if com == "Core":
                                if version not in result_core:
                                    result_core.append(version)
                            else:
                                if version not in result:
                                    result.append(version)
            # print("C:/RQ3/" + name_str + ".txt")
            write_json("C:/RQ3/" + name_str + ".txt", result)
            write_json("C:/RQ3/" + core_str + ".txt", result_core)
            # print(result)

def parse_for_SLF4J():
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    name_str1 = "org.slf4j slf4j-simple"
    name_str2 = "org.slf4j jcl-over-slf4j"
    name_str3 = "org.slf4j slf4j-log4j12"
    name_str4 = "org.slf4j slf4j-api"
    bug_info_dir = "C:/RQ3"
    bug_files = os.listdir(bug_info_dir)
    for file in bug_files:
        if file == "SLF4J.txt":
            bugs = read_json(os.path.join(bug_info_dir, file))
            for key in bugs.keys():
                if key == "size":
                    continue
                bug_list = bugs[key]["bugs"]
                for bug in bug_list:
                    print(bug)
                    components = bug["components"]
                    components_array = components.split(",")
                    affectsVersions = bug["affectsVersions"]
                    versions = affectsVersions.split(",")
                    for version in versions:
                        version = version.strip()
                        for com in components_array:
                            com = com.strip()
                            if com == "slf4j-simple":
                                if version not in result1:
                                    result1.append(version)
                            elif com == "jcl-over-slf4j":
                                if version not in result2:
                                    result2.append(version)
                            elif com == "log4j-over-slf4j":
                                if version not in result3:
                                    result3.append(version)
                            elif com == "Core API":
                                if version not in result4:
                                    result4.append(version)
            # print("C:/RQ3/" + name_str + ".txt")
            write_json("C:/RQ3/" + name_str1 + ".txt", result1)
            write_json("C:/RQ3/" + name_str2 + ".txt", result2)
            write_json("C:/RQ3/" + name_str3 + ".txt", result3)
            write_json("C:/RQ3/" + name_str4 + ".txt", result4)
            # print(result)


def lib_classification():
    version_dic = {}
    # version_dic["LANG"] =
    # version_dic["LOG4J2"] =
    # version_dic["SLF4J"] =
    # read_json("COLLECTIONS.txt")

def collect_proj_with_bugs():
    bug_version_dir = "C:/RQ3/lib_versions"
    files = os.listdir(bug_version_dir)
    for file in files:
        if file != "org.slf4j slf4j-log4j12.txt":
        # if file == "org.apache.commons commons-lang3.txt" or file == "org.apache.httpcomponents httpclient_orgin.txt":
            continue
        result = {}
        name_str = file.replace(".txt","")
        name_array = name_str.split(" ")
        groupId  = name_array[0]
        artifactId = name_array[1]
        version_list = read_json(os.path.join(bug_version_dir,file))
        for version in version_list:
            sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
                artifactId) + "' and version = '" + str(version) + "'"
            version_info = database.querydb(db,sql)
            if len(version_info) == 0:
                result[version] = []
                continue
            if len(version_info) == 2:
                version_id = version_info[0][0]
                version_id2 = version_info[1][0]
                sql = "SELECT distinct project_id FROM project_lib_usage where version_id = "+str(version_id)+" or version_id = "+str(version_id2)
                query_result = database.querydb(db,sql)
            elif len(version_info) == 1:
                version_id = version_info[0][0]
                sql = "SELECT distinct project_id FROM project_lib_usage where version_id = " + str(
                    version_id)
                query_result = database.querydb(db, sql)
            else:
                raise CustomizeException("length != 2:" + name_str + " " +version)
            proj_ids = []
            for entry in query_result:
                project_id = entry[0]
                proj_ids.append(project_id)
            result[version] = proj_ids
        write_json("C:/RQ3/projects/"+file, result)

def collect_proj_with_bugs_for_lang3():
    bug_version_dir = "C:/RQ3/lib_versions"
    files = os.listdir(bug_version_dir)
    for file in files:
        if file != "org.apache.commons commons-lang3.txt":
            continue
        result = {}
        name_str = file.replace(".txt","")
        name_array = name_str.split(" ")
        groupId  = name_array[0]
        artifactId = name_array[1]
        version_list = read_json(os.path.join(bug_version_dir,file))
        for version in version_list:
            if version == "3.x":
                sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
                    artifactId) + "' and version like '3.%'"
                version_info = database.querydb(db, sql)
                sql = "SELECT distinct project_id FROM project_lib_usage where "
                for i in range(0,len(version_info)):
                    if i == 0:
                        sql += "version_id = '"+str(version_info[i][0])+"'"
                    else:
                        sql += " or version_id = '" + str(version_info[i][0]) + "'"
                    query_result = database.querydb(db, sql)
            else:
                sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
                    artifactId) + "' and version = '" + str(version) + "'"
                version_info = database.querydb(db,sql)
                if len(version_info) == 0:
                    result[version] = []
                    continue
                if len(version_info) == 2:
                    version_id = version_info[0][0]
                    version_id2 = version_info[1][0]
                    sql = "SELECT distinct project_id FROM project_lib_usage where version_id = "+str(version_id)+" or version_id = "+str(version_id2)
                    query_result = database.querydb(db,sql)
                elif len(version_info) == 1:
                    version_id = version_info[0][0]
                    sql = "SELECT distinct project_id FROM project_lib_usage where version_id = " + str(
                        version_id)
                    query_result = database.querydb(db, sql)
                else:
                    raise CustomizeException("length != 2:" + name_str + " " +version)
            proj_ids = []
            for entry in query_result:
                project_id = entry[0]
                proj_ids.append(project_id)
            result[version] = proj_ids
        write_json("C:/RQ3/projects/"+file, result)

def read_projs_with_bugs():
    projects_dir = "C:/RQ3/projects"
    files = os.listdir(projects_dir)
    for file in files:
        name_str = file.replace(".txt", "")
        versions = read_json(os.path.join(projects_dir,file))
        for key in versions.keys():
            pro_list = versions[key]
            print(name_str + " " + key + " ("+str(len(pro_list))+")")

def read_projs_with_bugs_for_lib():
    projects_dir = "C:/RQ3/projects"
    files = os.listdir(projects_dir)
    for file in files:
        whole_list = []
        name_str = file.replace(".txt", "")
        versions = read_json(os.path.join(projects_dir,file))
        for key in versions.keys():
            pro_list = versions[key]
            whole_list = whole_list + pro_list
        whole_list = list(set(whole_list))
        print(name_str + " ("+str(len(whole_list))+")")


# group_str = 'org.apache.commons' and name_str = 'commons-lang3' and version like '3.%'

        # parse_bug_info()
# parse_for_LANG()
# parse_for_LOG4J2()
# parse_for_SLF4J()
collect_proj_with_bugs()
# collect_proj_with_bugs_for_lang3()
# read_projs_with_bugs()
# read_projs_with_bugs_for_lib()