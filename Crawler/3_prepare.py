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
    pattern1 = '([0-9]\d*)\.([0-9]\d*)\.([0-9]\d*)'
    pattern2 = '([0-9]\d*)\.([0-9]\d*)'
    if re.match(pattern1, string) is None:
        if re.match(pattern2, string) is None:
            return False
    return True

def get_match(string):
    pattern1 = '([0-9]\d*)\.([0-9]\d*)\.([0-9]\d*)'
    pattern2 = '([0-9]\d*)\.([0-9]\d*)'
    m1 = re.match(pattern1, string)
    if m1 is not None:
        return m1.group(1) + "." + m1.group(2) + "." + m1.group(3)
    m2 = re.match(pattern2, string)
    if m2 is not None:
        return m2.group(1) + "." + m2.group(2)
    return None

def check_version_str():
    sql = "SELECT id,prev_version,curr_version FROM third_party_library.lib_update"
    query_result = database.querydb(db, sql)
    print(len(query_result))
    # print(query_result[0][0])
    count = 0
    final = []
    for entry in query_result:
        entry_id = entry[0]
        prev_version = entry[1]
        curr_version = entry[2]
        if is_match(prev_version) and is_match(curr_version):
            count += 1
            final.append([entry_id, prev_version, curr_version])
    write_json("C:/Users/yw/Desktop/X.Y.Z_version.txt", final)
    print(len(final))
    # print(count) #5217348  5117870

def version_compare():
    json_data = read_json("C:/Users/yw/Desktop/X.Y.Z_version.txt")
    up = 0
    down = 0
    unknown = 0
    up_list = []
    down_list = []
    unknown_list = []
    for entry in json_data:
        entry_id = entry[0]
        prev_version = entry[1]
        curr_version = entry[2]
        print(entry)
        version1 = get_match(prev_version)
        version2 = get_match(curr_version)
        ver1 = version1.split(".")
        ver2 = version2.split(".")
        if int(ver1[0]) > int(ver2[0]):
            down += 1
            print("down")
            down_list.append(entry)
        elif int(ver1[0]) < int(ver2[0]):
            up += 1
            print("up")
            up_list.append(entry)
        else:
            if int(ver1[1]) > int(ver2[1]):
                down += 1
                print("down")
                down_list.append(entry)
            elif int(ver1[1]) < int(ver2[1]):
                up += 1
                print("up")
                up_list.append(entry)
            else:
                if len(ver1) ==3 and len(ver2) ==3:
                    if int(ver1[2]) > int(ver2[2]):
                        down += 1
                        print("down")
                        down_list.append(entry)
                    elif int(ver1[2]) < int(ver2[2]):
                        up += 1
                        print("up")
                        up_list.append(entry)
                    else:
                        unknown += 1
                        print("unknown")
                        unknown_list.append(entry)
                elif len(ver1) == 3:
                    if int(ver1[2]) == 0:
                        unknown += 1
                        print("unknown")
                        unknown_list.append(entry)
                    else:
                        down += 1
                        print("down")
                        down_list.append(entry)
                elif len(ver2) == 3:
                    if int(ver2[2]) == 0:
                        unknown += 1
                        print("unknown")
                        unknown_list.append(entry)
                    else:
                        up += 1
                        print("up")
                        up_list.append(entry)
                else:
                    unknown += 1
                    print("unknown")
                    unknown_list.append(entry)
    print("up" + str(up))
    print("down" + str(down))
    print("unknown" + str(unknown))
    print("up" + str(len(up_list)))
    print("down" + str(len(down_list)))
    print("unknown" + str(len(unknown_list)))
    write_json("C:/Users/yw/Desktop/up.txt", up_list)
    write_json("C:/Users/yw/Desktop/down.txt", down_list)
    write_json("C:/Users/yw/Desktop/unknown.txt", unknown_list)

def check_snapshot_in_unknown():
    json_data = read_json("C:/Users/yw/Desktop/unknown.txt")
    up = 0
    down = 0
    unknown = 0
    up_list = []
    down_list = []
    unknown_list = []
    for entry in json_data:
        prev_version = entry[1]
        curr_version = entry[2]
        print(entry)
        version1 = get_match(prev_version)
        version2 = get_match(curr_version)
        prefix1 = prev_version.replace(version1, "")
        prefix2 = curr_version.replace(version2, "")
        print(prefix1 + " " + prefix2)
        if (prefix1.endswith("SNAPSHOT") and prefix2.endswith("SNAPSHOT")) or (not prefix1.endswith("SNAPSHOT") and not prefix2.endswith("SNAPSHOT")):
            unknown += 1
            print("unknown")
            unknown_list.append(entry)
        elif prefix1.endswith("SNAPSHOT") and prefix1.startswith(prefix2):
            up += 1
            print("up")
            up_list.append(entry)
        elif prefix2.endswith("SNAPSHOT") and prefix2.startswith(prefix1):
            down += 1
            print("down")
            down_list.append(entry)
        else:
            unknown += 1
            print("unknown")
            unknown_list.append(entry)
    print("up" + str(up))
    print("down" + str(down))
    print("unknown" + str(unknown))
    print("up" + str(len(up_list)))
    print("down" + str(len(down_list)))
    print("unknown" + str(len(unknown_list)))
    write_json("C:/Users/yw/Desktop/snapshot_up.txt", up_list)
    write_json("C:/Users/yw/Desktop/snapshot_down.txt", down_list)
    write_json("C:/Users/yw/Desktop/snapshot_unknown.txt", unknown_list)
    # up603779
    # down38179
    # unknown762005

