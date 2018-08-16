import database
from exception import CustomizeException
from file_util import write_json, read_json

db = database.connectdb()

record_result = []
def find_same_time_in_diff_versions():
    # sql = "SELECT count(DISTINCT version),group_str,name_str,repository,date FROM library_versions where date is not null group by group_str,name_str,repository,date"
    # query_result = database.querydb(db,sql)
    # for record in query_result:
    #     count = record[0]
    #     if count > 1:
    #         record_result.append(record)
    #         print(record)
    #         # group_str = record[1]
    #         # name_str = record[2]
    #         # repository = record[3]
    #         # date = record[4]
    # print(len(query_result))
    # print(query_result[0])
    # write_json("record.txt", record_result)

    count = 0
    json_data = read_json("record.txt")

    for data in json_data:
        num = data[0]
        groupId = data[1]
        artifactId = data[2]
        repository = data[3]
        date = data[4]
        if num > 4:
            print(data)
            count += 1
    print(count)

def find_same_version_in_diff_repo():
    sql = "SELECT count(*) FROM library_versions group by group_str,name_str,version"
    query_result = database.querydb(db, sql)
    print(len(query_result))
    print(query_result[0])

def update_record():
    count = 0
    json_data = read_json("new_record.txt")
    print("whole length: " + str(len(json_data)))
    i = 0
    while i < len(json_data):
        # if json_data[i][2] == "wicket-util":
        if json_data[i][0] == 2:
            count += 1
            print(json_data[i])
            json_data.pop(i)
            i -= 1
        i += 1
    print(count)
    print("last length: " + str(len(json_data)))
    write_json("new_record.txt",json_data)

def print_data():
    json_data = read_json("new_record.txt")
    count = 0
    for data in json_data:
        print(data)
        groupId = data[1]
        artifactId = data[2]
        repository = data[3]
        sql = "SELECT * FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
            artifactId) + "' and repository != '" + str(repository) + "'"
        version_info = database.querydb(db, sql)
        if len(version_info) > 0:
            count += 1
    print(len(json_data))
    print("count:"+str(count))

def print_unique_data():
    count = 0
    json_data = read_json("same_repo.txt")
    for data in json_data:
        # if data[2] == "wicket-ioc":
        if data[0] != 2:
            print(data)
            count += 1
    print(count)

def unify_time_for_same_version_in_same_repo():
    last_record = []
    sql = "SELECT count(*),group_str,name_str,version,repository FROM library_versions group by group_str,name_str,version,repository"
    query_result = database.querydb(db, sql)
    print(len(query_result))
    for record in query_result:
        count = record[0]
        if count > 1:
            # if count != 2:
            #     raise CustomizeException("length = "+str(count))
            last_record.append(record)
            print(record)
    print(len(last_record))
    write_json("same_repo1.txt", last_record)

    # count = 0
    # json_data = read_json("same_repo1.txt")
    # for data in json_data:
    #     if data[0] == 2:
    #         groupId = data[1]
    #         artifactId = data[2]
    #         version = data[3]
    #         repository = data[4]
    #         sql = "SELECT id,date FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
    #             artifactId) + "' and version = '" + str(version) +"' and repository = '" + str(repository) + "'"
    #         query_result = database.querydb(db, sql)
    #         date1 = query_result[0][1]
    #         date2 = query_result[1][1]
    #         # date3 = query_result[2][1]
    #         # date4 = query_result[3][1]
    #         # date5 = query_result[4][1]
    #         # date6 = query_result[5][1]
    #         # date7 = query_result[6][1]
    #         # if date1 == date2 == date3 == date4 == date5 == date6 == date7:
    #         count += 1
    #         print(data)
    #         print(str(date1)+"  "+str(date2))
                # print(str(date1) + "  " + str(date2) + "  " + str(date3) + "  " + str(date4) + "  " + str(date5) + "  " + str(date6) + "  " + str(date7))
            # print(query_result[1][0])
            # if date1 == date2 == date3:
            #     sql = "delete FROM library_versions WHERE id = " + str(query_result[1][0])
            #     database.execute_sql(db,sql)
            #     sql = "delete FROM library_versions WHERE id = " + str(query_result[2][0])
            #     database.execute_sql(db, sql)
            #     sql = "delete FROM library_versions WHERE id = " + str(query_result[3][0])
            #     database.execute_sql(db, sql)
            #     sql = "delete FROM library_versions WHERE id = " + str(query_result[4][0])
            #     database.execute_sql(db, sql)
            #     sql = "delete FROM library_versions WHERE id = " + str(query_result[5][0])
            #     database.execute_sql(db, sql)
            #     sql = "delete FROM library_versions WHERE id = " + str(query_result[6][0])
            #     database.execute_sql(db, sql)
    print(count)

