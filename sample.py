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

def main():
    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        print "Usage: python classfiy.py url_file"
        sys.exit(1)
    
    #0. make dir
    sample_dir = "sample_" + time.strftime("%Y%m%d%H%M%S", time.localtime())
    classfiy_dir = "sample_" + time.strftime("%Y%m%d", time.localtime())
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)
    if not os.path.exists(classfiy_dir):
        os.makedirs(classfiy_dir)

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
    classfiy(sample_dir, classfiy_dir)

if __name__ == "__main__":
    main()
