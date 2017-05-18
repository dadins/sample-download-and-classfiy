#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import string
import time
import redis

from util import *

r0 = redis.Redis(host='10.66.20.100', port=6379, db=0)
r1 = redis.Redis(host='10.66.20.100', port=6379, db=1)

'''
family(key)         feature(value)
tfddos              DealWithDDoS 
billgates           MainBeikong    
调用该接口输入样本平台、大小、特征相关信息
'''
def add_sample_family(machine, size, feature, family):
    sample_key = machine + "_" + str(size)
    if not r0.exists(sample_key):
        r0.set(sample_key, family) 
    if not r1.exists(family):
        r1.set(family, feature)
    return

'''
family(key)         feature(value)
tfddos              DealWithDDoS 
billgates           MainBeikong
遍历整个列表,与样本作特征匹配,匹配成果返回对应的family,否则返回new
'''
def deep_sample_analysis(sample):
    print "begin deep sample analysis"
    str = strings(sample)
    for family in r1.keys():
        for s in str:
            if r1[family].lower() in s.lower():
                return family
    return "new"

'''
查找redis数据库,根据machine、size信息匹配family名称
'''
def get_sample_family(machine, size, sample):
    print "begin get sample family"
    sample_key = machine + "_" + str(size)
    print "sample_key=%s" % sample_key
    if not r0.exists(sample_key):
        family =  deep_sample_analysis(sample)
        if family == "new":
            r0.set(sample_key, "new_"+str(size))
        else:
            r0.set(sample_key, family)
    return r0.get(sample_key)


def sample_store(sample, dst):
    move_file(sample, dst)   

'''
1. 遍历样本目录，针对每个样本进行操作;
2. 判断文件大小是否满足要求；
3. 根据文件平台类型、大小、特征等确定样本所属botnet家族;
4. 存储样本;
'''
def classfiy(dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for root,dirs,files in os.walk(dir):
        if 0 != len(files):
            for file in files:
                sample = os.path.join(root, file)
                size = os.path.getsize(sample)
                if size >= 36:
                    with open(sample, 'r') as elf:
                        machine = readelf(elf)
                        if not machine == "unknown-machine":
                            print "machine is %s" % machine
                            family = get_sample_family(machine, size, sample)
                            dst = os.path.join(dst_dir, family)
                        else:
                            dst = os.path.join(dst_dir, "NOT_ELF")
                else:
                    dst = os.path.join(dst_dir, "NOT_ELF")
                if not os.path.exists(dst):
                    os.makedirs(dst)
                sample_store(sample, os.path.join(dst, file))

classfiy(sys.argv[1], sys.argv[2])
