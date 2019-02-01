import json

import os

import database
from exception import CustomizeException
from file_util import write_json, read_json

db = database.connectdb()
cursor = db.cursor()

li = []
project = []
categories = []

def all_projects():
    pro_local_path = "F:/GP/high_quality_repos/"
    index = -1
    lib_dic = {}
    with open("C:\\Users\\yw\\Desktop\\pro.txt", "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            # print(lines[i])
            lines[i] = lines[i].strip('\n')

            if lines[i].startswith("../data/prior_repository/"):
                absolutePath = pro_local_path +lines[i][25:];
                print(os.path.exists(absolutePath))
                if os.path.exists(absolutePath):
                    li.append(index)
            else:
                index = lines[i]
            # lines[i] = lines[i].strip('\n')
    f.close()
    print(len(li))
    with open("project.txt", 'w') as file_object:
        json.dump(li, file_object)

def get_categories():
    for i in range(1, 7102):
        sql = "SELECT * FROM library_versions WHERE id = " + str(i)
        version_info = database.querydb(db, sql)
        if len(version_info) != 0:
            category_str = version_info[0][8]
            library_id = version_info[0][1]
            if category_str != "None":
                category_list = json.loads(category_str)
                for category in category_list:
                    if category not in categories:
                        categories.append(category)
                        index = categories.index(category) + 1
                        sql = "INSERT IGNORE INTO library_category_relation (category_id,library_id) VALUES (" + str(index) + "," + str(library_id) + ")"
                        print("insert " +category+" "+str(index)+" "+str(library_id))
                        database.execute_sql(db, sql)
                    else:
                        index = categories.index(category) + 1
                        sql = "INSERT IGNORE INTO library_category_relation (category_id,library_id) VALUES (" + str(index) + "," + str(library_id) + ")"
                        print("insert " + category + " " + str(index) + " " + str(library_id))
                        database.execute_sql(db, sql)
    for category in categories:
        sql = "INSERT INTO library_categories (name) VALUES ('" + category + "')"
        database.execute_sql(db, sql)

def get_libraries():
    for i in range(1, 695504):
        sql = "SELECT * FROM library_versions WHERE id = " + str(i)
        version_info = database.querydb(db, sql)
        if len(version_info) != 0:
            key = version_info[0][2]+" "+version_info[0][3]
            if key not in li:
                li.append(key)
                index = li.index(key) + 1
                sql = "UPDATE library_versions SET library_id = " + str(index) +" WHERE id =" + str(i)
                database.execute_sql(db, sql)
            else:
                index = li.index(key) + 1
                sql = "UPDATE library_versions SET library_id = " + str(index) +" WHERE id =" + str(i)
                database.execute_sql(db, sql)

    print(len(li))
    # print(li)
    # print(li.index("com.squareup fest-android"))
    write_json("library_temp.txt",li)

    # li = ["1 2"]
    version_values = []
    for category in li:
        name = category.split(" ")
        if len(name) != 2:
            raise (CustomizeException("length is not 2"))
        else:
            version_values.append((name[0], name[1]))
            if len(version_values) == 5000:
                cursor.executemany(
                    'INSERT INTO library (group_str,name_str) VALUE (%s,%s)',
                    version_values)
                db.commit()
                version_values = []
                print(5000)
            # sql = "INSERT INTO library (group_str,name_str) VALUES ('" + name[0] + "','" + name[1] + "')"
            # database.execute_sql(db, sql)
    cursor.executemany(
        'INSERT INTO library (group_str,name_str) value (%s,%s)',
        version_values)
    db.commit()


def update_lib_usage():
    # sql = "SELECT * FROM project_lib_usage"
    # usage_info = database.querydb(db, sql)
    # for entry in usage_info:
    #     # version_type_id = entry[1]
    #     # project_id = entry[0]
    #     # library_id = entry[3]
    #     # sql = "SELECT * FROM library_category_relation WHERE library_id = " + str(library_id)
    #     # relation = database.querydb(db, sql)
    #     # if len(relation) != 0:
    #     #     category_id = relation[0][0]
    #     #     sql = "UPDATE project_lib_usage SET category_id = " + str(category_id) + " WHERE version_type_id =" + str(
    #     #         version_type_id) + " AND project_id = " + str(project_id)
    #     #     database.execute_sql(db, sql)
    #     # version_type_id = entry[1]
    #     # project_id = entry[0]
    #     # sql = "SELECT * FROM version_types WHERE type_id = " +str(version_type_id)
    #     # type_info = database.querydb(db, sql)
    #     # if len(type_info) != 0:
    #     #     version_id = type_info[0][1]
    #     #     sql = "SELECT * FROM library_versions WHERE id = " + str(version_id)
    #     #     version_info = database.querydb(db, sql)
    #     #     if len(version_info) != 0:
    #     #         library_id = version_info[0][1]
    #     #         sql = "UPDATE project_lib_usage SET library_id = " + str(library_id) + " WHERE version_type_id =" + str(version_type_id) + " AND project_id = " + str(project_id)
    #     #         database.execute_sql(db, sql)
    #     version_type_id = entry[1]
    #     project_id = entry[0]
    #     module_ = entry[2]
    #     sql = "SELECT * FROM version_types WHERE type_id = " + str(version_type_id)
    #     type_info = database.querydb(db, sql)
    #     if len(type_info) != 0:
    #         version_id = type_info[0][1]
    #         sql = "UPDATE project_lib_usage SET version_id = " + str(version_id) + " WHERE version_type_id =" + str(
    #             version_type_id) + " AND project_id = " + str(project_id) + " AND module = '" + module_ + "'"
    #         database.execute_sql(db, sql)

    sql = "SELECT distinct(version_id) FROM project_lib_usage"
    usage_info = database.querydb(db, sql)
    for entry in usage_info:
        version_id = entry[0]
        sql = "SELECT * FROM library_versions WHERE id = " + str(version_id)
        version_info = database.querydb(db, sql)
        if len(version_info) != 0:
            library_id = version_info[0][1]
            sql = "UPDATE project_lib_usage SET library_id = " + str(library_id) + " WHERE version_id =" + str(version_id)
            database.execute_sql(db, sql)

def update_lib_update():
    sql = "SELECT * FROM lib_update"
    usage_info = database.querydb(db, sql)
    for entry in usage_info:
        group_str = entry[4]
        name_str = entry[5]
        id = entry[0]
        print(group_str + " " + name_str)
        sql = "SELECT * FROM library WHERE group_str = '" + str(group_str) +"' and name_str = '"+name_str+"'"
        library = database.querydb(db, sql)
        if len(library) != 0:
            library_id = library[0][0]
            sql = "UPDATE lib_update SET lib_id = " + str(library_id) + " WHERE id =" + str(id)
            database.execute_sql(db, sql)

def update_type_id_in_lib_update():
    prev_values = []
    curr_values = []
    sql = "SELECT id,group_str,name_str,prev_version,curr_version,type,classifier FROM lib_update where id >= 423118"
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
            prev_type_id = in_version_type_table(prev_version_id, _type, classifier)
            if prev_type_id > 0:
                # print(prev_type_id)
                prev_values.append((id, prev_type_id))
                if len(prev_values) == 5000:
                    cursor.executemany('INSERT INTO lib_update (id,prev_type_id) value (%s,%s) on duplicate key update prev_type_id = values(prev_type_id)',prev_values)
                    db.commit()
                    prev_values = []
                    cursor.executemany('INSERT INTO lib_update (id,curr_type_id) value (%s,%s) on duplicate key update curr_type_id = values(curr_type_id)',curr_values)
                    db.commit()
                    curr_values = []
                    print("prev  "+str(5000))
                # sql = "UPDATE lib_update SET prev_type_id = " + str(prev_type_id) + " WHERE id =" + str(id)
                # database.execute_sql(db, sql)


        sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
            artifactId) + "' and version = '" + str(curr_verison) + "'"
        curr_version_info = database.querydb(db, sql)
        if len(curr_version_info) == 1 or len(curr_version_info) == 2:
            curr_version_id = curr_version_info[0][0]
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
                    print("curr  "+str(5000))
        #         sql = "UPDATE lib_update SET curr_type_id = " + str(curr_type_id) + " WHERE id =" + str(id)
        #         database.execute_sql(db, sql)

    cursor.executemany('INSERT INTO lib_update (id,prev_type_id) value (%s,%s) on duplicate key update prev_type_id = values(prev_type_id)',prev_values)
    db.commit()
    cursor.executemany('INSERT INTO lib_update (id,curr_type_id) value (%s,%s) on duplicate key update curr_type_id = values(curr_type_id)',curr_values)
    db.commit()


