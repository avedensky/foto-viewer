#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import wx

#TO DO: Value need to load from INI File
supported_fromat = ['.png','.jpg','.bmp','.gif','.tif','.tiff','.PNG','.JPG','.BMP','.GIF','.TIF','.TIFF']
FILENAME_SCRIPTS_XML = 'scripts.xml'

#Window option
DEFAULT_THMB_PANEL_HEIGHT = 126

#Thumbnail panel option
DEFAULT_THMB_WIDTH              = 128
DEFAULT_THMB_HEIGHT             = 96
DEFAULT_BORDURE_LEFT_OFF_THMB   = 15
DEFAULT_BORDURE_RIGHT_OFF_THMB  = 15
DEFAULT_BORDURE_TOP_OFF_THMB    = 15
DEFAULT_BORDURE_BOTTOM_OFF_THMB = 22

#cache param
FILENAME_FILES_BD_XML = 'FilesBD.xml'
CACHE_PATH = 'cache'
CACHE_FILE_TYPE = wx.BITMAP_TYPE_JPEG #wx.BITMAP_TYPE_PNG
CACHE_FILE_EXT  = '.jpg'
CACHE_IMAGE_WIDTH = 1600 #resize to WIDTH
CACHE_IMAGE_HEIGHT = 1200 #resize to HEIGHT
MAX_FILE_SIZE_BYTES = 500000 #if img>MAX_ then save resize to cache dir

#Thread switch and indication
SW_THREAD_LOAD_IMG_FROM_DIR    = 'stop'
LED_THREAD_LOAD_IMG_FROM_DIR   = 'off'
SW_THREAD_UPDATE_IMG_FROM_LST  = 'stop'
LED_THREAD_UPDATE_IMG_FROM_LST = 'off'
LED_THREAD_MAIN_REPAINT_IMAGE  = 'off'

#Значения которые должны быть заменены на реальные
#названия файлов в коммандной строке запуска внешнего скрипта
VALUE_SCRIPT            = '%script%'
VALUE_SELECTED_FILE     = '%selected_file%'
VALUE_SELECTED_FILELIST = '%selected_filelist%'


def print_err (value):
    sys.stderr.write (value+'\n')
    sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [0])+'\n')
    sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [1])+'\n')

def print_ln (value):
    sys.stdout.write (str(value)+'\n')

def message(parent, value):
    #wx.MessageBox("You selected item '%s'" % str (value))
    dlg = wx.MessageDialog(parent, value, 'Information', wx.OK|wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()

