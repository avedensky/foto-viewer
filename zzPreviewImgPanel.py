#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import sys
import zzImageLst


class zzPreviewImgPanel (wx.Panel):
    '''Preview Image Panel'''
    def __init__(self, parent, image_lst):
        wx.Panel.__init__(self, parent, wx.NewId ())
        self.img_lst = image_lst
        #self.__set_properties()

        #Bind Event
        self.Bind(wx.EVT_PAINT, self.__OnPaint)
        self.Bind(wx.EVT_SIZE, self.__OnSize)

    #def __set_properties(self):
    #    pass

    def __DrawBackGround (self, dc):
        '''Draw BackGround'''
        bg_colour = wx.Colour(200, 200, 205)
        dc.SetPen(wx.Pen(bg_colour))
        dc.SetBrush(wx.Brush(bg_colour))
        dc.DrawRectangleRect (self.GetClientRect())


    def __OnPaint (self,event):
        '''ReDraw Preview Image'''
        s_dc = wx.PaintDC (self)

        if self.img_lst.IsEmpty ():
            self.__DrawBackGround (s_dc)
            event.Skip()
            return

        self.img_lst.DrawPrev (s_dc, self.GetClientRect())
        event.Skip()


    def __OnSize (self,event):
        '''if change size -> ReDraw (paint())'''
        self.Refresh()
        event.Skip()
        pass
