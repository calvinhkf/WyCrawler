import os
import sys
import time

import database

from exception import CustomizeException
from file_util import read_file, append_file


def distinct():
    dir = "C:/data/three_month/lib_update_distinct"
    file_list = os.listdir(dir)
    for file in file_list:
        print(file)
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
        print(len(new))
        if len(new) != len(lines):
            print(file)
            print(len(new))
            print(len(lines))

def lib_update_data_to_db():
    db = database.connectdb()
    cursor = db.cursor()
    update_values = []
    dir = "C:/data/three_month/lib_update_distinct"
    file_list = os.listdir(dir)
    for file in file_list:
        project_id = int(file.replace(".txt", ""))
        sql = "SELECT * FROM lib_update WHERE project_id = " + str(project_id)
        query_result = database.querydb(db, sql)
        if len(query_result) > 0:
            continue
        print("++++++++++++++++++++++++ " + file)
        lines = read_file(os.path.join(dir, file))
        for line in lines:
            # print(line)
            value = line.split(" VALUES ")[1]
            try:
                value = tuple(eval(value.strip()))
            except:
                append_file("C:/data/three_month/lib_update_unsolved.txt", line)
                # raise CustomizeException(value)
                # sys.exit(0)
                continue
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
    sql = "SELECT id,group_str,name_str,prev_version,curr_version,type,classifier FROM lib_update where id > 3889039"
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
    db = database.connectdb()
    cursor = db.cursor()
    sql = "SELECT id,prev_version_id,curr_version_id FROM lib_update where prev_version_id is not null or curr_version_id is not null"
    query_result = database.querydb(db, sql)
    curr_values = []
    for entry in query_result:
        id = entry[0]
        print(id)
        prev_version_id = entry[1]
        curr_version_id = entry[2]
        prev_date  = None
        curr_date = None
        library_id = None
        prev_num = None
        curr_num = None
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
        curr_values.append((id, library_id, prev_date, curr_date, prev_num, curr_num))
        if len(curr_values) == 5000:
            cursor.executemany(
                'INSERT INTO lib_update (id,library_id, prev_date, curr_date, prev_num, curr_num) value (%s,%s,%s,%s,%s,%s) on duplicate key update classifier = values(classifier)',
                curr_values)
            db.commit()
            curr_values = []
            print(str(5000))
        # break
    # cursor.executemany(
    #     'INSERT INTO lib_update (id,classifier) value (%s,%s) on duplicate key update classifier = values(classifier)',
    #     curr_values)
    # db.commit()

def parse_date(date_str):
    time1 = time.strptime(date_str, "%Y-%m-%d")
    time_int = int(time.mktime(time1))
    return time_int

# distinct()
# lib_update_data_to_db()
# update_classifier()
db = database.connectdb()
cursor = db.cursor()
# update_type_and_version_id_in_lib_update()
time1 = parse_date("2012-03-09")
time2 = parse_date("2013-04-12")
print((time2-time1)/60/60/24)