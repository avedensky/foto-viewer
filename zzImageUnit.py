#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import sys
import zzShare


class zzImage:         
    def __init__(self):
        '''Image Load, Resize and Save, Draw Preview, Draw Thumbnail etc...'''
        self.orig_img   = wx.EmptyImage (1,1,True) 
        self.thmb_img   = wx.EmptyImage (1,1,True)
        self.prvw_img   = wx.EmptyImage (1,1,True)        
        self.thmb_height_old = 1
        self.prvw_height_old = 1
        self.prvw_width_old  = 1        
        self.filename  = ''        

        
    def LoadFromFile (self, name):
        '''Load (orig) image from file'''
        zzShare.print_ln ('(zzImage) LoadFromFile:' + name)
        if not self.orig_img.LoadFile (name):
            sys.stderr.write ('\n Can\'t open file :'+ name+'\n')
            return        
        self.filename = name
        
        
    def SaveResizeImage (self, filename):
        '''Resize img and Save '''
        zzShare.print_ln ('(zzImage) SaveResizeImage:' + filename)
        try:            
            tmp_img = wx.EmptyImage (1,1,True)            
            tmp_rect = wx.Rect (0, 0, zzShare.CACHE_IMAGE_WIDTH, zzShare.CACHE_IMAGE_HEIGHT)            
            tmp_img = self.__GetImageInRect (self.orig_img, tmp_rect)            
            tmp_img.SaveFile (filename, zzShare.CACHE_FILE_TYPE)
        except:            
            sys.stderr.write ('* Error in zzImage.SaveResizeImage()\n')
            sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [0])+'\n')
            sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [1])+'\n')
    
        
    #Помещается ли img в координатх rect
    def __IsImgInRect (self, src_img, rect):
        '''Is image size in rect...'''
        if rect.GetWidth() >= src_img.GetWidth() and rect.GetHeight() >= src_img.GetHeight():
            return True
        return False
    
    def __GetImageInRect(self, src_img, rect):
        '''Create img with true aspect ratio in rect'''
        #Main side - width
        if rect.GetWidth()>=rect.GetHeight():
            asp_r1 = src_img.GetWidth()*1.0 / src_img.GetHeight()            
            w = rect.GetWidth()
            h = w / asp_r1
            
            if h <= rect.GetHeight(): #пропорции соблюдены и все вписывается
                return src_img.ResampleBox (long(w),long(h))                
            
            #Находим оптимальные ширину и высоту, с сохранением пропорций,
            #для вписывани в размеры rect
            while (h>rect.GetHeight()):
                w -= 1
                h = w / asp_r1
                        
            return src_img.ResampleBox (long(w),long(h))            
               
        #Main side - height
        if rect.GetWidth()<rect.GetHeight():
            asp_r1 = src_img.GetWidth() * 1.0 / src_img.GetHeight()            
            h = rect.GetHeight()
            w = h * asp_r1
            
            if w <= rect.GetWidth(): #пропорции соблюдены и все вписывается
                return src_img.ResampleBox (long(w),long(h))
                            
            #Находим оптимальные ширину и высоту, с сохранением пропорций,
            #для вписывани в размеры rect
            while (w>rect.GetWidth()):
                h -= 1
                w = h * asp_r1
                
            return src_img.ResampleBox (long(w),long(h))
        return None
    
    
    def __DoPreviewImg (self,  rect):
        '''Prepare scale preview image (self.prvw_img) for draw in rect'''
        if rect.GetHeight() <> self.prvw_height_old \
           or rect.GetWidth() <> self.prvw_width_old:
            
            if self.__IsImgInRect (self.orig_img, rect):
                self.prvw_img = self.orig_img.Copy()
                return
            else:                
                self.prvw_img = self.__GetImageInRect (self.orig_img, rect)#.Copy()
                return
        
        #prvw_img is true exist
        if self.prvw_img.GetWidth() > 1 \
           and self.prvw_img.GetHeight() > 1 \
           and self.__IsImgInRect (self.prvw_img, rect):
            
            return
            
        #Copy from original image    
        if self.__IsImgInRect (self.orig_img, rect):
            self.prvw_img = self.orig_img.Copy()
            return
        
        #Resize
        self.prvw_img = self.__GetImageInRect (self.orig_img, rect)#.Copy()

    
    def DrawPreviewImg (self, dc, rect):
        '''Draw Preview Image on dc'''
        self.__DoPreviewImg (rect)
        self.prvw_height_old = rect.GetHeight()
        self.prvw_width_old = rect.GetWidth ()
        x = long (rect.GetWidth() / 2 - self.prvw_img.GetWidth () / 2 + rect.GetLeft())
        y = long (rect.GetHeight() / 2 - self.prvw_img.GetHeight () / 2 + rect.GetTop())
        
        bmp=wx.BitmapFromImage (self.prvw_img)        
        dc.DrawBitmap(bmp,x,y,False)


    def __DoThmbImg (self, rect):
        '''Prepare scale thumbnails image (self.thmb_img) for draw in rect'''
        if rect.GetHeight() <> self.thmb_height_old:
            if self.__IsImgInRect (self.orig_img, rect):
                self.thmb_img = self.orig_img.Copy()
                return
            else:                
                self.thmb_img = self.__GetImageInRect (self.orig_img, rect)#.Copy()
                return
            
        #prvw_img is true exist
        if self.thmb_img.GetWidth() > 1 \
           and self.thmb_img.GetHeight() > 1 \
           and self.__IsImgInRect (self.thmb_img, rect):
            
            return
            
        #Copy from original image    
        if self.__IsImgInRect (self.orig_img, rect):
            self.thmb_img = self.orig_img.Copy()
            return
        
        #Resize
        self.thmb_img = self.__GetImageInRect (self.orig_img, rect)#.Copy()     

            
    def DrawThmbImg (self, dc, rect):
        '''Draw Thumbnails on dc'''
        self.__DoThmbImg (rect)
        self.thmb_height_old = rect.GetHeight()
        x = long (rect.GetWidth() / 2 - self.thmb_img.GetWidth () / 2 + rect.GetLeft())
        y = long (rect.GetHeight() / 2 - self.thmb_img.GetHeight () / 2 + rect.GetTop())
        
        bmp=wx.BitmapFromImage (self.thmb_img)        
        dc.DrawBitmap(bmp,x,y,False)        

    #def Current (self, curr):
    #    '''Set Current'''
    #    self.current = curr

    #def IsCurrent (self):       
    #    return self.current
    
    #def Selected (self, sel):
    #    '''Set Selected'''
    #    self.selected = sel

    #def IsSelected (self):       
    #    return self.selected

    #def GetFileName (self):
    #    return self.filename
    
if __name__ == '__main__':
    print "zzImageUnit: For run this module, please, use import in your application"

