#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import string
import time
import redis

from sample import *
from util import *

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
                samp_obj = Sample(sample)
                machine = samp_obj.get_machine_type()
                print sample
                if machine == "windows" or machine == "data":
                    # 对于windows或data，没有做进一步分析
                    dst = os.path.join(dst_dir, machine)
                else:
                    # 对于其他平台的样本, 进一步分析样本所属botnet
                    info_obj = SampleInfo(machine, samp_obj.size)
                    info_obj.get_sample_family(sample)
                    if None == info_obj.family:
                        info_obj.set_sample_family(None, None)
                    dst = os.path.join(dst_dir, info_obj.family)
                
                if not os.path.exists(dst):
                    os.makedirs(dst)
                samp_obj.move_file(os.path.join(dst, file))

def main():
    classfiy(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
