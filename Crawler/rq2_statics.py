import os
import sys
import time

import database

from exception import CustomizeException
from file_util import read_file, append_file, read_json, write_json


def distinct():
    dir = "C:/data/three_month/lib_update_gradle"
    file_list = os.listdir(dir)
    for file in file_list:
        # print(file)
        # if file != "1840.txt":
        #     continue
        lines = read_file(os.path.join(dir, file))
        # new = set(lines)
        # for line in new:
        #     # print(line)
        #     append_file("C:/data/three_month/lib_update_distinct/1840.txt", line)
        # new = set()
        # for line in lines:
        #     if line in new:
        #         print(line)
        #         continue
        #     new.add(line)
        # print(len(new))
        new = set(lines)
        # print(len(new))
        if len(new) != len(lines):
            print(file)
            print(len(new))
            print(len(lines))

def lib_update_data_to_db():
    db = database.connectdb()
    cursor = db.cursor()
    update_values = []
    dir = "C:/data/three_month/lib_update_gradle"
    file_list = os.listdir(dir)
    count = 0
    for file in file_list:
        project_id = int(file.replace(".txt", ""))
        # sql = "SELECT * FROM lib_update WHERE project_id = " + str(project_id)
        # query_result = database.querydb(db, sql)
        # if len(query_result) > 0:
        #     continue
        print("++++++++++++++++++++++++ " + file)
        lines = read_file(os.path.join(dir, file))
        for line in lines:
            # print(line)
            value = line.split(" VALUES ")[1]
            # try:
            value = value.replace("NULL", "'NULL'")
            value = tuple(eval(value.strip()))
            # except:
            #     # print(value)
            #     append_file("C:/data/three_month/lib_update_unsolved.txt", line)
            #     # raise CustomizeException(value)
            #     # sys.exit(0)
            #     continue
            # count += 1
    # print(count)
            if len(value) != 13:
                print(value)
                print(len(value))
            value_list = list(value)
            value_list[6] = None
            value = tuple(value_list)
            print(value)
            update_values.append(value)
            if len(update_values) == 5000:
                cursor.executemany(
                    'INSERT INTO lib_update (project_id,file,group_str,name_str,prev_version,curr_version,prev_time,curr_time,prev_commit,curr_commit,remark,type,classifier) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    update_values)
                db.commit()
                update_values = []
                print(5000)
    cursor.executemany(
        'INSERT INTO lib_update (project_id,file,group_str,name_str,prev_version,curr_version,prev_time,curr_time,prev_commit,curr_commit,remark,type,classifier) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        update_values)
    db.commit()

def update_type_and_version_id_in_lib_update():
    prev_values = []
    curr_values = []
    prev_versions = []
    curr_versions = []
    sql = "SELECT id,group_str,name_str,prev_version,curr_version,type,classifier FROM lib_update where id > 5189589"
    update_info = database.querydb(db, sql)
    for entry in update_info:
        groupId = entry[1]
        artifactId = entry[2]
        prev_verison = entry[3]
        curr_verison = entry[4]
        _type = entry[5]
        classifier = entry[6]
        id = entry[0]
        print(str(id) + " : "+groupId + " " + artifactId)

        sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
            artifactId) + "' and version = '" + str(prev_verison) + "'"
        prev_version_info = database.querydb(db, sql)
        if len(prev_version_info) == 1 or len(prev_version_info) == 2:
            prev_version_id = prev_version_info[0][0]
            prev_versions.append((id, prev_version_id))
            prev_type_id = in_version_type_table(prev_version_id, _type, classifier)
            if prev_type_id > 0:
                prev_values.append((id, prev_type_id))
                if len(prev_values) == 5000:
                    cursor.executemany('INSERT INTO lib_update (id,prev_type_id) value (%s,%s) on duplicate key update prev_type_id = values(prev_type_id)',prev_values)
                    db.commit()
                    prev_values = []
                    cursor.executemany('INSERT INTO lib_update (id,curr_type_id) value (%s,%s) on duplicate key update curr_type_id = values(curr_type_id)',curr_values)
                    db.commit()
                    curr_values = []
                    cursor.executemany('INSERT INTO lib_update (id,prev_version_id) value (%s,%s) on duplicate key update prev_version_id = values(prev_version_id)',prev_versions)
                    db.commit()
                    prev_versions = []
                    cursor.executemany('INSERT INTO lib_update (id,curr_version_id) value (%s,%s) on duplicate key update curr_version_id = values(curr_version_id)',curr_versions)
                    db.commit()
                    curr_versions = []
                    print("prev  "+str(5000))

        sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
            artifactId) + "' and version = '" + str(curr_verison) + "'"
        curr_version_info = database.querydb(db, sql)
        if len(curr_version_info) == 1 or len(curr_version_info) == 2:
            curr_version_id = curr_version_info[0][0]
            curr_versions.append((id, curr_version_id))
            curr_type_id = in_version_type_table(curr_version_id, _type, classifier)
            if curr_type_id > 0:
                curr_values.append((id, curr_type_id))
                if len(curr_values) == 5000:
                    cursor.executemany('INSERT INTO lib_update (id,curr_type_id) value (%s,%s) on duplicate key update curr_type_id = values(curr_type_id)',curr_values)
                    db.commit()
                    curr_values = []
                    cursor.executemany('INSERT INTO lib_update (id,prev_type_id) value (%s,%s) on duplicate key update prev_type_id = values(prev_type_id)',prev_values)
                    db.commit()
                    prev_values = []
                    cursor.executemany('INSERT INTO lib_update (id,prev_version_id) value (%s,%s) on duplicate key update prev_version_id = values(prev_version_id)',prev_versions)
                    db.commit()
                    prev_versions = []
                    cursor.executemany('INSERT INTO lib_update (id,curr_version_id) value (%s,%s) on duplicate key update curr_version_id = values(curr_version_id)',curr_versions)
                    db.commit()
                    curr_versions = []
                    print("curr  "+str(5000))
        #         sql = "UPDATE lib_update SET curr_type_id = " + str(curr_type_id) + " WHERE id =" + str(id)
        #         database.execute_sql(db, sql)

    cursor.executemany('INSERT INTO lib_update (id,prev_type_id) value (%s,%s) on duplicate key update prev_type_id = values(prev_type_id)',prev_values)
    db.commit()
    cursor.executemany('INSERT INTO lib_update (id,curr_type_id) value (%s,%s) on duplicate key update curr_type_id = values(curr_type_id)',curr_values)
    db.commit()
    cursor.executemany('INSERT INTO lib_update (id,prev_version_id) value (%s,%s) on duplicate key update prev_version_id = values(prev_version_id)',prev_versions)
    db.commit()
    cursor.executemany('INSERT INTO lib_update (id,curr_version_id) value (%s,%s) on duplicate key update curr_version_id = values(curr_version_id)',curr_versions)
    db.commit()

