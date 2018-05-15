import random
import requests
import time

import database
import proxy
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
# proxy_ip = {
#     'http': '61.134.25.106:3128',
#     'https': '61.134.25.106:3128'
# }
proxy_ip = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}

pool = []
main_url = 'http://mvnrepository.com'
r = requests.get(main_url+"/open-source") #像目标url地址发送get请求，返回一个response对象
soup = BeautifulSoup(r.text, 'lxml');
index = 1
db = database.connectdb()

def get_category_url(soup,url):
    global index
    categories = soup.find_all('div', class_='im')
    for category in categories:
        if category.a is None:
            continue
        category_url = main_url + category.a["href"]
        sql = "INSERT INTO library_url(url) VALUES ('" + category_url + "')"
        database.execute_sql(db,sql)
        print("index:" + str(index))
        print(category_url)
        index = index + 1
    goto_next_page(soup,url)

def goto_next_page(soup,url):
    search_nav_ul = soup.find('ul', class_='search-nav')
    if search_nav_ul is None:
        return
    search_nav=search_nav_ul.find_all('li')

    for nav in search_nav:
        if nav.string == 'Next':
            if(nav.a is None):
                return
            next_url = url + nav.a["href"]
            break
    next_page = requests.get(next_url)
    next_soup = BeautifulSoup(next_page.text, 'lxml')
    get_category_url(next_soup,url)


def get_top_category_url(soup):
    # global page_index
    top_categories = soup.find_all('h4')
    for category in top_categories:
        top_url = main_url + category.a["href"]
        top_page = requests.get(top_url)
        top_soup = BeautifulSoup(top_page.text, 'lxml')
        get_category_url(top_soup,top_url)
    #     print(top_url)
    # print("page_index:" + str(page_index))
    # page_index = page_index+1
    goto_next_top_page(soup)

def goto_next_top_page(soup):
    search_nav = soup.find('ul', class_='search-nav').find_all('li')
    for nav in search_nav:
        if nav.string == 'Next':
            if(nav.a is None):
                return
            next_url = main_url + "/open-source" + nav.a["href"]
            break
    next_page = requests.get(next_url)
    next_soup = BeautifulSoup(next_page.text, 'lxml')
    get_top_category_url(next_soup)


# get_top_category_url(soup)