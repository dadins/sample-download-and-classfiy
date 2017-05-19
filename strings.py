#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import string
import struct
import time
import redis
from util import *

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

platform    = sys.argv[1]
size        = sys.argv[2]
feature     = sys.argv[3]
family      = sys.argv[4]
sample = sample_info(platform, size, feature, family)
sample.set_sample_family(family, feature)
