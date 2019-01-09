import os

from file_util import read_json, write_json


def merge_project_call():
    dir = ""
    file_list = os.listdir(dir)
    curr_id = None
    call_list = []
    for file in file_list:
        project_id = int(file.split("_")[0])
        new_list = read_json(os.path.join(dir,file))
        if curr_id is None:
            curr_id = project_id
            call_list.extend(new_list)
        elif curr_id != project_id:
            write_json("/" + str(project_id) + ".txt", call_list)
            curr_id = None
            call_list = []
        else:
            call_list.extend(new_list)
            continue

def extract_api_call():
    dir = "projec_call"
    file_list = os.listdir(dir)
    for file in file_list:
        project_id = int(file.replace(".txt", ""))
        calls = read_json(os.path.join(dir, file))
        lib_list = read_json("C:/lib_list/" + str(project_id) + ".json")
        for lib in lib_list:
            if os.path.exists(lib + ".json"):
                json_data = read_json(lib + ".json")
                for clazz in json_data:
                    class_name = clazz["className"].replace("$", ".")
                    fields = clazz["fields"]


