#!/usr/bin/python env
import os
import sys
import tarfile
import zipfile
import time

filename = sys.argv[1]

def zip_process(filename):
    if zipfile.is_zipfile(filename):
        z = zipfile.ZipFile(filename, 'r')
        for file in z.namelist():
            print "zip", file
    else:
        print "not a zipfile"

def tar_process(filename):
    if tarfile.is_tarfile(filename):
        t = tarfile.open(filename, 'r')
        for file in t.getnames():
            t.extract(t.getmember(file), path='tmp')
            tar_process(os.path.join("tmp", file))
            zip_process(os.path.join("tmp", file))
    else:
        print "not a tarfile"

tar_process(filename)
