import os
import database

from handle_jar_db import insert_project_lib_usage, insert_library_version, insert_version_type
from file_util import read_json

db = database.connectdb()
lib_path = "C:/Users/yw/Desktop/lib/"
result_path ="C:/Users/yw/Desktop/result/"
output_path ="C:/Users/yw/Desktop/"

def parse_file_data():
    for i in range(1, 2):
        if os.path.exists(output_path + str(i) + ".txt"):
            data = read_json(output_path + str(i) + ".txt")
            for entry_dic in data:
                if "version_type" not in entry_dic or "lib_usage" not in entry_dic or "library_version" not in entry_dic:
                    continue
                version_type_dic = entry_dic["version_type"]
                lib_usage_dic = entry_dic["lib_usage"]
                library_version_dic = entry_dic["library_version"]

                _type = version_type_dic["_type"]
                classifier = version_type_dic["classifier"]
                jar_package_url = version_type_dic["jar_package_url"]

                module_ = lib_usage_dic["module_"]

                group = library_version_dic["group"]
                name = library_version_dic["name"]
                version = library_version_dic["version"]
                version_url = library_version_dic["version_url"]
                license_= library_version_dic["license"]
                categories = library_version_dic["categories"]
                organization = library_version_dic["organization"]
                home_page = library_version_dic["home_page"]
                date = library_version_dic["date"]
                files = library_version_dic["files"]
                repository = library_version_dic["repository"]
                used_by = library_version_dic["used_by"]
                category_url = library_version_dic["category_url"]

                sql = "SELECT * FROM library_versions WHERE group_str = '" + str(group) + "' and name_str = '" + str(
                    name) + "' and version = '" + str(version) + "'"
                version_info = database.querydb(db, sql)
                if len(version_info) != 0:
                    version_id = version_info[0][0]
                    files = version_info[0][12]
                    print("+++++++++++++++++++++++++version_id:" + str(version_id))
                    sql = "SELECT * FROM version_types WHERE version_id = " + str(version_id)
                    types = database.querydb(db, sql)
                    for t in types:
                        if t[2] == _type:
                            insert_project_lib_usage(i, t[0], module_)
                            return
                else:
                    version_id = insert_library_version(group, name, version, version_url, license_, categories,
                                                        organization, home_page, date,
                                                        files, repository, used_by, category_url)
                version_type_id = insert_version_type(version_id, _type, classifier, jar_package_url)
                insert_project_lib_usage(i, version_type_id, module_)