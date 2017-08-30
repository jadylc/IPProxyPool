# -*- coding: utf-8 -*-
import os
import random
import time
import requests
import urllib.request
import threading
import socket
import logging
from bs4 import BeautifulSoup


target_url = []
aim_ip = []
for i in range(1, 2):
    url = 'http://www.xicidaili.com/nn/%d' % i
    #url = 'http://www.kuaidaili.com/free/outha/%d/' % i
    target_url.append(url)

all_message = []


class ipGet(threading.Thread):
    def __init__(self, target):
        threading.Thread.__init__(self)
        self.target = target

    def Get_ip(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        html = requests.get(self.target, headers=headers)
        soup = BeautifulSoup(html.text, "html.parser")
        trs = soup.find('table', id='ip_list').find_all('tr')
        #trs = soup.find('tbody').find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            ip = tds[1].text.strip()
            opening = tds[2].text.strip()
            message = [ip, opening]
            all_message.append(message)
            #print ip, opening

    def run(self):
        self.Get_ip()


class ipCheck(threading.Thread):
    def __init__(self, ipList):
        threading.Thread.__init__(self)
        self.ipList = ipList
        self.timeout = 3
        # self.test_url = 'https://www.jd.com/'
        # self.another_url = 'https://www.baidu.com/'
        self.real_url= 'https://tellme.pw'

    def Check_ip(self):
        socket.setdefaulttimeout(3)
        for ip in self.ipList:
            try:
                proxy_host = "http://" + ip[0] + ":" + ip[1]
                proxy_temp = {"http": proxy_host}
                #t_start = time.time()
                # res = requests.get(self.test_url,headers=get_header(),proxies= proxy_temp).status_code
                # res2 = requests.get(self.another_url,headers=get_header(),proxies = proxy_temp).status_code
                res3 = requests.get(self.real_url,headers=get_header(),proxies = proxy_temp).status_code
                #t_use = time.time() - t_start
                # if res == 200 and res2 == 200:
                if res3 == 200:
                    aim_ip.append((ip[0].encode("utf-8"), ip[1].encode("utf-8")))
                else:
                    continue
            except Exception as e:
                print(e)

    def run(self):
        self.Check_ip()


class save_csv():
    def __init__(self, SaveList):
        self.savelist = SaveList

    def Save_ip(self):
        counts = 0
        BASE_DIR = os.path.dirname(__file__)
        file_path = os.path.join(BASE_DIR, 'Proxyips.txt')
        f=open(file_path, 'w+')
        for each in self.savelist:
            f.write(each.__str__())
            f.write('\n')
            counts += 1
        return counts


USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]


def get_header():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }


if __name__ == '__main__':
    GetThreading = []
    CheckThreading = []

    for i in range(len(target_url)):
        t = ipGet(target_url[i])
        GetThreading.append(t)
    for i in range(len(GetThreading)):
        GetThreading[i].start()
    for i in range(len(GetThreading)):
        GetThreading[i].join()

    print('@' * 3 + ' ' * 2 + "总共抓取了%s个代理" % len(all_message) + ' ' * 2 + '@' * 3)

    for i in range(20):
        t = ipCheck(all_message[int(((len(all_message) + 19) / 20) * i):int(((len(all_message) + 19) / 20) * (i + 1))])
        CheckThreading.append(t)
    for i in CheckThreading:
        i.start()
        print(i.is_alive())
    for i in CheckThreading:
        i.join()

    print('@' * 3 + ' ' * 2 + "总共有%s个代理通过校验" % len(aim_ip) + ' ' * 2 + '@' * 3)

    t = save_csv(aim_ip)
    counts = t.Save_ip()

    print('@' * 3 + ' ' * 2 + "总共新增%s个代理" % (len(aim_ip) - counts) + ' ' * 2 + '@' * 3)