#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import string
import time
import redis
from util import *

'''
table 0: <machine+size, family>  通常情况下,machine 和size都相同的样本，
属于同一个botnet family, 这些样本都是用生成器生成的,每个样本只有CC服务
器地址不同. 通过这个特征,我们可以对样本进行快速的归类;

table 1: <family, feature>  对于同一个botnet family的样本,可能存在多个变种,
直接根据machine 和size无法准确的对这些样本进行归类,但这些样本内部有一些共
同的特征,通过这些特征我们也可以快速的判断出样本所属的botnet family
'''

class sample_info:
    '''
    r0 <1 v 1>: 采用最简单的strings类型, 一个key(machine_size)对应一个value(family)
    r1 <1 v n>: 采用list类型, 一个key(family)对应多个value(feature)
    '''
    r0 = redis.Redis(host='10.66.20.100', port=6379, db=0)
    r1 = redis.Redis(host='10.66.20.100', port=6379, db=1)
   
    def __init__(self, machine=None, size=0, feature=None, family=None):
        self.machine = machine
        self.size = size
        self.feature = feature
        self.family = family
    
    def set_family_machine_size(self, family):
        if None == family:
            return
        db = sample_info.r0
        key = self.machine + "_" + str(self.size)
        if not db.exists(key):
            db.set(key, family)
            self.family = family
    
    def set_family_feature(self, feature):
        if None == feature:
            return
        db = sample_info.r1
        if db.exists(self.family):
            for value in db.lrange(self.family, 0, db.llen(self.family)):
                if value == feature:
                    return 
        db.lpush(self.family, feature)
        self.feature = feature

    def set_sample_family(self, family, feature):
        self.set_family_machine_size(family)
        self.set_family_feature(feature)
    
    def get_family_by_machine_size(self):
        db = sample_info.r0
        key = self.machine + "_" + str(self.size)
        if db.exists(key):
            return db.get(key)
        else:
            return None

    def get_family_by_feature(self, str):
        db = sample_info.r1
        for family in db.keys():
            for s in str:
                len = db.llen(family)
                for feature in db.lrange(family, 0, len):
                    if feature.lower() in s.lower():
                        return family
        return None

    def get_sample_family(self, sample):
        self.family = self.get_family_by_machine_size()
        if None == self.family:
            str = strings(sample)
            self.family = self.get_family_by_feature(str)

def sample_store(sample, dst):
    move_file(sample, dst)   

def classfiy(dir, dst_dir):
    '''
    1. 遍历样本目录，针对每个样本进行操作;
    2. 判断文件大小是否满足要求；
    3. 根据文件平台类型、大小、特征等确定样本所属botnet家族;
    4. 存储样本;
    '''
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
                            obj = sample_info(machine, size)
                            obj.get_sample_family(sample)
                            if None == obj.family:
                                obj.set_sample_family("new_"+str(size), None)
                            dst = os.path.join(dst_dir, obj.family)
                        else:
                            dst = os.path.join(dst_dir, "NOT_ELF")
                else:
                    dst = os.path.join(dst_dir, "NOT_ELF")
                if not os.path.exists(dst):
                    os.makedirs(dst)
                sample_store(sample, os.path.join(dst, file))

classfiy(sys.argv[1], sys.argv[2])
