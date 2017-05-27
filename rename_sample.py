#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import string
import time
import redis
import struct
import sys


def rename(dir):
    for root,dirs,files in os.walk(dir):
        if 0 != len(files):
            num = 1
            for file in files:
                old_path = os.path.join(root, file)
                if windows_pe(old_path):
                    print "%s is a Windows File" % old_path

def main():
    rename(sys.argv[1])

if __name__=="__main__":
    main()
