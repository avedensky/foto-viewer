#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime

def deletefile (filename):
    #print filename
    if os.path.exists (filename):
        try:
            #print filename + ' - exists'
            os.remove (filename)
            #print filename + ' - remove'
            return 0
        except:
            #print filename + ' - error'
            return -2
        #print filename + ' - not exist'
    return -1


def isFileExistWait (filename, wait):
    dt_old = datetime.datetime.now()
    while os.path.exists (filename):
        dt_new = datetime.datetime.now()
        if dt_new - dt_old > wait:
            break


if __name__=="__main__":
    #print 'Script: delete_file.py runing'

    filename = sys.argv[1]
    res = deletefile (filename)
    if res == 0:
        isFileExistWait (filename, 3)

    sys.exit (res)

