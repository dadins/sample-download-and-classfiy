#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import sys
import string
import time

from download import *
from extract import *
from classfiy import *
from url import *

if __name__=="__main__":
    
    if len(sys.argv) != 3 or not os.path.isfile(sys.argv[1]):
        print "Usage: python classfiy.py url_file sample_dir classfiy_dir"
        sys.exit(1)
    
    #0. make dir
    sample_dir = sys.argv[2]
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)
    
    #1. process url
    url = Url(sys.argv[1])
    url.url_process()
    
    #2. download samples by the url and save them to the sample_dir
    sample_download(sample_dir)

    #3. wait until the sample download completed
    time.sleep(20)
    
    #4. extract .tar file
    sample_extract(sample_dir)

    #5. classfiy all the samples
    classfiy(sample_dir, "/media/truecrypt5/botnet/tracker/dest")
