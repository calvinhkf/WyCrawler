import json

import os

import database
from exception import CustomizeException

db = database.connectdb()

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
    for i in range(1, 7102):
        sql = "SELECT * FROM library_versions WHERE id = " + str(i)
        version_info = database.querydb(db, sql)
        if len(version_info) != 0:
            key = version_info[0][2]+" "+version_info[0][3]
            if key not in li:
                li.append(key)
                index = li.index(key) + 1
                sql = "UPDATE library_versions SET category_id = " + str(index) +" WHERE id =" + str(i)
                database.execute_sql(db, sql)
            else:
                index = li.index(key) + 1
                sql = "UPDATE library_versions SET category_id = " + str(index) +" WHERE id =" + str(i)
                database.execute_sql(db, sql)

    # print(len(li))
    # print(li)
    # print(li.index("com.squareup fest-android"))
    for category in li:
        name = category.split(" ")
        if len(name) != 2:
            raise (CustomizeException("length is not 2"))
        else:
            sql = "INSERT INTO library (group_str,name_str) VALUES ('" + name[0] + "','" + name[1] + "')"
            database.execute_sql(db, sql)


def update_lib_usage():
    sql = "SELECT * FROM project_lib_usage"
    usage_info = database.querydb(db, sql)
    for entry in usage_info:
        version_type_id = entry[1]
        project_id = entry[0]
        library_id = entry[3]
        sql = "SELECT * FROM library_category_relation WHERE library_id = " + str(library_id)
        relation = database.querydb(db, sql)
        if len(relation) != 0:
            category_id = relation[0][0]
            sql = "UPDATE project_lib_usage SET category_id = " + str(category_id) + " WHERE version_type_id =" + str(
                version_type_id) + " AND project_id = " + str(project_id)
            database.execute_sql(db, sql)
        # version_type_id = entry[1]
        # project_id = entry[0]
        # sql = "SELECT * FROM version_types WHERE type_id = " +str(version_type_id)
        # type_info = database.querydb(db, sql)
        # if len(type_info) != 0:
        #     version_id = type_info[0][1]
        #     sql = "SELECT * FROM library_versions WHERE id = " + str(version_id)
        #     version_info = database.querydb(db, sql)
        #     if len(version_info) != 0:
        #         library_id = version_info[0][1]
        #         sql = "UPDATE project_lib_usage SET library_id = " + str(library_id) + " WHERE version_type_id =" + str(version_type_id) + " AND project_id = " + str(project_id)
        #         database.execute_sql(db, sql)

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


# update_lib_update()
# update_lib_update()
# get_api_call_lib()
# api_count()