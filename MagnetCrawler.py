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

def search_magnet(list_code):
    socket.setdefaulttimeout(5)
    urls =[]
    for code in list_code:
        urls.append(target_url+code+'R')
        for index, url in enumerate(urls):
            res = requests.get(url, headers=config.get_header(), proxies=get_proxies(index, proxy_list)).content
            if res == None:
                res = requests.get(url, headers=config.get_header(), proxies=get_proxies(index+1, proxy_list)).content
                if res == None:
                    code_notfind.append(url)
                else:
                    prase(url,res)
            else:
                prase(url,res)

def search_magnet2(list_code):
    urls = []
    for url in code_notfind:
        url = url[:-1]
        urls.append(url)
    socket.setdefaulttimeout(5)
    for index, url in enumerate(urls):
        res = requests.get(url, headers=config.get_header(), proxies=get_proxies(index, proxy_list)).content
        if res == None:
            res = requests.get(url, headers=config.get_header(), proxies=get_proxies(index+1, proxy_list)).content
            if res == None:
                code_notfind_final.append(url)
            else:
                prase2(url,res)
        else:
            prase2(url,res)

def prase(url,res):
    soup = BeautifulSoup(res.decode('UTF-8'), 'html.parser')
    if soup.find('div', class_='data-list'):
        url1 = (soup.find('div', class_='data-list')).a['href']
        get_detail(url1)
    else:
        code_notfind.append(url)

def prase2(url,res):
    soup = BeautifulSoup(res.decode('UTF-8'), 'html.parser')
    if soup.find('div', class_='data-list'):
        url1 = (soup.find('div', class_='data-list')).a['href']
        get_detail(url1)
    else:
        code_notfind_final.append(url)


def get_detail(url):
    res = requests.get(url, headers=config.get_header(), proxies=get_proxies_random(proxy_list)).content
    if res == None:
        res = requests.get(url, headers=config.get_header(), proxies=get_proxies_random(proxy_list)).content
        if res == None:
            res = requests.get(url, headers=config.get_header(), proxies=get_proxies_random(proxy_list)).content
            if res == None:
                print('get_detail error')
            else:
                prase_detail(url, res)
        else:
            prase_detail(url, res)
    else:
        prase_detail(url, res)


def prase_detail(url,res):
    soup = BeautifulSoup(res.decode('UTF-8'), 'html.parser')
    url2 = str(soup.textarea.get_text())
    magnet = url2.replace(';', '')
    list_magnet.append(magnet)


if __name__ == '__main__':
    code_notfind = []
    code_notfind_final = []
    list_magnet = []
    proxy_list = sqlhelper.select()
    search_magnet(get_code())
    search_magnet2(code_notfind)
    print(code_notfind)
    print(code_notfind_final)
    print(list_magnet)