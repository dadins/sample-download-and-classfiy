#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import sys
import re
import string
import requests
import redis
import time
'''
1. 把空格替换成":",方便后续处理
2. 排序
2. 去重操作(去掉包含关系的)
3. find "http:",从http之后获取<IP:port, sample_name>
'''

class Url:
    r = redis.Redis(host='10.66.20.100', port=6379, db=2)
    def __init__(self, filename, list=[]):
        self.filename = filename
        self.list = list
        file = open(self.filename)
        for url in file:
            self.list.append(url.strip('\n'))
        file.close()

    def format(self):
        '''
        0. 提取出http://相关的字符串
        1. 将' '替换成':'或'/'
        2. 截断';'后的内容
        '''
        format_list = []
        for url in self.list:
            beg = url.find("http://")
            if beg != -1:
                end = url.find("-O")
                if end != -1 and beg < end:
                    url = url[beg:end-1]
                else:
                    url = url[beg:]
            
            l = len(url)
            while url[l-1] == ' ':
                l -= 1
            url = url[:l]
            space = url.find(' ')
            #多个' '的情况下,第1个替换为':',表示端口; 其余的替换为'/',表示路径
            if (-1 != space) and (-1 != url[space+1:].find(' ')): 
                url = url.replace(' ', ':', 1)
            url = url.replace(' ', '/', 1)
            semicolon = url.find(';')
            if -1 == semicolon:
                format_list.append(url)
            else:
                format_list.append(url[:semicolon])
        self.list = format_list

    def sort(self):
        self.list = sorted(self.list)

    def uniq(self):
        uniq_list = []
        tmp = ""
        for url in self.list:
            if(url.strip('\n').find(tmp.strip('\n')) == -1):
                uniq_list.append(tmp)
            tmp = url
        if tmp != "":
            uniq_list.append(tmp)
        self.list = uniq_list
    
    def split(self):
        for url in self.list:
            #extract "host" as key,"sample" as value
            host_beg = url.find("http://")
            if host_beg != -1:
                host_beg += 7
                host_len = url[host_beg:].find('/')
                if host_len != -1:
                    host_end = host_beg+host_len
                    key = url[host_beg:host_end]
                    value = url[host_end+1:]
                    self.r.set(key, value)

    def url_process(self):
        self.format()
        self.sort()
        self.uniq()
        self.split()
