import os
import shutil
import database

from file_util import read_json

db = database.connectdb()

jars_path = "E:/data/projs8.11.json"
file_dir = "G:/project_call/batch"
def move_jar():
    json_data = read_json(jars_path)
    print(len(json_data))
    count = 0
    dir_count = 1
    os.mkdir(file_dir +"/" + str(dir_count))
    save_dir = file_dir + "/" + str(dir_count)
    for data in json_data:
        count += 1
        url = data["url"]
        sql = "SELECT id FROM project WHERE url = '"+url+"'"
        query_result = database.querydb(db,sql)
        project_id = query_result[0][0]
        print(file_dir + "/"+str(project_id)+".sh")
        if os.path.exists(file_dir + "/"+str(project_id)+".sh"):
            shutil.move(file_dir + "/"+str(project_id)+".sh", save_dir + "/batch"+str(project_id)+".sh")
        if count == 132:
            count = 0
            dir_count += 1
            os.mkdir(file_dir +"/" + str(dir_count))
            save_dir = file_dir +"/" + str(dir_count)

move_jar()