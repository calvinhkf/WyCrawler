import random
import requests
import time

import database
import proxy
from bs4 import BeautifulSoup

from exception import CustomizeException

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
proxy_ip = {
    'http': '202.194.14.72:8118',
    'https': '202.194.14.72:8118'
}
# proxy_ip = {
#     'http': 'socks5://127.0.0.1:1080',
#     'https': 'socks5://127.0.0.1:1080'
# }
pool = []
main_url = 'http://mvnrepository.com'
r = requests.get(main_url+"/open-source") #像目标url地址发送get请求，返回一个response对象
soup = BeautifulSoup(r.text, 'lxml');
index = 1
db = database.connectdb()

def read_library_url_from_db():
    for i in range(7796, 16664):
        # ip_index = random.randint(0, len(pool)-1)
        # proxy_ip.clear()
        # proxy_ip['http'] = pool[ip_index]
        # proxy_ip['https'] = pool[ip_index]
        # print(proxy_ip['http'])
        sql = "SELECT * FROM library_url WHERE id = " + str(i)
        results = database.querydb(db, sql)
        for item in results:
            library_url = item[1]
            print('+++++++++++++++++++++++++++++++++++  '+str(i)+':  '+library_url)
            get_library_information(library_url)

def get_library_information(url):
    time.sleep(random.randint(15, 20))
    library = requests.get(url, headers=headers)
    # library = requests.get(url, proxies=proxy_ip)
    # print(library.text)
    library_soup = BeautifulSoup(library.text, 'lxml');
    name = None
    results = library_soup.find(class_='im-title')
    if results is not None and results.a is not None:
        name = results.a.string.replace('\n', '')
    results = library_soup.find(class_='im-description')
    if results is None:
        print("||||||||||||||||||||||||||||||||||||||| error")
        return
    description = results.string
    results = library_soup.find(class_='grid').find_all('tr')
    license = None
    categories = None
    tags = None
    used_by = None
    for tr in results:
        if tr.th is not None:
            if tr.th.string == 'License':
                license = tr.td.span.string.replace('\n', '')
            elif tr.th.string == 'Categories':
                if tr.td.a is not None:
                    categories = "{'"+tr.td.a.string.replace('\n', '')+"':'"+"http://mvnrepository.com"+tr.td.a["href"] + "'}"
            elif tr.th.string == 'Tags':
                entries = tr.td.find_all('a')
                if entries is not None:
                    tags = "{"
                    for each in entries:
                        tags = tags + "'"+each.string.replace('\n', '')+"':'"+"http://mvnrepository.com"+each["href"] + "',"
                    if tags[len(tags)-1]==",":
                        tags = tags[:-1]
                    tags = tags + "}"
            elif tr.th.string == 'Used By':
                if tr.td.a is not None:
                    used_by = "{'"+tr.td.a.string.replace('\n', '') + "':'" + "http://mvnrepository.com" + tr.td.a["href"] + "'}"

    sql = "INSERT INTO library_category_information(name,description,license,categories,tags,used_by,url,page) VALUES (\'" \
          + str(name).replace("'", "''") + "\',\'" \
          + str(description).replace("'", "''") + "\',\'" \
          + str(license).replace("'", "''") + "\',\'" \
          + str(categories).replace("'", "''") + "\',\'" \
          + str(tags).replace("'", "''") + "\',\'" \
          + str(used_by).replace("'", "''") + "\',\'" \
          + str(url).replace("'", "''") + "\',\'" \
          + str(library.text).replace("'", "''") + "\')"
    database.execute_sql(db, sql)
    print('======================== INSERT INTO library_category_information ')
    sql = "SELECT LAST_INSERT_ID()"
    results = database.querydb(db, sql)
    category_id = results[0][0]
    print('IIIIIIIIIIIIIIIIIIIIIIII category_id:  '+str(category_id))
    results = library_soup.find('ul', class_='tabs').find_all('li')
    for tab in results:
        get_library_versions("http://mvnrepository.com" + tab.a["href"], url, category_id)

