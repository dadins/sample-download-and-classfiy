#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import string
import struct
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
    print "begin deep analysis"
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
    if not r0.exists(sample_key):
        family =  deep_sample_analysis(sample)
        if family == "new":
            r0.set(sample_key, "new_"+str(size))
        else:
            r0.set(sample_key, family)
    return r0.get(sample_key)

'''
add_sample_family("arm",  1001465, "DealWithDDoS", "tfddos")
add_sample_family("mips", 1156461, "DealWithDDoS", "tfddos")
add_sample_family("x86",  2426964, "DealWithDDoS", "tfddos")
add_sample_family("x86", 1223123, "MainBeikong", "billgates")
add_sample_family("x86", 1135000, "MainBeikong", "billgates")
add_sample_family("x86", 1521642, "MainBeikong", "billgates")
get_sample_family("x86", sys.argv[2], sys.argv[1])
'''
platform    = sys.argv[1]
size        = sys.argv[2]
feature     = sys.argv[3]
family      = sys.argv[4]
add_sample_family(platform, size, feature, family)