def in_version_type_table(version_id,type_,classifier):
    sql = "SELECT * FROM version_types WHERE type = '" + str(type_) + "' and (version_id = " + str(
        version_id) + " or version_id2 = " + str(version_id) + ")"
    types = database.querydb(db, sql)
    for t in types:
        if (classifier is not None and classifier == t[4]) or (classifier == None and t[4] == None):
            return t[0]
    return -1

def update_classifier():
    db = database.connectdb()
    cursor = db.cursor()
    sql = "SELECT id FROM lib_update WHERE classifier = 'null'"
    query_result = database.querydb(db, sql)
    curr_values = []
    for entry in query_result:
        id = entry[0]
        print(id)
        curr_values.append((id, None))
        if len(curr_values) == 5000:
            cursor.executemany(
                'INSERT INTO lib_update (id,classifier) value (%s,%s) on duplicate key update classifier = values(classifier)',
                curr_values)
            db.commit()
            curr_values = []
            print(str(5000))
        # break
    cursor.executemany(
        'INSERT INTO lib_update (id,classifier) value (%s,%s) on duplicate key update classifier = values(classifier)',
        curr_values)
    db.commit()

def update_time_in_lib_update():
    sql = "SELECT id,curr_time,prev_version_id,curr_version_id FROM lib_update where id > 3527352 and (prev_version_id is not null or curr_version_id is not null)"
    # sql = "SELECT id,curr_time,prev_version_id,curr_version_id FROM lib_update where id = 3"
    query_result = database.querydb(db, sql)
    print(len(query_result))
    curr_values = []
    for entry in query_result:
        id = entry[0]
        # if id == 3573890:
        #     continue
        print("entry id :" + str(id))
        curr_time = entry[1]
        prev_version_id = entry[2]
        curr_version_id = entry[3]
        prev_date = None
        curr_date = None
        library_id = None
        prev_num = None
        curr_num = None
        time_interval = None
        if prev_version_id is not None:
            sql = "SELECT library_id,parsed_date FROM library_versions where id = " + str(prev_version_id)
            prev_info = database.querydb(db, sql)
            library_id = prev_info[0][0]
            prev_date = prev_info[0][1]
            prev_num = parse_date(prev_date)
        if curr_version_id is not None:
            sql = "SELECT library_id,parsed_date FROM library_versions where id = " + str(curr_version_id)
            curr_info = database.querydb(db, sql)
            library_id = curr_info[0][0]
            curr_date = curr_info[0][1]
            curr_num = parse_date(curr_date)
        if curr_time is not None and curr_num is not None:
            time_interval = (curr_time - curr_num)/60/60
        curr_values.append((id, library_id, time_interval, prev_num, curr_num))
        print((id, library_id, time_interval, prev_num, curr_num))
        if len(curr_values) == 5000:
            cursor.executemany(
                'INSERT INTO lib_update (id,lib_id,time_interval,prev_release_time_num,curr_release_time_num) VALUE (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE lib_id = VALUES(lib_id),time_interval = VALUES(time_interval),prev_release_time_num = VALUES(prev_release_time_num),curr_release_time_num = VALUES(curr_release_time_num)',
                curr_values)
            db.commit()
            curr_values = []
            print("unique " + str(5000))
        # break
    cursor.executemany(
        'INSERT INTO lib_update (id,lib_id,time_interval,prev_release_time_num,curr_release_time_num) VALUE (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE lib_id = VALUES(lib_id),time_interval = VALUES(time_interval),prev_release_time_num = VALUES(prev_release_time_num),curr_release_time_num = VALUES(curr_release_time_num)',
        curr_values)
    db.commit()

