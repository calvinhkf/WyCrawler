import os
import database

from file_util import read_json, write_json

db = database.connectdb()

def get_jars_used_by_project():
    projs = {}
    proj_data = read_json("proj_in_usage.txt")
    for data in proj_data:
        project_id = data["id"]
        local_addr = data["local_addr"]
        local_addr = local_addr.replace("F:/wangying/projects_last_unzips/", "").replace("C:/", "").replace("D:/", "").replace("E:/", "").replace("F:/", "").replace("gradle_maven200_500/", "").replace("gradle_maven500/",
                                                                                           "").replace("maven200_500/","").replace("maven500/", "").replace("gradle200_500/", "").replace("gradle500/", "");
        projs[project_id] = local_addr
        # print(local_addr)
    projs[1492] = "belaban__fdse__JGroups"
    projs[5422] = "rsocket__fdse__rsocket-java"

    result = []
    proj_files = os.listdir("E:/data/proj_update_lib")
    print(len(proj_files))
    for proj_file in proj_files:
        print(proj_file)
        project_id = int(proj_file.replace(".txt", ""))
        if project_id not in projs:
            print(project_id)
            continue
        proj_path = projs[project_id]
        # print(proj_path)
        lib_array = []
        lib_data = read_json(os.path.join("E:/data/proj_update_lib",proj_file))
        for key in lib_data.keys():
            libs = lib_data[key]
            for lib_id in libs:
                sql = "SELECT * FROM version_types where type_id = " + str(lib_id)
                query_result = database.querydb(db,sql)
                jar_name = query_result[0][5]
                if jar_name not in lib_array:
                    lib_array.append(jar_name)
                    # print(jar_name)
        proj_obj = {}
        proj_obj["id"] = project_id
        proj_obj["path"] = proj_path
        proj_obj["lib_array"] = lib_array
        result.append(proj_obj)

    write_json("jars.txt",result)

get_jars_used_by_project()