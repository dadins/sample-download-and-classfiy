#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import sys
import string
import time

from download import *
from extract import *
from classfiy import *

if __name__=="__main__":
    
    if len(sys.argv) != 3 or not os.path.isfile(sys.argv[1]):

        print "Usage: python classfiy.py url_file sample_dir classfiy_dir"
        
        sys.exit(1)
    
    sample_dir = sys.argv[2]
    
    if not os.path.exists(sample_dir):
        
        os.makedirs(sample_dir)
    
    url_list = url_list_process(sys.argv[1])

    #download all samples to the sample_dir
    sample_download(url_list, sample_dir)
    
    #wait until the sample download completed
    time.sleep(20)
    
    #extract .tar file
    sample_extract(sample_dir)
    
    #classfiy the sample
    classfiy(sample_dir, "/media/truecrypt5/botnet/botnet-tracker/script/test")