def parse_date(time1):
    # time1 = time.strptime(date_str, "%Y-%m-%d")
    time_int = int(time.mktime(time1.timetuple()))
    return time_int

def parse_gradle_update():
    dir = "E:/lib_update_new/ok-ide/ok"
    files = os.listdir(dir)
    project_ids = set()
    for file in files:
        print(file)
        # id = file.split("_")[0]
        # project_ids.add(id)
        # continue
        json_data = read_json(os.path.join(dir, file))
        dependencyUrlList = json_data["dependencyUrlList"]
        parentDependencyUrlList = json_data["parentDependencyUrlList"]
        parent_dict = {}
        for den in parentDependencyUrlList:
            groupId = den["groupId"]
            artifactId = den["artifactId"]
            type_ = den["type"]
            version = den["version"]
            path = den["path"]
            key = groupId + " " + artifactId + " " + type_
            if path in parent_dict:
                if key in parent_dict[path]:
                    if version not in parent_dict[path][key]:
                        parent_dict[path][key].append(version)
                else:
                    parent_dict[path][key] = [version]
            else:
                new_obj = {}
                new_obj[key] = [version]
                parent_dict[path] = new_obj
        # print(parent_dict)
        compare_dict = {}
        for den in dependencyUrlList:
            groupId = den["groupId"]
            artifactId = den["artifactId"]
            type_ = den["type"]
            version = den["version"]
            path = den["path"]
            key = groupId + " " + artifactId + " " + type_
            if path in parent_dict and key in parent_dict[path]:
                if version in parent_dict[path][key]:
                    continue
                for prev_ver in parent_dict[path][key]:
                    if version != prev_ver:
                        value = prev_ver + " " + version
                        if path in compare_dict:
                            if key in compare_dict[path]:
                                if value not in compare_dict[path][key]:
                                    compare_dict[path][key].append(value)
                            else:
                                compare_dict[path][key] = [value]
                        else:
                            new_obj = {}
                            new_obj[key] = [value]
                            compare_dict[path] = new_obj
        print(compare_dict)
        if len(compare_dict) > 0:
            write_json("C:/data/lib_update_ide/"+file, compare_dict)
    # print(len(project_ids))
    # print(project_ids)
        # break
        # split_str = file.replace(".txt", "").split("_")
        # project_id = split_str[0]
        # prev_commit = split_str[1]
        # curr_commit = split_str[2]
        # curr_time = int(split_str[3])
        # print(project_id)
        # print(prev_commit)
        # print(curr_commit)
        # print(curr_time)
        # break
