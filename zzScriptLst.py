import zzShare
import os
import sys
import subprocess
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import TreeBuilder
'''
для того чтобы использовать дополнительные параметры в командной строк,
например img.width, img.file_size нужно:

Получить такой параметр из img_lst
Прописать в zzShare zzShare.NEW_VALUE=%new_value%
(строчку: %new_value% юзер может напечатать в командной строке для передачи параметра скрипту из проги)
Добавить в словарь cmd_param[zzShare.NEW_VALUE] = полученный параметр из img_lst все.

cmd_param правится здесь пока...
__ExecuteScriptForFile
__ExecuteScriptForFileList
TODO для добавления дополнительных параметров нужно завести отдельную ф-ию

Как формируется командная строка для вызова скрипта:
Пользователь в командной строке записывает значения,
программа ищет соответствующие key=значение в cmd_param и value

'''
class zzScriptLst:
    ''' Load, Save, Execute Scripts, Manage script list '''
    def __init__(self, image_lst):
        self.img_lst         = image_lst
        self.file_lst   = []
        self.script_lst = []

    def GetCultivatedFileLst(self):
        return self.file_lst

    def __ClearCultivatedFileList (self):
        '''Clear all items from self.img_lst[]'''
        while len (self.file_lst) > 0:
            self.file_lst.pop()

    def __GetScriptFilePath (self, path):
        #zzShare.print_ln (os.getcwdu())
        delim = [':','\\','/','//']
        for item in delim:
            if path.find (item) != -1:
                return path

        #work_dir = os.getcwdu()+'/'+'scripts'+'/'+path
        #zzShare.print_ln (work_dir)
        return os.path.normpath(os.getcwdu()+'/'+'scripts'+'/'+path)


    def __StartCMD (self, cmd, script_opt):
        try:
            #zzShare.print_ln ('zzScriptList::__StartCMD cmd='+cmd)
            if script_opt['sctipt_exit_waiting'] == 'true':
                retcode = subprocess.Popen (cmd, shell=True).wait ()
            else:
                retcode = subprocess.Popen (cmd, shell=True)
            zzShare.print_ln ('zzScriptLst->Execute (): retcode ='+ str (retcode))
        except:
            zzShare.print_ln ('zzScriptLst->__StartCMD (): Error')

    def __AdditionalValues (self, cmd_param, filename):
        '''Find Image by original filename and get param for use in cmd (cmd_param)'''
        pass


    def __ExecuteScriptForFileList (self, script_opt):
        template_cmd = script_opt['cmd']
        cmd_param = {}

        cmd_param[zzShare.VALUE_SELECTED_FILELIST] = self.__GetScriptFilePath (script_opt['selected_filelist'])
        cmd_param[zzShare.VALUE_SCRIPT] = self.__GetScriptFilePath (script_opt['script_filename'])

        #make filelist
        text_file = open(cmd_param[zzShare.VALUE_SELECTED_FILELIST], "w")
        for filename in self.file_lst:
            text_file.write(filename+'\n')
        text_file.close()

        #replace key in cmd on real value
        for key, value in cmd_param.items():
             template_cmd = template_cmd.replace (key, value)
        self.__StartCMD (template_cmd, script_opt)



    def __ExecuteScriptForFile (self, script_opt):
        #template_cmd = script_opt['cmd']
        cmd_param = {}
        cmd_param[zzShare.VALUE_SCRIPT] = self.__GetScriptFilePath (script_opt['script_filename'])

        for filename in self.file_lst:
            cmd_param[zzShare.VALUE_SELECTED_FILE] = os.path.normpath(filename)
            self.__AdditionalValues (cmd_param, filename)
            #zzShare.print_ln ('zzScriptList::__ExecuteScriptForFile filename='+filename)
            #zzShare.print_ln ('zzScriptList::__ExecuteScriptForFile VALUE_SELECTED_FILE='+ cmd_param[zzShare.VALUE_SELECTED_FILE])
            #replace key in cmd on real value
            template_cmd = script_opt['cmd']
            for key, value in cmd_param.items():
                template_cmd = template_cmd.replace (key, value)
            self.__StartCMD (template_cmd, script_opt)


    def Execute (self, scrpt_name):
        ''' Find and execute script by name '''
        for scr_opt in self.script_lst:
            if scr_opt['name'] == scrpt_name:
                self.__ClearCultivatedFileList ()
                self.img_lst.GetFileNameSelectLst (self.file_lst)
                if len (self.file_lst) == 0: # if not selected file, get current file
                    self.file_lst.append (self.img_lst.GetFileNameCurrent())

                template_cmd = scr_opt['cmd']
                if template_cmd.find(zzShare.VALUE_SELECTED_FILELIST) != -1:
                    self.__ExecuteScriptForFileList (scr_opt)
                    break
                elif template_cmd.find(zzShare.VALUE_SELECTED_FILE) != -1:
                    self.__ExecuteScriptForFile (scr_opt)
                    break
                else:
                    break


    def Delete (self, script_name):
        ''' Delete script by name from script list and save to xml file '''
        i = 0
        for item in self.script_lst:
            if item['name'] == script_name:
                self.script_lst.pop(i)
                self.SaveXML (zzShare.FILENAME_SCRIPTS_XML)
                break
            i+=1


    def ClearAll (self):
        '''Clear all items from self.script_lst[]'''
        while len (self.script_lst) > 0:
            self.script_lst.pop()


    def GetScriptNameLst (self, name_lst):
        ''' '''
        for voc in self.script_lst:
            name_lst.append (voc['name'])


    def GetContextMenuItem (self, name_lst):
        ''' '''
        for voc in self.script_lst:
            if voc['context_menu'] == 'true':
                name_lst.append (voc['name'])


    def LoadXML (self, filename):
        '''Load and parse xml from file'''
        if os.path.exists (filename):
            self.ClearAll()
            xml_tree = ElementTree()
            xml_tree.parse(filename)
            root_section = xml_tree.getroot()
            scrpt_lst = root_section.findall ("scripts/script")
            for i in scrpt_lst:
                voc = {}
                for j in i:
                    voc [j.tag] = j.text
                self.script_lst.append (voc)


    def SaveXML (self, filename):
        '''Save xml to file'''
        tree = TreeBuilder()
        tree.start ("document",{})
        tree.start ('scripts',{})
        for voc in self.script_lst:
            tree.start ('script',{})
            for key, value in voc.items():
                tree.start (key,{})
                tree.data (str (value))
                tree.end (key)
            tree.end ('script')
        tree.end ('scripts')
        tree.end ("document")
        root = ElementTree(tree.close())
        root.write (filename)