def get_library_versions(tab_url, category_url, category_id):
    time.sleep(random.randint(12, 15))
    print('------------------------- tab_url:'+tab_url)
    library_tab = requests.get(tab_url, headers=headers)
    # library_tab = requests.get(tab_url, proxies=proxy_ip)
    library_soup = BeautifulSoup(library_tab.text, 'lxml');
    results = library_soup.find(class_='grid versions')
    version_idx = -1
    repository_idx = -1
    usages_idx = -1
    date_idx = -1
    ths = results.thead.find_all('th')
    for i in range(0, len(ths)):
        if 'Version' == ths[i].string:
            version_idx = i
        if 'Repository' == ths[i].string:
            repository_idx = i
        if 'Usages' == ths[i].string:
            usages_idx = i
        if 'Date' == ths[i].string:
            date_idx = i
    if (version_idx == -1 or repository_idx == -1 or usages_idx == -1 or date_idx == -1):
        raise (CustomizeException("Version Repository Usages Date imcomplete"))
        # print("Version Repository Usages Date imcomplete")
        # return
    tbodys = results.find_all('tbody')
    # bi = 0
    for body in tbodys:
        # bi = bi + 1
        # if bi < 21:
        #     continue
        trs = body.find_all('tr')
        # tri = 0
        for tr in trs:
            # tri = tri + 1
            # if bi == 21 and tri < 29:
            # # if tri < 6:
            #     continue
            tds = tr.find_all('td')
            tr_version = version_idx
            tr_repository = repository_idx
            tr_usages = usages_idx
            tr_date = date_idx
            if(ths[0].string is None):
                if (tds[0].a is not None):
                    tr_version = tr_version - 1
                    tr_repository = tr_repository - 1
                    tr_usages = tr_usages - 1
                    tr_date = tr_date - 1
            version_url = category_url[0:category_url.rindex('/')] + '/' + tds[tr_version].a["href"]
            version = tds[tr_version].a.string.replace('\n', '')
            repository = "{'" + tds[tr_repository].a.string.replace('\n', '') + "':'" + "http://mvnrepository.com" + \
                             tds[tr_repository].a["href"] + "'}"
            usages = None
            if tds[tr_usages].a is None:
                usages = "{'" + tds[tr_usages].get_text().replace('\n', '') + "':''}"
                # print(usages)
            else:
                usages = "{'" + tds[tr_usages].a.string.replace('\n', '') + "':'" + category_url + tds[tr_usages].a["href"] + "'}"
            date = tds[tr_date].string.replace('\n', '')
            print('         version:', end="")
            print(version)
            print('         repository:', end="")
            print(repository)
            print('         usages:', end="")
            print(usages)
            print('         date:', end="")
            print(date)
            # time.sleep(random.randint(30, 60))
            time.sleep(random.randint(8, 10))
            library_version = requests.get(version_url, headers=headers)
            # library_version = requests.get(version_url, proxies=proxy_ip)
            page = library_version.text
            library_soup = BeautifulSoup(library_version.text, 'lxml');
            results = library_soup.find('div', class_='im')
            if results is None:
                raise (CustomizeException("can't find 'im' class"))
                # print("can't find 'im' class")
                # return
            results = results.find_next_sibling(class_='grid')
            information_trs = results.find_all('tr')
            license = None
            categories = None
            organization = None
            home_page = None
            files = None
            used_by = None
            declarations = None
            for tr in information_trs:
                if 'License' == tr.th.string:
                    license =''
                    spans = tr.td.find_all('span')
                    for span in spans:
                        license = license + span.string + ','
                    if license[len(license)-1] == ',':
                        license = license[:-1].replace('\n', '')
                if 'Categories' == tr.th.string:
                    categories = "{'" + tr.td.a.string.replace('\n', '') + "':'" + "http://mvnrepository.com" + tr.td.a["href"] + "'}"
                if 'Organization' == tr.th.string:
                    if tr.td.a is None:
                        organization = "{'" + tr.td.string.replace('\n', '') + "':''}"
                    else:
                        organization = "{'" + tr.td.a.string.replace('\n', '') + "':'" + tr.td.a["href"] + "'}"
                if 'HomePage' == tr.th.string:
                    if tr.td.a is None:
                        home_page = tr.td.string.replace('\n', '')
                    else:
                        home_page = tr.td.a["href"]
                if 'Date' == tr.th.string:
                    date = tr.td.string
                if 'Files' == tr.th.string:
                    entries = tr.td.find_all('a')
                    if entries is not None:
                        files = "{"
                        for each in entries:
                            files = files + "'" + each.get_text().replace('\n', '') + "':'" + each["href"] + "',"
                        if files[len(files) - 1] == ",":
                            files = files[:-1]
                        files = files + "}"
                if 'Repositories' == tr.th.string:
                    entries = tr.td.find_all('a')
                    if entries is not None:
                        repository = "{"
                        for each in entries:
                            repository = repository + "'" + each.string.replace('\n', '') + "':'" + "http://mvnrepository.com" + each["href"] + "',"
                        if repository[len(repository) - 1] == ",":
                            repository = repository[:-1]
                            repository = repository + "}"
                if 'Used By' == tr.th.string:
                    used_by = "{'" + tr.td.a.string.replace('\n', '') + "':'" + "http://mvnrepository.com" + tr.td.a["href"] + "'}"
            print('    license:', end="")
            print(license)
            print('    categories:', end="")
            print(categories)
            print('    organization:', end="")
            print(organization)
            print('    home_page:', end="")
            print(home_page)
            print('    date:', end="")
            print(date)
            print('    files:', end="")
            print(files)
            print('    repository:', end="")
            print(repository)
            print('    used_by:', end="")
            print(used_by)
            declarations = library_soup.find('div', id='snippets')
            if declarations is not None:
                declarations = str(declarations)
            # print('declarations:\n' + str(declarations))
            compile_dependencies_table = None
            provided_dependencies_table = None
            test_dependencies_table = None
            managed_dependencies_table = None
            licenses_table = None
            developers_table = None
            mailing_lists_table = None
            results = library_soup.find_all('div', class_='version-section')
            for entry in results:
                heading = None
                if entry.h2 is not None:
                    heading = entry.h2.string
                elif entry.h3 is not None:
                    continue
                else:
                    raise (CustomizeException("class 'version-section' can't find h2"))
                    # print("class 'version-section' can't find h2")
                    # return
                if 'Compile Dependencies' in heading:
                    compile_dependencies_table = str(entry)
                elif 'Provided Dependencies' in heading:
                    provided_dependencies_table = str(entry)
                elif 'Test Dependencies' in heading:
                    test_dependencies_table = str(entry)
                elif 'Managed Dependencies' in heading:
                    managed_dependencies_table = str(entry)
                elif 'Licenses' in heading:
                    licenses_table = str(entry)
                elif 'Developers' in heading:
                    developers_table = str(entry)
                elif 'Mailing Lists' in heading:
                    mailing_lists_table = str(entry)
                # else:
                #     print("new h2 : ", end="")
                #     print(heading)
                #     return
            declarations_soup = BeautifulSoup(str(declarations), 'lxml');
            maven = declarations_soup.find(id='maven-a').string
            # print(maven)
            declarations_soup = BeautifulSoup(maven, 'xml');
            group = declarations_soup.find('groupId').string
            name1 = declarations_soup.find('artifactId').string
            version1 = declarations_soup.find('version').string
            print(group)
            print(name1)
            print(version1)
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
                  + str(category_id).replace("'", "''") + "\',\'" \
                  + str(group).replace("'", "''") + "\',\'" \
                  + str(name1).replace("'", "''") + "\',\'" \
                  + str(version1).replace("'", "''") + "\',\'" \
                  + str(version_url).replace("'", "''") + "\',\'" \
                  + str(usages).replace("'", "''") + "\',\'" \
                  + str(license).replace("'", "''") + "\',\'" \
                  + str(categories).replace("'", "''") + "\',\'" \
                  + str(organization).replace("'", "''") + "\',\'" \
                  + str(home_page).replace("'", "''") + "\',\'" \
                  + str(date).replace("'", "''") + "\',\'" \
                  + str(files).replace("'", "''") + "\',\'" \
                  + str(repository).replace("'", "''") + "\',\'" \
                  + str(used_by).replace("'", "''") + "\',\'" \
                  + str(declarations).replace("'", "''") + "\',\'" \
                  + str(compile_dependencies_table).replace("'", "''") + "\',\'" \
                  + str(provided_dependencies_table).replace("'", "''") + "\',\'" \
                  + str(test_dependencies_table).replace("'", "''") + "\',\'" \
                  + str(managed_dependencies_table).replace("'", "''") + "\',\'" \
                  + str(licenses_table).replace("'", "''") + "\',\'" \
                  + str(developers_table).replace("'", "''") + "\',\'" \
                  + str(mailing_lists_table).replace("'", "''") + "\',\'" \
                  + str(page).replace("'", "''") + "\')"
            database.execute_sql(db, sql)
            print('======================== INSERT INTO library_versions ')
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# pool = proxy.get_proxies_from_file()
read_library_url_from_db()
# get_library_versions('http://mvnrepository.com/artifact/org.nuxeo.ecm.platform/nuxeo-platform-audit-ws','http://mvnrepository.com/artifact/org.nuxeo.ecm.platform/nuxeo-platform-audit-ws', 6812)
# /artifact/com.google.zxing/javase?repo=redhat-ga
# sql = "SELECT * FROM library_category_url_and_page WHERE id = 1"
# results = database.querydb(db, sql)
# for item in results:
#     t = item[3]
#     print(t)
# pool = proxy.get_proxies_from_file()

# for p in pool:
#     if proxy.test_useful(p):
#         with open('proxy_new.txt', 'a') as f:
#             f.write(p + '\n')
# print(pool)







