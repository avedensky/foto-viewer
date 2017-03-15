#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import sys
import os
import zzImageUnit
import zzShare
import zzImageLstXML
import crc


class zzImageLst:
    '''Image Mangement'''
    def __init__(self):
        self.thmb_width      = zzShare.DEFAULT_THMB_WIDTH
        self.thmb_height     = zzShare.DEFAULT_THMB_HEIGHT
        self.bordure_left    = zzShare.DEFAULT_BORDURE_LEFT_OFF_THMB
        self.bordure_right   = zzShare.DEFAULT_BORDURE_RIGHT_OFF_THMB
        self.bordure_top     = zzShare.DEFAULT_BORDURE_TOP_OFF_THMB
        self.bordure_bottom  = zzShare.DEFAULT_BORDURE_BOTTOM_OFF_THMB
        self.begin_index     = 0              #Thmb will start show by this index
        self.select_index    = 0              #Thmb will selected by this index
        self.client_w        = 0
        self.client_h        = 0
        self.update          = False          #Need ReDraw Thmb yes or no
        self.img_lst         = []             #List of zzImage

        self.small_font      = wx.Font (6, wx.FONTFAMILY_DEFAULT, \
                                        wx.FONTSTYLE_NORMAL, \
                                        wx.FONTWEIGHT_NORMAL)
        self.img_lst_xml     = zzImageLstXML.zzImageLstXML ()
        self.img_lst_xml.LoadXML(zzShare.FILENAME_FILES_BD_XML)
        self.shift           = False


    def ResetUpdate(self):
        '''if not need update thumbnail panel - reset'''
        self.update = False


    def isNeedUpdate(self):
        '''get current status self.update'''
        return self.update


    def __GetInfoAboutFile (self, filename, img_info):
        '''Get and Set additional information about file'''
        img_info['crc']   = crc.calc_adler32 (filename)
        img_info['size']  = os.path.getsize(filename)
        img_info['ctime'] = os.path.getatime(filename)
        img_info['mtime'] = os.path.getmtime(filename)
        img_info['orig_file_path']       = filename
        tmp1, img_info['orig_file_ext']  = os.path.splitext(filename)
        tmp2, img_info['orig_file_name'] = os.path.split(tmp1)


    def __LoadNewFile (self, filename, img_info, zzimg):
        '''write new load loaction img_info['load_from'], if file size > MAX_FILE_SIZE...
            save resized image to CACHE dir and update img_info['load_from'] in xml file'''
        if img_info['size'] < zzShare.MAX_FILE_SIZE_BYTES:
            img_info['load_from'] = filename
            return

        #Save to cache
        cache_pth = os.path.join (sys.path[0], zzShare.CACHE_PATH)
        if not os.path.exists (cache_pth):
            os.mkdir (cache_pth)

        img_info['load_from'] = os.path.join (cache_pth,'', \
                                              img_info['orig_file_name']+zzShare.CACHE_FILE_EXT)
        zzimg.SaveResizeImage (img_info['load_from'])

        #check result and save to xml
        if os.path.exists (img_info['load_from']) \
           and os.path.getsize(img_info['load_from']) > 0:
            self.img_lst_xml.UpdateFileLocation (img_info)
            self.img_lst_xml.SaveXML (zzShare.FILENAME_FILES_BD_XML)
        else:
            img_info['load_from'] = filename


    def LoadOneFile (self, filename, index=-1):
        '''Load image form file and add to self.img_lst[]'''
        #zzShare.print_ln ('zzImageLst:LoadOneFile begin')
        if not os.path.exists (filename):
            return

        img_info = {}
        zzimg = zzImageUnit.zzImage()
        self.__GetInfoAboutFile (filename, img_info)
        self.img_lst_xml.GetFileLocation (img_info)

        if os.path.exists (img_info['load_from']):
            zzimg.LoadFromFile (img_info['load_from'])
        else:
            zzimg.LoadFromFile (filename)
            self.__LoadNewFile (filename, img_info, zzimg)

        img_info['score']    = 0
        img_info['zzimage']  = zzimg
        img_info['current']  = False
        img_info['selected'] = False

        if index < 0:
            self.img_lst.append(img_info)
        if index >=0:
            self.img_lst.insert (index, img_info)

        img_lst_len = len (self.img_lst)
        if img_lst_len == 1:
            self.begin_index  = 0
            self.select_index = 0
            self.img_lst[self.begin_index + self.select_index]['current'] = True

        if img_lst_len >= self.begin_index \
           and img_lst_len <= self.begin_index+self.__GetMaxThmbShowHoriz (self.client_w):
            self.update = True


    def DrawPrev (self, dc, rect):
        '''Draw preview current image on dc'''
        if self.IsEmpty():
            return
        self.img_lst[self.begin_index+self.select_index]['zzimage'].DrawPreviewImg (dc, rect)


    def Draw (self,dc):
        '''Draw thumbnails on dc, started by self.begin_index'''
        #zzShare.print_ln ('Draw')
        #self.__DrawBackGround (dc)
        if self.IsEmpty():
            zzShare.print_ln ('(Draw): Thumbnails list empty \n')
            return
        index       = self.begin_index
        rect        = wx.Rect (self.bordure_left, self.bordure_top, self.thmb_width, self.thmb_height)
        max_thmb    = self.__GetMaxThmbShowHoriz (self.client_w)
        img_lst_len = len (self.img_lst)
        while index < (self.begin_index + max_thmb) and index < img_lst_len:
            #zzShare.print_ln ('Draw () ->file='+self.img_lst[index]['orig_file_name'])
            if self.img_lst[index]['current'] == True:
                self.__DrawUserPointerBox (dc, rect)
            self.__DrawIndication (dc, rect, index)
            self.__DrawThmbRect (dc, rect)
            self.__DrawTopText (dc, rect, index)
            self.img_lst[index]['zzimage'].DrawThmbImg (dc, rect)
            self.img_lst[index]['thmb_rect'] = wx.Rect(rect.GetLeft(), rect.GetTop(), rect.GetWidth(), rect.GetHeight())
            rect.SetLeft(rect.GetLeft() + self.thmb_width + self.bordure_left+self.bordure_right)
            index += 1


    #def __DrawBackGround (self, dc):
    #    '''Draw BackGround'''
    #    #zzShare.print_ln ('__DrawBackGround')
    #    initialColour = wx.Colour (255,255,255)
    #    destColour    = wx.Colour (0,0,0)
    #    rect1 = wx.Rect(0, 0, self.client_w, long(self.client_h / 2) )
    #    dc.GradientFillLinear (rect1, initialColour, destColour, wx.SOUTH)
    #    rect2 = wx.Rect(0, long(self.client_h / 2), self.client_w, long(self.client_h / 2)+1)
    #    initialColour = wx.Colour (0,10,0)
    #    destColour    = wx.Colour (255,255,255)
    #    dc.GradientFillLinear (rect2, initialColour, destColour, wx.SOUTH)


    def __DrawTopText (self, dc, rect, index):
        #zzShare.print_ln ('__DrawTopText')
        x = rect.GetLeft ()
        y = rect.GetTop ()
        w = rect.GetWidth ()
        h = rect.GetHeight()
        txt = self.img_lst[index]['orig_file_name']+self.img_lst[index]['orig_file_ext']
        space =12
        dc.SetFont (self.small_font)
        wt,ht = dc.GetTextExtent (txt)
        #Center
        x += w // 2 - wt // 2
        #zzShare.print_ln (str(w)+' '+str(wt)+' '+str(k))
        dc.DrawText (txt, x, y-space)


    def __DrawIndication (self, dc, rect, index):
        #zzShare.print_ln ('__DrawIndication')
        x1 = rect.GetLeft ()
        y1 = rect.GetTop ()
        x2 = rect.GetRight ()
        y2 = rect.GetBottom ()
        w = rect.GetWidth ()
        if self.img_lst[index]['selected'] == True:
            dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
            dc.SetBrush(wx.Brush(wx.Colour (0,240,0)))
        else:
            dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
            dc.SetBrush(wx.Brush(wx.Colour (255,255,255)))
        space = 5
        r_indicator_1 = 7
        x_indicator_1 = 0
        y_indicator_1 = 0
        x_indicator_1 += x1+ w // 2 - r_indicator_1 - space
        y_indicator_1 += y2 + r_indicator_1 + space
        dc.DrawCircle (x_indicator_1,y_indicator_1,r_indicator_1)

        r_indicator_2 = 7
        x_indicator_2 = 0
        y_indicator_2 = 0
        x_indicator_2 += x1+ w // 2 + r_indicator_2 + space
        y_indicator_2 += y2 + r_indicator_2 + space

        if self.img_lst[index]['score'] == 0:
            dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
            dc.SetBrush(wx.Brush(wx.Colour (255,255,255)))
        elif self.img_lst[index]['score'] == 1:
            dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
            dc.SetBrush(wx.Brush(wx.Colour (0,0,255)))
        elif self.img_lst[index]['score'] == 2:
            dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
            dc.SetBrush(wx.Brush(wx.Colour (0,255,0)))
        elif self.img_lst[index]['score'] == 3:
            dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
            dc.SetBrush(wx.Brush(wx.Colour (205,255,0)))
        elif self.img_lst[index]['score'] == 4:
            dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
            dc.SetBrush(wx.Brush(wx.Colour (255,255,0)))
        elif self.img_lst[index]['score'] == 5:
            dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
            dc.SetBrush(wx.Brush(wx.Colour (255,0,0)))
        dc.DrawCircle (x_indicator_2,y_indicator_2,r_indicator_2)

        txt = str(self.img_lst[index]['score'])
        dc.SetFont (self.small_font)
        wt,ht = dc.GetTextExtent (txt)
        dc.DrawText (txt, x_indicator_2 - wt // 2, y_indicator_2 - ht // 2)


    def __DrawThmbRect (self, dc, rect):
        '''Draw small rectangle around thumbnail'''
        #zzShare.print_ln ('__DrawThmbRect')
        x = rect.GetLeft ()
        y = rect.GetTop ()
        w = self.thmb_width
        h = rect.GetHeight()

        dc.SetPen(wx.Pen(wx.Colour(255,209,0)))
        dc.DrawLine (x-2,y-2,x+w+2,y-2)
        dc.DrawLine (x-1,y-1,x+w+1,y-1)

        dc.DrawLine (x-2,y-2,x-2,h+y+2)
        dc.DrawLine (x-1,y-1,x-1,h+y+1)

        dc.SetPen(wx.Pen(wx.Colour(255,226,95)))
        dc.DrawLine (x-2,h+y+2,x+w+2,h+y+2)
        dc.DrawLine (x-1,h+y+1,x+w+1,h+y+1)

        dc.DrawLine (x+w+2,y-2,x+w+2,h+y+2)
        dc.DrawLine (x+w+1,y-1,x+w+1,h+y+1)

        dc.SetPen(wx.Pen(wx.Colour(240,240,240)))
        dc.SetBrush(wx.Brush(wx.Colour (240,240,240)))
        dc.DrawRectangle (x,y,w,h)

    def __DrawUserPointerBox (self, dc, rect):
        '''Draw select rectangle around thumbnail'''
        #zzShare.print_ln ('start __DrawUserPointerBox')
        color = wx.Colour(255,0,0)
        size  = 3
        space = 5
        length = 15
        x1 = rect.GetLeft ()
        y1 = rect.GetTop ()
        x2 = rect.GetRight ()
        y2 = rect.GetBottom ()
        dc.SetPen(wx.Pen(color))
        for i in range (1, size):
            dc.DrawLine (x1-space,y1-space-i,x1+length-space, y1-space-i) #horizontal top left
            dc.DrawLine (x2+space,y1-space-i,x2-length+space, y1-space-i) #horizontal top right
            dc.DrawLine (x1-space,y2+space+i,x1+length-space, y2+space+i) #horizontal bottom left
            dc.DrawLine (x2+space,y2+space+i,x2-length+space, y2+space+i) #horizontal bottom right
        for i in range (1, size):
            dc.DrawLine (x1-space-i,y1-space,x1-space-i, y1+length-space) #vertical top left
            dc.DrawLine (x2+space+i,y1-space,x2+space+i, y1+length-space) #vertical top right
            dc.DrawLine (x1-space-i,y2+space,x1-space-i, y2-length+space) #vertical bottom left
            dc.DrawLine (x2+space+i,y2+space,x2+space+i, y2-length+space) #vertical bottom right
        #zzShare.print_ln ('end __DrawUserPointerBox')


    def UserPointerBoxLeft(self):
        '''Move Selector Left'''
        if self.IsEmpty ():
            return
        #sys.stderr.write ('LEFT'+'\n')
        if  self.select_index == 0:                                             #Move Slides
            if self.begin_index > 0:
                self.img_lst[self.begin_index+ self.select_index]['current'] = False
                self.begin_index -= 1
                self.img_lst[self.begin_index+ self.select_index]['current'] = True
                self.update = True
                return
            else:
                return
        if  self.select_index > 0:                                           #Move Selected Box
            self.img_lst[self.begin_index+ self.select_index]['current'] = False
            self.select_index -=1
            self.img_lst[self.begin_index+ self.select_index]['current'] = True
            self.update = True
            return


    def UserPointerBoxRight(self):
        '''Move Selector Right'''
        if self.IsEmpty ():
            return
        #sys.stderr.write ('RIGHT'+'\n')
        if self.shift == True:
            self.img_lst[self.begin_index+ self.select_index]['selected'] = True
        if  self.select_index == self.__GetMaxThmbShowHoriz (self.client_w)-1:      #Move Slides
            if self.begin_index < len (self.img_lst) - self.__GetMaxThmbShowHoriz (self.client_w):
                self.img_lst[self.begin_index+ self.select_index]['current'] = False
                self.begin_index += 1
                self.img_lst[self.begin_index + self.select_index]['current'] = True
                self.update = True
                return
            else:
                return

        if  self.select_index < self.__GetMaxThmbShowHoriz (self.client_w)-1 \
           and self.begin_index + self.select_index+1 <  len (self.img_lst):  #Move Selected Box
            self.img_lst[self.begin_index+ self.select_index]['current'] = False
            self.select_index += 1
            self.img_lst[self.begin_index+ self.select_index]['current'] = True
            self.update = True
            return


    def UserClickToXY(self, x, y):
        ''' fund thumbnail by x,y and set current '''
        i           = self.begin_index
        max_thmb    = self.__GetMaxThmbShowHoriz (self.client_w)
        img_lst_len = len (self.img_lst)
        #zzShare.print_ln (str(x)+' '+str (y))
        while i < (self.begin_index + max_thmb) and i < img_lst_len:
            if self.img_lst[i]['thmb_rect'].InsideXY (x,y):
                self.img_lst[self.begin_index + self.select_index]['current'] = False
                self.img_lst[i]['current'] = True
                self.select_index = i - self.begin_index
                self.update = True
                return
            i += 1


    def ReverseCurrentSelect(self):
        ''' '''
        index = self.begin_index + self.select_index
        if self.img_lst[index]['selected']:
            self.img_lst[index]['selected'] = False
            self.update = True
        else:
            self.img_lst[index]['selected'] = True
            self.update = True


    def SetClientSize (self,w,h):
        '''set new size of thumbnails window'''
        if self.IsEmpty():
            sys.stderr.write ('(SetClientSize): Thumbnails list empty \n')
            return
        if self.client_h <> h: #if change size...
            delta = h + 2 - (self.bordure_top + self.bordure_bottom + self.thmb_height)
            if delta <>0:
                self.thmb_width  += delta
                self.thmb_height += delta
            new_count_thmb = self.__GetMaxThmbShowHoriz (w)
            if self.select_index+1 > new_count_thmb:
                self.img_lst[self.begin_index + self.select_index]['current'] = False
                self.select_index = new_count_thmb - 1
                self.img_lst[self.begin_index + self.select_index]['current'] = True
            self.update = True
        self.client_h = h
        self.client_w = w


    def GetFileNameSelectLst (self, filename_list):
        ''' Get selected thumbnails.file_names'''
        for item in self.img_lst:
            if item['selected'] == True:
                filename_list.append (item['orig_file_path'])


    def GetFileNameCurrent (self):
        ''' Get current (user cursor) img file name  '''
        for item in self.img_lst:
            if item['current'] == True:
                return item['orig_file_path']


    def IsEmpty (self):
        '''Check is empty Image List (self.img_lst[])'''
        if len (self.img_lst) == 0:
            return True
        else:
            return False


    def GetIndexByOriginalFileName (self, filename):
        ''' return index in self.img_lst by original filename'''
        for item in self.img_lst:
            if item['orig_file_path'] == filename:
                return self.img_lst.index(item)


    def DeleteByIndex (self, indx):
        ''' Delete thumbnail from self.img_lst by index'''
        isCurr = False
        if -1<indx<len (self.img_lst):
            self.img_lst[self.begin_index + self.select_index]['current'] = False
            #if self.img_lst[indx]['current'] == True:
            #    isCurr = True

            #zzShare.print_ln ('\nindx               = '+ str (indx))
            #zzShare.print_ln (self.img_lst[indx]['orig_file_name']+self.img_lst[indx]['orig_file_ext'])
            #zzShare.print_ln ('before len         = '+ str (len (self.img_lst)))
            del self.img_lst[indx]

            #zzShare.print_ln ('after len          = '+ str (len (self.img_lst)))
            #zzShare.print_ln ('select_index       = '+ str (self.select_index))
            #zzShare.print_ln ('begin_index        = '+ str (self.begin_index))

            if self.IsEmpty ():
                return

            if len (self.img_lst) > self.__GetMaxThmbShowHoriz (self.client_w):
                if self.begin_index == indx and self.begin_index > 1:
                    #print 'good'
                    self.select_index = 0
                    self.begin_index  -= 1
                    self.img_lst[self.begin_index + self.select_index]['current'] = True
                    self.update = True
                    return
                if self.begin_index < indx < self.begin_index + self.__GetMaxThmbShowHoriz (self.client_w):
                    self.select_index = indx - self.begin_index - 1
                    if self.select_index < 0:
                        self.select_index = 0
                    self.img_lst[self.begin_index + self.select_index]['current'] = True
                    self.update = True
                    return


            self.select_index = 0
            self.begin_index  = 0
            self.img_lst[self.begin_index + self.select_index]['current'] = True
            self.update = True


    def ClearAll (self):
        '''Clear all items from self.img_lst[]'''
        while len (self.img_lst) > 0:
            self.img_lst.pop()
        self.begin_index     = 0
        self.select_index    = 0
        self.update          = True

    def SetScore (self, value):
        ''' user set thumbnail score '''
        if value >= 0 or value <= 5:
            self.img_lst[self.begin_index+ self.select_index]['score'] = value
            self.update = True


    def __GetMaxThmbShowHoriz (self, width):
        ''' count and get maximum thumbnails can draw for w (width)'''
        return long (width / (self.thmb_width + self.bordure_right+self.bordure_left))