def unify_time_for_same_version_in_diff_repo():
    # last_record = []
    # sql = "SELECT count(*),group_str,name_str,version FROM library_versions group by group_str,name_str,version"
    # query_result = database.querydb(db, sql)
    # print(len(query_result))
    # for record in query_result:
    #     count = record[0]
    #     if count > 1:
    #         # if count != 2:
    #         #     raise CustomizeException("length = "+str(count))
    #         last_record.append(record)
    #         print(record)
    # print(len(last_record))
    # write_json("diff_repo.txt", last_record)

    count = 0
    json_data = read_json("diff_repo.txt")
    for data in json_data:
        if data[0] == 2:
            groupId = data[1]
            artifactId = data[2]
            version = data[3]
            sql = "SELECT id,date,repository FROM library_versions WHERE group_str = '" + str(groupId) + "' and name_str = '" + str(
                artifactId) + "' and version = '" + str(version) +"'"
            query_result = database.querydb(db, sql)
            date1 = query_result[0][1]
            date2 = query_result[1][1]
            # date3 = query_result[2][1]
            # date4 = query_result[3][1]
            # date5 = query_result[4][1]
            # date6 = query_result[5][1]
            # date7 = query_result[6][1]
            repostiory1 = query_result[0][2]
            repostiory2 = query_result[1][2]
            # if date1 == date2 == date3 == date4 == date5 == date6 == date7:
            count += 1
            print(data)
            print(str(date1)+"  "+str(repostiory1))
            print(str(date2) + "  " + str(repostiory2))
    # print(str(date1) + "  " + str(date2) + "  " + str(date3) + "  " + str(date4) + "  " + str(date5) + "  " + str(date6) + "  " + str(date7))
    # print(query_result[1][0])
    # if date1 == date2 == date3:
    #     sql = "delete FROM library_versions WHERE id = " + str(query_result[1][0])
    #     database.execute_sql(db,sql)
    #     sql = "delete FROM library_versions WHERE id = " + str(query_result[2][0])
    #     database.execute_sql(db, sql)
    #     sql = "delete FROM library_versions WHERE id = " + str(query_result[3][0])
    #     database.execute_sql(db, sql)
    #     sql = "delete FROM library_versions WHERE id = " + str(query_result[4][0])
    #     database.execute_sql(db, sql)
    #     sql = "delete FROM library_versions WHERE id = " + str(query_result[5][0])
    #     database.execute_sql(db, sql)
    #     sql = "delete FROM library_versions WHERE id = " + str(query_result[6][0])
    #     database.execute_sql(db, sql)
    print(count)

def get_repos_with_null_date():
    # sql = "SELECT distinct(repository) FROM library_versions where date is null"
    # query_result = database.querydb(db,sql)
    # write_json("repos.txt",query_result)

    json_data = read_json("repos.txt")
    print(len(json_data))
    for data in json_data:
        print(data)

def crawl_date_for_one_repo():
    # count = 0
    for i in range(1,2):
        json_data = read_json(str(i)+"_repo.txt")
        # count += len(json_data)
        print(len(json_data))
        for data in json_data:
            print(data)
            id = data[0]
            groupId = data[1]
            artifactId = data[2]
            version = data[3]
            repository = data[4]

def get_data_for_crawling_date():
    json_data = read_json("repos.txt")
    print(len(json_data))
    index = 0
    for data in json_data:
        index += 1
        print(data[0])
        sql = "SELECT id,group_str,name_str,version,repository,date,url FROM library_versions where date is null and repository = '" + str(
            data[0]) + "'"
        query_result = database.querydb(db, sql)
        write_json(str(index) + "_repo.txt", query_result)

# find_same_time_in_diff_versions()
# find_same_time_in_diff_versions()
# update_record()
# print_data()
# print_unique_data()
# unify_time_for_same_version_in_diff_repo()
# find_same_time_in_diff_versions()
# get_repos_with_null_date()
# crawl_date_for_one_repo()
# get_data_for_crawling_date()