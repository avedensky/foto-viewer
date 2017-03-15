#!/usr/bin/python
# -*- coding: utf-8 -*-

import zlib

def calc_crc32 (filename):
    '''calculate crc32 value for file'''
    try:
        input = open(filename, 'rb')
        crc32 = 0
        while True:
            data = input.read (1024)
            if data == "":
                break
            crc32 = zlib.crc32(data, crc32)
        
        input.close()
    except:        
        sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [0])+'\n')
        sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [1])+'\n')
        return -1
    
    if crc32 < 0:
        crc32 = abs (crc32)
    
    return crc32

def calc_adler32 (filename):
    '''calculate adler32 value for file (faster than calc_crc32)'''
    try:
        input = open(filename, 'rb')
        adler32 = 0
        while True:
            data = input.read (1024)
            if data == "":
                break
            adler32 = zlib.adler32(data, adler32)
        
        input.close()
    except:        
        sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [0])+'\n')
        sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [1])+'\n')
        return -1
    
    if adler32 < 0:
        adler32 = abs (adler32)
        
    return adler32
