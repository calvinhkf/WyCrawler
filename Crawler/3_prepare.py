import re

import database

from file_util import read_json, write_json

db = database.connectdb()

def release():
    ver = set()
    versions = read_json("D:/data/data_copy/figure/datas/version_ids.txt")
    for id in versions:
        sql = "SELECT group_str,name_str,repository FROM library_versions WHERE id = " + str(id)
        version_info = database.querydb(db, sql)
        groupId = version_info[0][0]
        artifactId = version_info[0][1]
        repository = version_info[0][2]
        key = groupId + " " + artifactId + " " + repository
        ver.add(key)
    total = 0
    version_names = []
    for entry in ver:
        key_list = entry.split(" ")
        groupId = key_list[0]
        artifactId = key_list[1]
        repository = key_list[2]
        sql = "SELECT version FROM library_versions WHERE group_str = '" + groupId + "' and name_str = '" + artifactId + "' and repository = '" + repository + "'"
        version_result = database.querydb(db, sql)
        for i in version_result:
            version_names.append(i[0])
    # print(total)
    write_json("D:/data/data_copy/figure/datas/version_names.txt", version_names)

    # lib = set()
    # sql = "SELECT group_str,name_str FROM `usage`"
    # usage_info = database.querydb(db, sql)
    # for entry in usage_info:
    #     groupId = entry[0]
    #     artifactId = entry[1]
    #     key = groupId + " " + artifactId
    #     lib.add(key)
    # sql = "SELECT group_str,name_str FROM library"
    # usage_info = database.querydb(db, sql)
    # for entry in usage_info:
    #     groupId = entry[0]
    #     artifactId = entry[1]
    #     key = groupId + " " + artifactId
    #     lib.add(key)
    # print(len(lib))

    # lib = set()
    # sql = "SELECT group_str,name_str FROM `usage`"
    # usage_info = database.querydb(db, sql)
    # for entry in usage_info:
    #     groupId = entry[0]
    #     artifactId = entry[1]
    #     key = groupId + " " + artifactId
    #     lib.add(key)
    # sql = "SELECT group_str,name_str FROM library"
    # usage_info = database.querydb(db, sql)
    # for entry in usage_info:
    #     groupId = entry[0]
    #     artifactId = entry[1]
    #     key = groupId + " " + artifactId
    #     lib.add(key)
    # print(len(lib))

def release_version_check():
    # 132973
    version_names = read_json("D:/data/data_copy/figure/datas/version_names.txt")
    # print(len(version_names))#323885
    # print(is_match("0.0.00"))
    count = 0
    for name in version_names:
        print(name)
        matched = is_match(name)
        print(matched)
        if matched:
            count += 1
    print(count)

def is_match(string):
    pattern = '([0-9]\d*)\.([0-9]\d*)\.([0-9]\d*)'
    if re.match(pattern, string) is None:
        return False
    return True

release_version_check()