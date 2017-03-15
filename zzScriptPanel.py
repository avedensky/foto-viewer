#!/usr/bin/python
# -*- coding: utf-8 -*-
import zzShare
import wx
import sys
import zzThreads
import zzScriptLst
import zzImageLst



class zzScriptPanel (wx.Panel):
    '''Script Panel'''
    def __init__(self, parent, image_list, thmb_panel, script_lst):
        wx.Panel.__init__(self, parent, wx.NewId ())        
        

        #self.list_box_1_items = ['Copy', 'Move', 'Delete', 'Coments']
        self.scrpt_lst = script_lst
        self.thmb_pnl  = thmb_panel
        self.img_lst   = image_list
        #zzScriptLst.zzScriptLst ()
        

        #Script ListBox
        self.list_box_1 = wx.ListBox(self, 26, choices=[])

        self.popupmenu = wx.Menu()
        self.__setPopupMenu ()

        self.__set_properties()
        self.__do_layout()
        
        #Bind Event        
        #self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown, self.list_box_1)        
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)
        self.Bind(wx.EVT_LISTBOX, self.OnSelect, self.list_box_1)
        #self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown, self.list_box_1)
        #self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown, self)

        
    def __setPopupMenu (self):
        item_1 = self.popupmenu.Append(-1, 'execute')
        self.popupmenu.AppendSeparator()
        item_2 = self.popupmenu.Append(-1, 'add')
        item_3 = self.popupmenu.Append(-1, 'delete')
        self.Bind(wx.EVT_MENU, self.OnPopupItem_Execute, item_1)
        self.Bind(wx.EVT_MENU, self.OnPopupItem_Add, item_2)
        self.Bind(wx.EVT_MENU, self.OnPopupItem_Delete, item_3)
        
    def __set_properties(self):                
        name_lst = []
        self.scrpt_lst.GetScriptNameLst (name_lst)
        for script_name in name_lst:            
            self.list_box_1.Insert (script_name, 0)        
        
    

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL) #self.notebook_1_pane_2, "Action"
        self.SetSizer(sizer_1)
        sizer_1.Add(self.list_box_1, 1, wx.EXPAND, 0)
        pass
    

    def OnShowPopup(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)


    def OnPopupItem_Execute(self, event):
        script_name = self.list_box_1.GetString(self.list_box_1.GetSelection())
        self.scrpt_lst.Execute (script_name)
        self.__UpdateImg ()
        

    def OnPopupItem_Add(self, event): 
        zzShare.print_ln ('Add')
        self.list_box_1.Insert ('Show', 0)

        
    def OnPopupItem_Delete(self, event):
        script_name = self.list_box_1.GetString(self.list_box_1.GetSelection())
        dlg = wx.MessageDialog(self, u'Are you sure you want to delete action: "'+script_name+'" ?' , 'Question', wx.YES_NO|wx.ICON_QUESTION|wx.NO_DEFAULT)
        ans = dlg.ShowModal()        
        dlg.Destroy()
        if ans == wx.ID_YES:            
            self.list_box_1.Delete(self.list_box_1.GetSelection())
            self.scrpt_lst.Delete (script_name)
            
    def __UpdateImg (self):
        if zzShare.LED_THREAD_LOAD_IMG_FROM_DIR == 'off' and  zzShare.LED_THREAD_UPDATE_IMG_FROM_LST == 'off':
            zzThreads.UpdateImgFromList (self.scrpt_lst.GetCultivatedFileLst(), self.thmb_pnl, self.img_lst)

    def OnSelect(self, event):
        #zzShare.print_ln ('Good')
        #index = event.GetSelection()
        #str_value = self.list_box_1.GetString(index)
        pass



    #def OnKeyDown (self,event):
    #    '''check user keypress...'''
    #    zzShare.print_ln ('Good')
    #    key_code = event.GetKeyCode ()        
    #    shift = event.ShiftDown ()
    #    sys.stdout.write (key_kode)
    
    #def OnMouseRightDown  (self, event):        
    #    pos = event.GetPosition ()
    #    self.PopupMenu(self.popupmenu, pos)
        
    #def OnMouseLeftDown  (self, event):
    #    zzShare.print_ln ('Good')        
