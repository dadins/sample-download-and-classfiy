#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import sys
import re
import string
import requests
import redis

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
            self.list.append(url.replace(' ', ':'))
        file.close()

    def sort(self):
        tmp = sorted(self.list)
        self.list = tmp

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
            #extract "host" as key 
            host_beg = url.find("http://")
            if host_beg != -1:
                host_beg += 7
                host_len = url[host_beg:].find('/')
                if host_len != -1:
                    key = url[host_beg:host_beg+host_len]
                    #extract "sample" as value
                    samp_beg = host_beg+host_len + 1
                    samp_len = url[samp_beg:].find(':')
                    if samp_len == -1:
                        samp_len = url[samp_beg:].find('\n')
                    if samp_len != -1:
                        value = url[samp_beg:samp_beg+samp_len]
                        Url.r.set(key, value)

    def url_process(self):
        self.sort()
        self.uniq()
        self.split()
