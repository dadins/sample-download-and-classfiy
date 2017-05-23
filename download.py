#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import sys
import string
import requests

from url import *

def sample_download(url_obj, dst_dir):
    for host in url_obj.r.keys('*'):
        sample = url_obj.r.get(host)
        try:
            url = "http://" + host
            r = requests.get(url, timeout=5)
            if "server" in r.headers:
                server = r.headers['server']
            else:
                server = "Other"
            '''
            1. HFS server 有多个版本,每个版本下载所有文件的URL不同;
            2. 需要一个数据库来保存HFS版本和对应的下载路径;
            '''
            if "HFS" in server:
                url += "/?mode=archive\&recursive"
                filename = dst_dir + "/" + host + ".tar"
            else:
                url += "/" + sample
                filename = dst_dir + "/" + host + "-" + sample
            
            cmd = "wget -b -q -c --timeout=60 -O" + " " + filename + " " + url + " &"
            r = os.system(cmd)

        except requests.exceptions.RequestException:
            continue
