#-*- coding:UTF-8 -*- 
import os
import requests
import time
import re
from bs4 import BeautifulSoup
from queue import Queue
import sys
# input star_lt_500_gt_200.csv output
def extract(content):
    sub_sub_dirs = []
    sub_sub_files = []
    # todo bs -> fileList
    soup = BeautifulSoup(content, "html.parser")
    sources = soup.findAll('tr', attrs={'class': 'js-navigation-item'})
    # s_cnt = 0
    for source in sources:
        # print('cnt:'+str(s_cnt))
        # s_cnt+=1
        isBack = source.find('a', attrs={'rel': 'nofollow'})
        if isBack:
            continue
        a = source.find('svg', attrs={'class': 'octicon octicon-file-directory'})
        tag_a = source.find('a', attrs={'class': 'js-navigation-open'})
        url = None
        if tag_a!=None:
            url = 'https://github.com' + tag_a.get('href')
        else:
            tag_a = source.find('a',attrs={'data-skip-pjax':'true'})
            if tag_a != None:
                url = tag_a.get('href')

        if a is None:
            #  isFile
            if url != None:
                sub_sub_files.append(url)
        else:
            # is directory
            if url != None:
                sub_sub_dirs.append(url)

    return sub_sub_dirs, sub_sub_files


def latest_time(content):
    soup = BeautifulSoup(content, "html.parser")
    sources = soup.findAll('tr', attrs={'class': 'js-navigation-item'})
    time_agos = []
    for source in sources:
        time_ago = source.find('time-ago')
        if time_ago!=None:
            time_ago = time_ago.get('datetime')
            timeArray = time.strptime(time_ago,'%Y-%m-%dT%H:%M:%SZ')
            timeStamp = int(time.mktime(timeArray))
            time_agos.append(timeStamp)
    time_agos.sort()

    if len(time_agos) !=0:
        return time_agos[len(time_agos)-1]
    else:
        return 0


def checkFile(sub_files):
    for file1 in sub_files:
        file = file1.lower()
        if file.endswith('pom.xml'):
            return 'maven'
        if file.endswith('build.gradle'):
            return 'gradle'
        if file.endswith('androidmanifest.xml'):
            return 'android'
    return 'No'

def crawlerOneProj(url):
    queue = Queue()
    name = url.split('/')
    queue.put(url)
    first  = True
    ltime  = 0
    while queue.qsize() !=0 :
        queue_url = queue.get()
        req = requests.get(queue_url)
        req.encoding = 'utf-8'
        if first:
            ltime = latest_time(req.text)
            print('time:'+str(ltime))
            first = False
        sub_dirs, sub_files  = extract(req.text)
        flag = checkFile(sub_files)
        if flag =='maven' or flag =='gradle':
            break
        if flag =='android':
            break
        for dir in sub_dirs:
            queue.put(dir)
    return flag,ltime

def crawler(num_a,num_b):
    path = os.getcwd()
    m_list = []
    fout = open(path+'/result-'+str(num_a)+'-'+str(num_b)+'.txt','a')
    with open(path+'/star_lt_500_gt_200.csv','r',encoding='utf-8') as f:
        flag = True
        for line in f:
            if flag:
                flag = False
                continue
            data = line.split(',')
            url = data[2]
            m_list.append(url)
    cnt = 0
    index = num_a
    # max 0 2675
    for i in range(num_a,num_b):
        print("No."+str(index))
        print(m_list[i])
        flag,ltime = crawlerOneProj(m_list[i])
        if flag=='maven' or flag=='gradle':
            cnt+=1
        print('proj-type: '+flag)
        fout.write(str(index)+'\n')
        fout.write(m_list[i])
        fout.write('\n')
        fout.write(str(ltime))
        fout.write('\n')
        fout.write(flag)
        fout.write('\n')
        fout.flush()
        index+=1
        # break
    fout.close()
    print("List total len:"+str(len(m_list)))
    print("java proj Cnt:"+ str(cnt))

def run():
    num_a = sys.argv[1]
    num_b = sys.argv[2]
    crawler(int(num_a),int(num_b))

def debug():
    queue = Queue()
    url =  'https://github.com/grifotv/grifotv-portfolio'
    name = url.split('/')
    print(url)
    queue.put(url)
    first  = True
    while queue.qsize() !=0 :
        queue_url = queue.get()
        req = requests.get(queue_url)
        print(queue_url)
        req.encoding = 'utf-8'
        if first:
            ltime = latest_time(req.text)
            print('time:'+str(ltime))
            first = False
        sub_dirs, sub_files  = extract(req.text)
        flag = checkFile(sub_files)
        if flag =='maven' or flag =='gradle':
            break
        if flag =='android':
            break
        for dir in sub_dirs:
            queue.put(dir)
    print('proj-type: '+flag)

# debug()
run()