def gradle_to_sql():
    dir = "C:/data/lib_update"
    files = os.listdir(dir)
    for file in files:
        # print(file)
        split_str = file.replace(".txt", "").split("_")
        project_id = split_str[0]
        curr_commit = split_str[1]
        prev_commit = split_str[2]
        curr_time = int(split_str[3])
        json_data = read_json(os.path.join(dir, file))
        for path in json_data.keys():
            lib_dict = json_data[path]
            for lib in lib_dict.keys():
                lib_str = lib.split(" ")
                groupId = lib_str[0]
                artifactId = lib_str[1]
                type_ = lib_str[2]
                value_list = lib_dict[lib]
                for value in value_list:
                    value_str = value.split(" ")
                    prev_version = value_str[0]
                    curr_version = value_str[1]
                    sql = "INSERT INTO lib_update(project_id,file,group_str,name_str,prev_version,curr_version,prev_time,curr_time,prev_commit,curr_commit,remark,type,classifier) VALUES ("+str(project_id)+",'"+path+"','"+groupId+"','"+artifactId+"','"+prev_version+"','"+curr_version+"',NULL,"+str(curr_time)+",'"+prev_commit+"','"+curr_commit+"','modified', '"+type_+"', NULL)"
                    if groupId is None or artifactId is None or prev_version is None or curr_version is None or type_ is None or '${' in groupId or '${' in artifactId or '${' in prev_version or '${' in curr_version or '${' in type_ or '@' in groupId or '@' in artifactId or '@' in prev_version or '@' in curr_version or '@' in type_:
                        # print(sql)
                        continue
                    if type(prev_version)==list or type(curr_version)==list:
                        continue
                    # append_file("C:/data/three_month/lib_update_gradle/" + str(project_id) + ".txt", sql)
        # break

def delete_unparsed():
    # if groupId is None or artifactId is None or version is None or type_ is None or '${' in groupId or '${' in artifactId or '${' in version or '${' in type_ or '@' in groupId or '@' in artifactId or '@' in version or '@' in type_:
    # sql = "SELECT * FROM third_party_library.lib_update where group_str like '%@%' or name_str like '%@%'  or prev_version like '%@%' or curr_version like '%@%' or type like '%@%' or classifier like '%@%'"
    # # sql = "SELECT * FROM third_party_library.lib_update where group_str like '%$%' or name_str like '%$%'  or prev_version like '%$%' or curr_version like '%$%' or type like '%$%' or classifier like '%$%'"
    # query_result = database.querydb(db, sql)
    # print(len(query_result))
    # total_ids = set()
    # for entry in query_result:
    #     entry_id = entry[0]
    #     total_ids.add(entry_id)
    # write_json("C:/Users/yw/Desktop/ids1.txt", list(total_ids))
    #     print(entry[4] + " " + entry[5] + " " + entry[6] + " " + entry[7])
    ids = read_json("C:/Users/yw/Desktop/ids.txt")
    ids1 = read_json("C:/Users/yw/Desktop/ids1.txt")
    ids.extend(ids1)
    ids = set(ids)
    print(len(ids))
    for id in ids:
        print(id)
        sql = "delete FROM third_party_library.lib_update where id = " + str(id)
        database.execute_sql(db, sql)
        # break
    # sql = "delete FROM third_party_library.lib_update where group_str like '%$%' or name_str like '%$%'  or prev_version like '%$%' or curr_version like '%$%' or type like '%$%' or classifier like '%$%'"
    # database.execute_sql(db, sql)

def temp_sql():
    # sql = "SELECT count(*) FROM third_party_library.lib_update where prev_version like '%SNAPSHOT' or curr_version like '%SNAPSHOT'"
    # query_result = database.querydb(db, sql)
    # print(query_result[0][0])

    sql = "SELECT parsed_date FROM library_versions where id < 4 and id > 1"
    query_result = database.querydb(db, sql)
    print(query_result[0][0])
    time1 = parse_date(query_result[0][0])
    print(query_result[1][0])
    time2 = parse_date(query_result[1][0])
    print((time2 - time1) / 60 / 60 / 24)

# distinct()
# lib_update_data_to_db()
# update_classifier()
db = database.connectdb()
cursor = db.cursor()
# gradle_to_sql()
# update_type_and_version_id_in_lib_update()
# time1 = parse_date("2012-03-09")
# time2 = parse_date("2013-04-12")
# print((time2-time1)/60/60/24)
parse_gradle_update()
# update_time_in_lib_update()
# temp_sql()