def distinguish_major_minor_patch():
    json_data = read_json("C:/Users/yw/Desktop/down.txt")
    major = 0
    minor = 0
    patch = 0
    for entry in json_data:
        prev_version = entry[1]
        curr_version = entry[2]
        ver1 = prev_version.split(".")
        ver2 = curr_version.split(".")
        ver13 = None
        ver23 = None
        print(entry)
        if len(prev_version) > len(ver1[0]+"."+ver1[1]):
            ver13 = prev_version[len(ver1[0]+"."+ver1[1]):]
        if len(curr_version) > len(ver2[0]+"."+ver2[1]):
            ver23 = curr_version[len(ver2[0]+"."+ver2[1]):]
        if ver1[0] != ver2[0]:
            major += 1
            # print("major")
        elif ver1[1] != ver2[1]:
            minor += 1
            # print("minor")
        elif (ver13 is None and ver23 is not None) or (ver13 is not None and ver23 is None):
            patch += 1
            # print("patch")
        elif ver13 != ver23:
            patch += 1
            # print("patch")
        # else:
        #     print(entry)
        #     print(ver13)
        #     print(ver23)
    print("major" + str(major))
    print("minor" + str(minor))
    print("patch" + str(patch))

def update_module_in_usage():
    sql = "SELECT * FROM `usage`"
    query_result = database.querydb(db, sql)
    print(len(query_result))
    curr_values = []
    for entry in query_result:
        module_ = entry[6]
        # if module_.endswith(".gradle"):
        #     print("++++++++++++++ "+ module_)
        module_ = module_.replace("\\", "/")
        if module_.endswith(".gradle"):
            module_ = module_.replace("I:/projects/", "")
        else:
            if module_ == '':
                module_ = "pom.xml"
            else:
                module_ = module_ + "/pom.xml"
        # if module_.endswith(".gradle"):
        #     print(module_)
        entry_list = list(entry)
        entry_list[6] = module_
        print(tuple(entry_list))
        curr_values.append(tuple(entry_list))
    print(len(curr_values))
    write_json("D:/data/data_copy/usage.txt", curr_values)

def insert_to_usage():
    cursor = db.cursor()
    json_data = read_json("D:/data/data_copy/usage.txt")
    print(len(json_data))
    curr_values = []
    for entry in json_data:
        curr_values.append(entry)
        if len(curr_values) == 5000:
            cursor.executemany(
                'INSERT INTO `usage` (project_id,group_str,name_str,version,type,classifier,module,library_id,version_id) value (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                curr_values)
            db.commit()
            curr_values = []
            print(5000)
    cursor.executemany(
        'INSERT INTO `usage` (project_id,group_str,name_str,version,type,classifier,module,library_id,version_id) value (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        curr_values)
    db.commit()

def update_module_in_project_lib_usage():
    sql = "SELECT * FROM `project_lib_usage`"
    query_result = database.querydb(db, sql)
    print(len(query_result))
    curr_values = []
    for entry in query_result:
        module_ = entry[2]
        if module_.endswith(".gradle"):
            print("++++++++++++++ "+ module_)
            print(module_.split("\\")[0])
            print(module_.split("/")[0])
    #     module_ = module_.replace("\\", "/")
    #     if module_.endswith(".gradle"):
    #         module_ = module_.replace("I:/projects/", "")
    #     else:
    #         if module_ == '':
    #             module_ = "pom.xml"
    #         else:
    #             module_ = module_ + "/pom.xml"
    #     # if module_.endswith(".gradle"):
    #     #     print(module_)
    #     entry_list = list(entry)
    #     entry_list[6] = module_
    #     print(tuple(entry_list))
    #     curr_values.append(tuple(entry_list))
    # print(len(curr_values))
    # write_json("D:/data/data_copy/usage.txt", curr_values)

# release_version_check()
# print(is_match("3.4.5sfs"))
# print(get_match("3.4-243"))
# check_version_str()
# version_compare()
# check_snapshot_in_unknown()
# distinguish_major_minor_patch()
update_module_in_project_lib_usage()
# insert_to_usage()