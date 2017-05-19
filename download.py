#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import sys
import re
import string
import requests

'''
todo:
    1. server type;
    2. HFS服务器版本判断，根据版本找到对应的链接;
'''

def sort_process(url_file_name):
    '''
    Read the url file、split it and extract the [IP,Port,sample_name]
    Args:
        url_file_name: the name of the url file
    Returns:
        An sorted list of the urls(IP:Port/sample_name)
    '''
    url_list = []
    file = open(url_file_name)
    for line in file:
        field = re.split(r'[:&/\s]*', line)
        field_len = len(field)
        #print field
        for x in range(field_len):
            if field[x] == "http":
                pos = x + 1
                if (pos + 3) > field_len: #每个list最后一个元素是空格
                    break
                if field[pos + 1].isdigit():
                    url = field[pos] + ":" + field[pos+1] + "/" + field[pos+2]
                else:
                    url = field[pos] + "/" + field[pos+1]
                url_list.append(url)
                break
    file.close()
    return sorted(url_list)


def uniq_process(list):
    uniqed_list = []
    tmp_url = ""
    for url in list:
        if(string.find(url, tmp_url) == -1):
            uniqed_list.append(tmp_url)
        tmp_url = url
    return uniqed_list


def strings2dict_list(list):
    url_list = []
    for line in list:
        field = re.split(r'[/]', line)
        key = field[0]
        value = field[1]
        tmp_dict = {key:value}
        url_list.append(tmp_dict)
    return url_list

def url_list_process(url_file):
    sorted_list = sort_process(url_file)
    uniqed_list = uniq_process(sorted_list)
    url_list = strings2dict_list(uniqed_list)
    return url_list

def sample_download(list, dst_dir):
    url_list = []
    for item in list:
        if item not in url_list:
            url_list.append(item)
            for addr, sample in item.iteritems():
                try:
                    url = "http://" + addr
                    r = requests.get(url, timeout=5)
                    if "server" in r.headers:
                        server = r.headers['server']
                    else:
                        server = "Other"
                    
                    '''
                    1. HFS server 有多个版本,每个版本下载所有文件的URL不同;
                    2. 需要一个数据库来保存HFS版本和对应的下载路径;
                    '''
                    if(string.find(server, "HFS") != -1):
                        url = url+"/?mode=archive\&recursive"
                        filename = dst_dir+"/"+addr+".tar"
                    else:
                        url = url+"/"+sample
                        filename = dst_dir+"/"+addr+"-"+sample
                    
                    cmd = "wget -b -q -c --timeout=60 -O"+ " " + filename + " " + url + " &"
                    r = os.system(cmd)
                    
                except requests.exceptions.RequestException:
                    continue
