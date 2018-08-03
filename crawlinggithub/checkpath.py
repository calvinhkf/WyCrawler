#-*- coding:UTF-8 -*- 
import os
import requests
import time
import re
from bs4 import BeautifulSoup
from queue import Queue
import sys


def check():
    path = os.getcwd()
    m_list = []
    with open(path+'/star_lt_500_gt_200.csv','r',encoding='utf-8') as f:
        flag = True
        for line in f:
            if flag:
                flag = False
                continue
            data = line.split(',')
            url = data[2]
            m_list.append(url)
    exist = 0
    for i in range(0,len(m_list)):
        data = m_list[i].split('/')
        print("No."+str(i))
        print(m_list[i])
        t_path = '/home/fdse/data/prior_repository/'+data[-2]+'/'+data[-1]
        if os.path.exists(t_path):
            exist+=1
        break
    print(exist)

check()
