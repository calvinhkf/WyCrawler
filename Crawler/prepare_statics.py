import os
import shutil

from exception import CustomizeException
from file_util import read_json, read_file, write_json
import database

def android_proj():
    android_count = 0
    no_count = 0
    m_g_count = 0
    lines = read_file("C:/Users/yw/Desktop/I-result-7-25_500.txt")
    for line in lines:
        if line == "proj-type: android":
            android_count += 1
        elif line == "proj-type: no":
            no_count += 1
        elif line == "proj-type: maven" or line == "proj-type: gradle" or line == "proj-type: maven-gradle":
            m_g_count += 1
        elif line.startswith("proj-type:"):
            print(line)

    lines = read_file("C:/Users/yw/Desktop/I-result-7-25.txt")
    for line in lines:
        if line == "proj-type: android":
            android_count += 1
        elif line == "proj-type: no":
            no_count += 1
        elif line == "proj-type: maven" or line == "proj-type: gradle" or line == "proj-type: maven-gradle":
            m_g_count += 1
        elif line.startswith("proj-type:"):
            print(line)
    #
    print(android_count)
    print(no_count)
    print(m_g_count)

def collect_projs():
    db = database.connectdb()
    dir = "E:/data/dependency/gradle_all"
    files = os.listdir(dir)
    for file in files:
        name = "https://github.com/" + file.replace(".txt", "").replace("__fdse__", "/")
        sql = "SELECT * FROM project where url = '" + name + "' and stars > 200"
        query_result = database.querydb(db, sql)
        id = query_result[0][0]
        shutil.copyfile(dir + "/" + file, "E:/data/dependency/gradle_id/" + str(id) + ".txt")
        # _type = query_result[0][8]
        # # print(_type)
        # if _type != "gradle":
        #     print(file)

def dependency_statics():
    count = 0
    # dir = "E:/data/curr_result8.5(maven_gradle)"
    # files = os.listdir(dir)
    # for file in files:
    #     data = read_json(os.path.join(dir, file))
    #     for lib in data:
    #         if 'id' in lib:
    #             project_id = lib["id"]
    #             print("-------------------- project_id: " + str(project_id))
    #             continue
    #         count += 1
    # print(count)

    # dir = "E:/data/dependency/gradle_id"
    # files = os.listdir(dir)
    # for file in files:
    #     print("-------------------- project_id: " + str(file))
    #     json_data = read_json(os.path.join(dir, file))
    #     dependency_list = json_data["dependencyUrls"]
    #     count += len(dependency_list)
    #     # for lib in dependency_list:
    #     #     count += 1
    # print(count)

    # new_list = []
    # new_list = read_json("E:/data/curr_result_statics/total.txt")
    # print(len(new_list))
    # dir = "E:/data/curr_result8.5(maven_gradle)"
    # files = os.listdir(dir)
    # for file in files:
    #     data = read_json(os.path.join(dir, file))
    #     for lib in data:
    #         if 'id' in lib:
    #             project_id = lib["id"]
    #             print("-------------------- project_id: " + str(project_id))
    #             continue
    #         new_list.append(lib)
    # write_json("E:/data/curr_result_statics/total.txt", new_list)

    # dir = "E:/data/dependency/gradle_id"
    # files = os.listdir(dir)
    # for file in files:
    #     print("-------------------- project_id: " + str(file))
    #     json_data = read_json(os.path.join(dir, file))
    #     dependency_list = json_data["dependencyUrls"]
    #     for lib in dependency_list:
    #         lib["type"] = "jar"
    #         lib["classifier"] = None
    #         new_list.append(lib)
    # write_json("E:/data/curr_result_statics/total.txt", new_list)

    new_list = read_json("E:/data/curr_result_statics/total.txt")
    print(len(new_list))
    for lib in new_list:
        if "groupId" not in lib or "artifactId" not in lib or "version" not in lib or "type" not in lib:
            print(False)
            continue
        groupId= lib["groupId"]
        artifactId = lib["artifactId"]
        version = lib["version"]
        type_ = lib["type"]
        if groupId is None or artifactId is None or version is None or type_ is None or '${' in groupId or '${' in artifactId or '${' in version or '${' in type_:
            print("groupId: " + str(groupId) +"   artifactId: " + str(artifactId)+"   version: " + str(version)+"   type: " + str(type_) )
            print(False)
            continue
        classifier = None
        if "classifier" in lib:
            classifier = lib["classifier"]
            if '${' in classifier:
                print("groupId: " + str(groupId) + "   artifactId: " + str(artifactId) + "   version: " + str(
                    version) + "   type: " + str(type_) + "   classifier: " + str(classifier))
                print(False)
                continue
        if type(version) == list:
            continue



# android_proj()
# json_data = read_json("E:/data/projs.json");
# print(len(json_data))
# collect_projs()
dependency_statics()