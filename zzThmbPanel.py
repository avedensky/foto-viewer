#!/usr/bin/python
# -*- coding: utf-8 -*-

import zzShare
import wx
import sys
import zzImageLst
import zzThreads


class zzThmbPanel (wx.Panel):
    '''User thumbnails manage  panel'''
    def __init__(self, parent, image_lst, viewer_panel, script_list):
        wx.Panel.__init__(self, parent, wx.NewId ())
        self.img_lst   = image_lst
        self.vwr_pnl   = viewer_panel
        self.scrpt_lst = script_list

        #self.__set_properties()

        #Menu
        self.popupmenu = wx.Menu()
        self.__setPopupMenu ()

        #Bind Event
        self.Bind(wx.EVT_PAINT, self.__OnPaint)
        self.Bind(wx.EVT_SIZE, self.__OnSize)
        self.Bind(wx.EVT_KEY_DOWN, self.__OnKeyDown, self)
        self.Bind(wx.EVT_LEFT_DOWN, self.__OnMouseLeftDown, self)
        self.Bind(wx.EVT_RIGHT_DOWN, self.__OnMouseRightDown, self)


    def __setPopupMenu (self):
        '''make context menu'''
        menu_item = []
        self.scrpt_lst.GetContextMenuItem (menu_item)
        #zzShare.print_ln (menu_item)
        for text in menu_item:
            item = self.popupmenu.Append(-1, text)
            self.Bind(wx.EVT_MENU, self.__OnPopupItemSelected, item)

    #def __set_properties(self):
    #    pass


    def __OnPopupItemSelected(self, event):
        '''do it this, if user item choice in context menu (sort, script etc)'''
        item = self.popupmenu.FindItemById(event.GetId())
        script_name = item.GetText()
        self.scrpt_lst.Execute (script_name)
        self.__UpdateImg ()
        #wx.MessageBox("You selected item '%s'" % text)


    def __UpdateImg (self):
        '''Run thread for update images'''
        if zzShare.LED_THREAD_LOAD_IMG_FROM_DIR == 'off' and  zzShare.LED_THREAD_UPDATE_IMG_FROM_LST == 'off':
            zzThreads.UpdateImgFromList (self.scrpt_lst.GetCultivatedFileLst(), self, self.img_lst)


    def RepaintThmb (self):
        '''ReDraw all thumbnails if need'''
        if self.img_lst.isNeedUpdate() == True:
            self.Refresh()
            self.SetFocus ()

    def __DrawBackGround (self, dc):
        '''Draw BackGround'''
        #zzShare.print_ln ('__DrawBackGround')
        w = self.GetClientRect().GetWidth()
        h = self.GetClientRect().GetHeight()
        initialColour = wx.Colour (255,255,255)
        destColour    = wx.Colour (0,0,0)
        rect1 = wx.Rect(0, 0, w, long(h / 2) )
        dc.GradientFillLinear (rect1, initialColour, destColour, wx.SOUTH)
        rect2 = wx.Rect(0, long(h / 2), w, long(h / 2)+1)
        initialColour = wx.Colour (0,10,0)
        destColour    = wx.Colour (255,255,255)
        dc.GradientFillLinear (rect2, initialColour, destColour, wx.SOUTH)


    def __OnPaint (self,event):
        '''Draw in memory dc, after copy to panel dc'''
        zzShare.LED_THREAD_MAIN_REPAINT_IMAGE = 'on'
        try:
            w = self.GetClientRect().GetWidth()
            h = self.GetClientRect().GetHeight()
            self.img_lst.SetClientSize (w, h)

            #Draw in Memory DC
            bmp = wx.EmptyBitmap(w, h)
            m_dc = wx.MemoryDC()
            m_dc.SelectObject(bmp)

            self.__DrawBackGround (m_dc)
            if not self.img_lst.IsEmpty ():
                self.img_lst.Draw (m_dc)

            #Copy to Form
            s_dc = wx.PaintDC (self);
            s_dc.Blit(0,0, w, h, m_dc, 0, 0)

            m_dc.SelectObject(wx.NullBitmap)
            self.vwr_pnl.Refresh ()

            self.img_lst.ResetUpdate ()

            zzShare.LED_THREAD_MAIN_REPAINT_IMAGE = 'off'
            event.Skip()
        except:
            zzShare.LED_THREAD_MAIN_REPAINT_IMAGE = 'off'
            sys.stderr.write ('* Error in zzThmbPanel.__OnPaint()\n')
            sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [0])+'\n')
            sys.stderr.write ('* Err Info :'+ str(sys.exc_info () [1])+'\n')

    def __OnKeyDown (self,event):
        '''check user keypress...'''
        upd = False
        key_code = event.GetKeyCode ()
        #zzShare.print_ln (str(key_code))
        shift = event.ShiftDown ()
        #zzShare.print_ln (str (shift))
        #shift = event.ShiftDown ()
        #ctrl = event.ControlDown ()

        #if shift:
        #    self.img_lst.SelectThmbShift ()

        #if ctrl:
        #    zzShare.print_ln ('good')
        #    self.img_lst.ReverseCurrentSelect ()
        #    upd = True


        if key_code == wx.WXK_RIGHT or key_code == wx.WXK_NUMPAD_RIGHT or key_code == 68: #65 = D
            if shift:
                self.img_lst.ReverseCurrentSelect ()
            self.img_lst.UserPointerBoxRight()
        elif key_code == wx.WXK_LEFT or key_code == wx.WXK_NUMPAD_LEFT or key_code == 65: #68 = A
            if shift:
                self.img_lst.ReverseCurrentSelect ()
            self.img_lst.UserPointerBoxLeft()
        elif key_code == 49: #1
            self.img_lst.SetScore(1)
        elif key_code == 50: #2
            self.img_lst.SetScore(2)
        elif key_code == 51: #3
            self.img_lst.SetScore(3)
        elif key_code == 52: #4
            self.img_lst.SetScore(4)
        elif key_code == 53: #5
            self.img_lst.SetScore(5)
        elif key_code == 48 or key_code == 126: #0
            self.img_lst.SetScore(0)
        elif key_code ==wx.WXK_CONTROL:
            self.img_lst.ReverseCurrentSelect ()
        #elif key_code ==wx.WXK_SHIFT:
        #    self.img_lst.ReverseCurrentSelect ()

        #if shift:
        #    self.img_lst.ReverseCurrentSelect ()

        if self.img_lst.isNeedUpdate() == True:
            self.Refresh()


    def __OnMouseLeftDown (self, event):
        ''' user cursor.
            click left button mouse - make thumbnail is current '''
        x, y = event.GetPositionTuple()
        self.img_lst.UserClickToXY (x, y)
        if self.img_lst.isNeedUpdate() == True:
            self.Refresh()
        self.SetFocus ()


    def __OnMouseRightDown  (self, event):
        '''user cursor. click right button mouse - show context menu'''
        pos = event.GetPosition ()
        self.PopupMenu(self.popupmenu, pos)


    def __OnSize (self, event):
        '''if change size -> ReDraw (paint())'''
        self.Refresh()
        event.Skip()
        pass
