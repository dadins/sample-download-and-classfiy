#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import sys
import re
import string
import requests

'''
1. 把空格替换成":"
2. 排序
2. 去重操作(去掉包含关系的)
3. find "http:",从http之后获取<IP:port, sample_name>
'''

class Url:
    r = redis.Redis(host='10.66.20.100', port=6379, db=2)
    
    def __init__(self, filename, list=""):
        self.filename = filename
        self.list = list
        file = open(self.filename)
        for url in file:
            self.list.append(url.replace(' ', ':'))
        file.close()

    def sort(self):
        tmp = sorted(self.list)
        self.list = tmp
 
    def uniq(self):
        uniq_list = []
        tmp = ""
        for url in self.list:
            if(string.find(url, tmp) == -1):
                uniq_list.append(tmp)
            tmp = url
        self.list = uniq_list   
    
    def split(self):
        for url in self.list:
            host_beg = url.find("http:") + 5
            samp_beg = url[host_beg:].find('/')
            key = url[host_loc:samp_beg]
            samp_end = url[samp_beg:].find(':')
            if samp_end == -1:
                samp_end = url[samp_beg:].find('\n')
            value = url[samp_beg:samp_end]
            Url.r.set(key, value)

    def url_process(self):
        self.sort()
        self.uniq()
        self.split()
