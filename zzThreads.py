#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import wx
import zzImageLst
import zzThmbPanel
import zzShare
import crc

from wx.lib.pubsub import Publisher
from threading import Thread


def ThreadsLoadImgWait ():
    ''' wait while Thread is stoped '''
    if zzShare.SW_THREAD_LOAD_IMG_FROM_DIR == 'start':
            zzShare.SW_THREAD_LOAD_IMG_FROM_DIR = 'stop'
            #wait when process stoped...
    while zzShare.LED_THREAD_LOAD_IMG_FROM_DIR == 'on':
        pass


def ThreadsUpdateImgWait ():
    '''  wait while Thread is stoped '''
    if zzShare.SW_THREAD_UPDATE_IMG_FROM_LST == 'start':
        zzShare.SW_THREAD_UPDATE_IMG_FROM_LST = 'stop'
        #wait when process stoped...
    while zzShare.LED_THREAD_UPDATE_IMG_FROM_LST == 'on':
        pass


class LoadImgFromDir(Thread):
    '''Thread for Loading Images'''
    def __init__(self, path, zz_image_lst):#, zz_thumbail_panel):
        Thread.__init__(self)

        self.img_lst  = zz_image_lst
        #self.thmb_pnl = zz_thumbail_panel
        self.pth      = path
        self.start()


    def run(self):
        '''Clear Image List, Check Dir and Load Images'''
        #zzShare.print_ln ('Thread - go')
        zzShare.SW_THREAD_LOAD_IMG_FROM_DIR = 'start'
        zzShare.LED_THREAD_LOAD_IMG_FROM_DIR = 'on'

        for filename in os.listdir(self.pth):
            try:
                if zzShare.SW_THREAD_LOAD_IMG_FROM_DIR == 'stop':
                    break

                name, ext = os.path.splitext(filename)
                if ext in zzShare.supported_fromat:
                    full_filename = os.path.join (self.pth,'',filename)
                    self.img_lst.LoadOneFile (full_filename)
                    wx.CallAfter(Publisher().sendMessage, "zzMESSAGE_UPDATE_THMB_WIN")

            except IOError:
                sys.stderr.write ('* Error in LoadImg_Thread.run()\n')
                sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [0])+'\n')
                sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [1])+'\n')

        zzShare.SW_THREAD_LOAD_IMG_FROM_DIR = 'stop'
        zzShare.LED_THREAD_LOAD_IMG_FROM_DIR = 'off'
        #zzShare.print_ln ('Thread - stoped (finish)')


class UpdateImgFromList(Thread):
    '''Thread for Loading Images'''
    def __init__(self, cultivated_file_lst, zz_thumbail_panel, zz_image_lst):
        Thread.__init__(self)

        self.file_lst  = cultivated_file_lst
        self.thmb_pnl  = zz_thumbail_panel
        self.img_lst   = zz_image_lst
        self.start()

    def run(self):
        '''Clear Image List, Check Dir and Load Images'''
        #zzShare.print_ln ('UpdateImgFromList: Thread - go')
        zzShare.SW_THREAD_UPDATE_IMG_FROM_LST = 'start'
        zzShare.LED_THREAD_UPDATE_IMG_FROM_LST = 'on'

        for filename in self.file_lst:
            try:
                if zzShare.SW_THREAD_UPDATE_IMG_FROM_LST == 'stop':
                    break

                indx = self.img_lst.GetIndexByOriginalFileName (filename)
                #zzShare.print_ln ('UpdateImgFromList: filename:'+filename+' index:'+str (indx))
                self.img_lst.DeleteByIndex (indx)
                self.img_lst.LoadOneFile (filename, indx)
                wx.CallAfter(Publisher().sendMessage, "zzMESSAGE_UPDATE_THMB_WIN")
                while zzShare.LED_THREAD_MAIN_REPAINT_IMAGE == 'on':
                    pass

                #zzShare.print_ln ('!!! Load good !!!')


            except IOError:
                sys.stderr.write ('* Error in LoadImg_Thread.run()\n')
                sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [0])+'\n')
                sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [1])+'\n')

        zzShare.SW_THREAD_UPDATE_IMG_FROM_LST = 'stop'
        zzShare.LED_THREAD_UPDATE_IMG_FROM_LST = 'off'
        #zzShare.print_ln ('UpdateImgFromList: Thread - stoped (finish)')
