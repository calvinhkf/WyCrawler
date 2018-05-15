import database
import time

from bs4 import BeautifulSoup

db = database.connectdb()

def read_library_url_from_db():
    for i in range(80000, 87170):
        # sql = "SELECT declarations FROM library_versions1 WHERE id = " + str(i)
        sql = "SELECT * FROM library_versions1 WHERE id = " + str(i)
        print('\n++++++++++++++++++++++++++++++++++++++++++++ ' + str(i))
        results = database.querydb(db, sql)
        for item in results:
            soup = BeautifulSoup(item[13], 'lxml');
            maven = soup.find(id='maven-a').string
            # print(maven)
            soup = BeautifulSoup(maven, 'xml');
            group = soup.find('groupId').string
            name = soup.find('artifactId').string
            version = soup.find('version').string
            print(group)
            print(name)
            print(version)
            # print(item[1])
            sql = "INSERT INTO library_versions" \
                  "(category_id,group_str,name_str,version,url,usages,license,categories,organization,home_page,date,files,repository,used_by,declarations," \
                  "compile_dependencies_table," \
                  "provided_dependencies_table," \
                  "test_dependencies_table," \
                  "managed_dependencies_table," \
                  "licenses_table," \
                  "developers_table," \
                  "mailing_lists_table," \
                  "page) " \
                  "VALUES (\'" \
                  + str(item[1]).replace("'", "''") + "\',\'" \
                  + str(group).replace("'", "''") + "\',\'" \
                  + str(name).replace("'", "''") + "\',\'" \
                  + str(version).replace("'", "''") + "\',\'" \
                  + str(item[3]).replace("'", "''") + "\',\'" \
                  + str(item[4]).replace("'", "''") + "\',\'" \
                  + str(item[5]).replace("'", "''") + "\',\'" \
                  + str(item[6]).replace("'", "''") + "\',\'" \
                  + str(item[7]).replace("'", "''") + "\',\'" \
                  + str(item[8]).replace("'", "''") + "\',\'" \
                  + str(item[9]).replace("'", "''") + "\',\'" \
                  + str(item[10]).replace("'", "''") + "\',\'" \
                  + str(item[11]).replace("'", "''") + "\',\'" \
                  + str(item[12]).replace("'", "''") + "\',\'" \
                  + str(item[13]).replace("'", "''") + "\',\'" \
                  + str(item[14]).replace("'", "''") + "\',\'" \
                  + str(item[15]).replace("'", "''") + "\',\'" \
                  + str(item[16]).replace("'", "''") + "\',\'" \
                  + str(item[17]).replace("'", "''") + "\',\'" \
                  + str(item[18]).replace("'", "''") + "\',\'" \
                  + str(item[19]).replace("'", "''") + "\',\'" \
                  + str(item[20]).replace("'", "''") + "\',\'" \
                  + str(item[21]).replace("'", "''") + "\')"
            database.execute_sql(db, sql)
            print('======================== INSERT INTO library_versions ')
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

def update_group_name():
    for i in range(87481, 87492):
        # sql = "SELECT declarations FROM library_versions WHERE id = " + str(i)
        sql = "SELECT * FROM library_versions WHERE id = " + str(i)
        print('\n++++++++++++++++++++++++++++++++++++++++++++ ' + str(i))
        results = database.querydb(db, sql)
        for item in results:
            soup = BeautifulSoup(item[15], 'lxml');
            maven = soup.find(id='maven-a').string
            # print(maven)
            soup = BeautifulSoup(maven, 'xml');
            group = soup.find('groupId').string
            name = soup.find('artifactId').string
            version = soup.find('version').string
            print(group)
            print(name)
            print(version)
            # print(item[1])
            sql = "UPDATE library_versions SET group_str = \'"+str(group).replace("'", "''")+"\',name_str=\'"+str(name).replace("'", "''")+"\',version=\'"+str(version).replace("'", "''")+"\' WHERE id ="+ str(i)
            # sql = "INSERT INTO library_versions" \
            #       "(category_id,group_str,name_str,version,url,usages,license,categories,organization,home_page,date,files,repository,used_by,declarations," \
            #       "compile_dependencies_table," \
            #       "provided_dependencies_table," \
            #       "test_dependencies_table," \
            #       "managed_dependencies_table," \
            #       "licenses_table," \
            #       "developers_table," \
            #       "mailing_lists_table," \
            #       "page) " \
            #       "VALUES (\'" \
            #       + str(item[1]).replace("'", "''") + "\',\'" \
            #       + str(group).replace("'", "''") + "\',\'" \
            #       + str(name).replace("'", "''") + "\',\'" \
            #       + str(version).replace("'", "''") + "\',\'" \
            #       + str(item[3]).replace("'", "''") + "\',\'" \
            #       + str(item[4]).replace("'", "''") + "\',\'" \
            #       + str(item[5]).replace("'", "''") + "\',\'" \
            #       + str(item[6]).replace("'", "''") + "\',\'" \
            #       + str(item[7]).replace("'", "''") + "\',\'" \
            #       + str(item[8]).replace("'", "''") + "\',\'" \
            #       + str(item[9]).replace("'", "''") + "\',\'" \
            #       + str(item[10]).replace("'", "''") + "\',\'" \
            #       + str(item[11]).replace("'", "''") + "\',\'" \
            #       + str(item[12]).replace("'", "''") + "\',\'" \
            #       + str(item[13]).replace("'", "''") + "\',\'" \
            #       + str(item[14]).replace("'", "''") + "\',\'" \
            #       + str(item[15]).replace("'", "''") + "\',\'" \
            #       + str(item[16]).replace("'", "''") + "\',\'" \
            #       + str(item[17]).replace("'", "''") + "\',\'" \
            #       + str(item[18]).replace("'", "''") + "\',\'" \
            #       + str(item[19]).replace("'", "''") + "\',\'" \
            #       + str(item[20]).replace("'", "''") + "\',\'" \
            #       + str(item[21]).replace("'", "''") + "\')"
            database.execute_sql(db, sql)
            print('======================== UPDATE library_versions ')
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


update_group_name()
    # read_library_url_from_db()