def in_version_type_table(version_id,type_,classifier):
    sql = "SELECT * FROM version_types WHERE type = '" + str(type_) + "' and (version_id = " + str(
        version_id) + " or version_id2 = " + str(version_id) + ")"
    types = database.querydb(db, sql)
    for t in types:
        if (classifier is not None and classifier == t[4]) or (classifier == None and t[4] == None):
            return t[0]
    return -1

def get_api_call_lib():
    for i in range(10000,20000):
        print(i)
        sql = "SELECT * FROM api_call where id = "+str(i)
        usage_info = database.querydb(db, sql)
        for entry in usage_info:
            api_id = entry[2]
            sql = "SELECT * FROM api_interface WHERE id = " + str(api_id)
            api_interface = database.querydb(db, sql)
            if len(api_interface) != 0:
                class_id = api_interface[0][1]
                sql = "SELECT * FROM api_classes WHERE id = " + str(class_id)
                api_class = database.querydb(db, sql)
                if len(api_class) != 0:
                    version_type_id = api_class[0][1]
                    sql = "SELECT * FROM version_types WHERE type_id = " + str(version_type_id)
                    version_types = database.querydb(db, sql)
                    if len(version_types) != 0:
                        version_id = version_types[0][1]
                        sql = "SELECT * FROM library_versions WHERE id = " + str(version_id)
                        library_versions = database.querydb(db, sql)
                        if len(library_versions) != 0:
                            library_id = library_versions[0][1]
                            sql = "UPDATE api_call SET lib_id = " + str(library_id) + " WHERE id =" + str(i)
                            database.execute_sql(db,sql)

