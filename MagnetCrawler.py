# coding:UTF-8
import re
import socket
import threading
import time
import urllib.request
import logging
from random import choice

import requests
from bs4 import BeautifulSoup
import threadpool

import config
from db.DataStore import sqlhelper





def get_code():
    f = open("E:\\Workspace\IPProxyPool\pyin.txt")
    list_code = []
    for line in f:
        line = line.rstrip( )
        line = re.sub('-', ' ', line)
        if line != ' ' and line != '':
            list_code.append(line)
    f.close()
    return list_code


def get_proxies(s, proxy_list):
    proxies = []
    for i in proxy_list:
        proxies.append("http://" + i[0] + ":" + str(i[1]))
    proxy = {"http": proxies[s % len(proxies)]}
    return proxy

def get_proxies_random(proxy_list):
    proxies = []
    for i in proxy_list:
        proxies.append("http://" + i[0] + ":" + str(i[1]))
    proxy = {"http": choice(proxies)}
    return proxy


target_url = 'https://btso.pw/search/'

def search_magnet(code):
    socket.setdefaulttimeout(3)
    url = target_url+code+'R'
    res = requests.get(url, headers=config.get_header(), proxies=get_proxies_random(proxy_list))
    if res.status_code != 200:
        res1 = requests.get(url, headers=config.get_header(), proxies=get_proxies_random(proxy_list))
        if res1.status_code != 200:
            logging.error('connect refused')
    else:
        prase(code,res.content)


def search_magnet2(code):
    socket.setdefaulttimeout(3)
    url2 = target_url + code
    res = requests.get(url2, headers=config.get_header(), proxies=get_proxies_random(proxy_list))
    if res.status_code != 200:
        res1 = requests.get(url2, headers=config.get_header(), proxies=get_proxies_random(proxy_list))
        if res1.status_code != 200:
            logging.error('connect refused')
    else:
        prase2(code,res.content)

def prase(code,res):
    soup = BeautifulSoup(res.decode('UTF-8'), 'html.parser')
    if soup.find('div', class_='data-list'):
        url1 = (soup.find('div', class_='data-list')).a['href']
        list_magnet_ch.append(get_detail(url1))
    else:
        code_notfind.append(code[:-1])

def prase2(code,res):
    soup = BeautifulSoup(res.decode('UTF-8'), 'html.parser')
    if soup.find('div', class_='data-list'):
        url1 = (soup.find('div', class_='data-list')).a['href']
        list_magnet.append(get_detail(url1))
    else:
        code_notfind_final.append(code)


def get_detail(url):
    res = requests.get(url, headers=config.get_header(), proxies=get_proxies_random(proxy_list)).content
    if res is None:
        res = requests.get(url, headers=config.get_header(), proxies=get_proxies_random(proxy_list)).content
        if res is None:
            res = requests.get(url, headers=config.get_header(), proxies=get_proxies_random(proxy_list)).content
            if res is None:
                print('get_detail error')
            else:
                return prase_detail(res)
        else:
            return prase_detail(res)
    else:
        return prase_detail(res)


def prase_detail(res):
    soup = BeautifulSoup(res.decode('UTF-8'), 'html.parser')
    url2 = str(soup.textarea.get_text())
    magnet = url2.replace(';', '')
    return magnet


if __name__ == '__main__':
    code_notfind = []
    code_notfind_final = []
    list_magnet = []
    list_magnet_ch = []
    start_time = time.time()
    proxy_list = sqlhelper.select(10)
    pool = threadpool.ThreadPool(10)
    reqs = threadpool.makeRequests(search_magnet, get_code())
    [pool.putRequest(req) for req in reqs]
    pool.wait()
    reqs2 = threadpool.makeRequests(search_magnet2, code_notfind)
    [pool.putRequest(req) for req in reqs2]
    pool.wait()

    f1 = open("E:\\Workspace\IPProxyPool\pyout.txt",'w+')
    f1.write('找到中文字幕'+'\n')
    for i in list_magnet_ch:
        f1.write(i+'\n')
    f1.write('\n' + '找到无字幕' + '\n')
    for i in list_magnet:
        f1.write(i+'\n')
    f1.write('\n' + '未找到' + '\n')
    for i in code_notfind_final:
        f1.write(i+'\n')
    f1.close()
