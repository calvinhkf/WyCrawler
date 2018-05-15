import requests
import time
from threading import Thread
from queue import Queue
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
proxy = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}
_BE_PROXY_QUEUE = Queue()
# path = 'proxy_xici.txt'
# path = 'proxy_kdl_intr.txt'
path = 'proxy_kdl_inha.txt'

class Consumer_Thread(Thread):
    def run(self):
        global _BE_PROXY_QUEUE
        while not _BE_PROXY_QUEUE.empty():
            p = _BE_PROXY_QUEUE.get()
            try:
                if test_useful(p):
                    with open(path, 'a') as f:
                        f.write(p + '\n')
            except Exception as e:
                print('[HERE]', e)
                pass
            finally:
                _BE_PROXY_QUEUE.task_done()


def test_useful(proxy):
    print('[INFO] Testing proxy ', proxy, ' now...')
    try:
        proxies = {'http': proxy}
        requests.get('http://ip.cip.cc', timeout=5, proxies=proxies)
        print('[Congra] Successfully get one')
        return True
    except Exception as e:
        print(e)
        return False

def get_proxies_from_file():
    with open('proxy.txt', 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip('\n')
        return lines

def test_proxies_efficience(proxy):
    proxies = {'http': proxy}
    start = time.time()
    for i in range(3):
        r = requests.get('http://www.baidu.com', proxies=proxies)
        print(i, '  ', r.text)
    cost = time.time() - start
    print('With Proxy: cost ', cost / 3, ' seconds')

    start = time.time()
    for i in range(3):
        r = requests.get('http://ip.cip.cc')
        print(i, '  ', r.text)
    cost = time.time() - start
    print('Without Proxy: cost ', cost / 3, ' seconds')

def get_proxy(proxy_url_lst):
    p_pool = []
    each_page = None
    for each_url in proxy_url_lst:
        each_page = requests.get(each_url, headers=headers)
        proxy_soup = BeautifulSoup(each_page.text, 'lxml');

        trs = proxy_soup.select('tbody > tr')
        # trs = proxy_soup.find_all("tr", class_=["", "odd"])

        for tr in trs:
            td = tr.find_all('td')
            proxy_addr = td[0].text + ':' + td[1].text
            p_pool.append(proxy_addr)
            # print(proxy_addr)
            # q_proxy.put(proxy_addr)
    return p_pool


def main():
    # 清空已有的文件
    with open(path, 'w') as f:
        f.write(time.ctime() + '\n')
        f.write('========================\n')
    global _BE_PROXY_QUEUE
    max_thread = 100
    threads = []
    # proxy_url_list = ['http://www.xicidaili.com/nn/' + str(i) for i in range(1, 30)]
    # proxy_url_list = ['http://www.kuaidaili.com/free/intr/' + str(i) for i in range(1, 30)]
    proxy_url_list = ['http://www.kuaidaili.com/free/inha/' + str(i) for i in range(1, 30)]
    pool = get_proxy(proxy_url_list)
    # 2大页面，每个大页面3个分页
    # pool = get_proxies_from_KDL(3)
    print('uher2')
    for i in range(len(pool)):
        _BE_PROXY_QUEUE.put(pool[i])
    for i in range(max_thread):
        threads.append(Consumer_Thread())
    for i in range(max_thread):
        threads[i].start()
    # 陷入等待 线程不够 是因为线程没有死循环就退出
    _BE_PROXY_QUEUE.join()

    print('###########################################')
    print('SUCCESS!')
    print('###########################################')


if __name__ == '__main__':
    main()
