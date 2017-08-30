# coding:UTF-8
import re
import time
import urllib.request
from bs4 import BeautifulSoup

from db.DataStore import sqlhelper

a = 'https://btso.pw/search/'
list_initial = []
list_R = []
list_remain = []
list_no_ch = []
list_no_ch_initial = []
#list_not_found = []
list_magnet = []


def get_code():
    f = open("E:\\Workspace\IPProxyPool\pyin.txt")
    for line in f:
        line = line.rstrip( )
        line = re.sub('-', ' ', line)
        if line != ' ' and line != '':
            list_initial.append(line)
    f.close()


def get_magnet(list = []):
    count = 1
    for i in list:
        url = a + i
        req = urllib.request.Request(url, headers={
            'Connection': 'Keep-Alive',
            'Cache-Control': 'max-age=0',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'DNT': 1,
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
        })
        response = urllib.request.urlopen(req)
        html = response.read().decode('UTF-8')
        time.sleep(3)
        soup = BeautifulSoup(html, 'html.parser')
        if soup.find('div', class_='data-list'):
            url1 = (soup.find('div', class_='data-list')).a['href']
        else:
            list_remain.append(i)
            continue

        req1 = urllib.request.Request(url1, headers={
            'Connection': 'Keep-Alive',
            'Cache-Control': 'max-age=0',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'DNT': 1,
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
        })
        response1 = urllib.request.urlopen(req1)
        html1 = response1.read().decode('UTF-8')
        time.sleep(3)
        soup = BeautifulSoup(html1, 'html.parser')
        url2 = str(soup.textarea.get_text())
        magnet = url2.replace(';', '')
        list_magnet.append(magnet)
        print(count)
        count+=1
    return list_magnet,list_remain


def get_ch_magnet():
    for i in list_initial:
        i += 'R'
        list_R.append(i)
    ch_magnet, list_no_ch = get_magnet(list_R)
    writein(ch_magnet, '中文字幕：')
    return list_no_ch

def get_no_ch_magnet(a):
    for i in a:
        i = i[:-1]
        list_no_ch_initial.append(i)
    no_ch_magnet, list_not_found = get_magnet(list_no_ch_initial)
    writein(no_ch_magnet, '无中文字幕：')
    return list_not_found

def get_not_found_magnet(a):

    writein(a, '未找到：')


def writein(x,y):
    f1 = open("E:\\Workspace\IPProxyPool\pyout.txt",'a+')
    f1.write('\n' + y + '\n')
    for i in x:
        f1.write(i + '\n')
    f1.close()


if __name__ == '__main__':
    # proxy_list = sqlhelper.select()
    # proxies = []
    # for i in proxy_list:
    #     proxies.append("http://" + i[0] + ":" + str(i[1]))
    # print(proxies)
    get_code()
    get_not_found_magnet(get_no_ch_magnet(get_ch_magnet()))
