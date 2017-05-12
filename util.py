#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import sys
import string
import shutil
import hashlib

md5_file = "md5.txt"

'''
1. 将源文件(包含路径)移到目标文件(包含路径);
2. 如果有同名文件,则在字符串后面+1,直到无同名文件为止
'''
def move_file(src, org_dst):
    '''
    1. 获取源文件的MD5值;
    2. 判断是否存在同名文件,如果存在则对比MD5,否则跳过此步骤；
    3. 如果MD5值相同，则退出，否则迭代对比;
    '''
    num = 1
    hash_md5 = md5(src)
    dst = org_dst
    
    while os.path.exists(dst):
        if hash_md5 == md5(dst):
            os.remove(src)
            return 
        else:
            dst = org_dst + str(num)
            num += 1
    '''
    1. 存储样本文件的MD5值(后续可以考虑存储倒redis的数据库中)
    2. 将样本文件move到指定的位置
    '''
    md5_path = os.path.join(os.path.dirname(dst), md5_file)
    store_md5(dst, hash_md5, md5_path)
    shutil.move(src, dst)

def md5(filename):
    return str(hashlib.md5(open(filename, "rb").read()).hexdigest())

def store_md5(md5_file, md5_key, md5_value):
    md5_info = md5_key + "\t" + md5_value + "\n"
    open(md5_file, "a+").write(md5_info)
