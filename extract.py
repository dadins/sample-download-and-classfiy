#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import re
import string
import tarfile

from util import *

'''
需要改进的地方:
    1. 采用python包等解压缩文件,记录解压缩后的文件类型;
    2. 各种异常的处理;
'''

def tar_process(filename, extract_dir):
    try:
        if tarfile.is_tarfile(filename):
            t = tarfile.open(filename, 'r')
            for file in t.getnames():
                t.extract(t.getmember(file), path=extract_dir)
                tar_process(os.path.join(extract_dir, file), extract_dir)
                return 0
        else:
            return -1
    except:
        pass

def sample_extract(sample_dir):
    tar_dir = os.path.join(sample_dir, "tar")
    if not os.path.exists(tar_dir):
        os.makedirs(tar_dir)
    
    for sample in os.listdir(sample_dir):
        src_path = os.path.join(sample_dir, sample)
        dst_path = os.path.join(tar_dir, sample)
        if 0 == tar_process(src_path, sample_dir):
            move_file(src_path, dst_path)