def api_count():
    for i in range(3000,3454):
        print("------------"+str(i))
        total = 0
        sql = "SELECT * FROM library_versions WHERE library_id = " + str(i)
        library_versions = database.querydb(db, sql)
        for version in library_versions:
            version_id= version[0]
            sql = "SELECT * FROM version_types WHERE version_id = " + str(version_id)
            version_types = database.querydb(db, sql)
            for type_ in version_types:
                type_id = type_[0]
                sql = "SELECT * FROM api_classes WHERE version_type_id = " + str(type_id)
                api_classes = database.querydb(db, sql)
                for clazz in api_classes:
                    class_id = clazz[0]
                    sql = "SELECT count(*) FROM api_interface WHERE class_id = " + str(class_id)
                    count = database.querydb(db, sql)
                    if len(count) !=0:
                        # print(count[0][0])
                        total += count[0][0]
        sql = "INSERT INTO api_count (lib_id,count) VALUES (" + str(i) + "," + str(total) + ")"
        database.execute_sql(db, sql)
        print(total)

def top_library():
    # sql = "SELECT library_id,count(distinct(project_id)) FROM project_lib_usage group by library_id order by count(distinct(project_id)) desc"
    # query_result = database.querydb(db,sql)
    # print(query_result)
    # write_json("top_library.txt ",query_result)

    # top_list = read_json("top_library.txt")
    # top_list = top_list[0:50]
    # print(len(top_list))
    # print(top_list)
    # write_json("top_library.txt ", top_list)

    top_list = read_json("top_library.txt")
    for lib in top_list:
        library_id = lib[0]
        count = lib[1]
        sql = "SELECT * FROM library where id = " + str(library_id)
        lib_result = database.querydb(db,sql)
        if len(lib_result) > 0:
            group = lib_result[0][1]
            name = lib_result[0][2]
            print(group + " : " + name + " (" + str(count)+")")
        else:
            raise CustomizeException("library_id:" + str(library_id))


# update_lib_update()
# update_lib_update()
# get_api_call_lib()
# api_count()
# get_libraries()
update_lib_usage()
# top_library()//70583
# update_type_id_in_lib_update()