import zzShare
import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import TreeBuilder

class zzImageLstXML:
    '''load, save, update image param'''
    def __init__(self):
        self.xml_tree = ElementTree()
        self.xml_filename = '' 

        
    def LoadXML (self, filename):
        '''Load and parse xml from file'''
        if not os.path.exists (filename):            
            xml_file = open(filename, "w")
            xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<document><files></files></document>")
            xml_file.close()
            
        if os.path.exists (filename):
            self.xml_tree.parse(filename)
            self.xml_filename = filename


    def GetFileLocation (self, img_info):
        '''Comments'''
        founded_section_file = self.__GetFileSection (img_info['crc'])    
        if founded_section_file <> None:            
            img_info['load_from'] = founded_section_file.find('load_from').text
            return
        img_info['load_from'] = ''

        
    def UpdateFileLocation (self, img_info):
        '''Comments'''
        #found section 'file' on crc and update 'load_from'
        founded_section_file = self.__GetFileSection (img_info['crc'])    
        if founded_section_file <> None:
            founded_section_file.find('load_from').text = img_info['load_from']
            return
        
        #if not found - create new section 'file'
        root_section = self.xml_tree.getroot()
        files_section = root_section.find ("files")
        new_file = TreeBuilder()
        new_file.start ('file',{})
        
        new_file.start ('crc',{})
        new_file.data (str(img_info['crc']))
        new_file.end ('crc')
        
        new_file.start ('load_from',{})
        new_file.data (img_info['load_from'])
        new_file.end ('load_from')
        
        new_file.end ('file')
        files_section.append (new_file.close())        


    def __GetFileSection (self, crc):
        '''Find file section in xml for crc '''
        root_section = self.xml_tree.getroot()
        file_lst = root_section.findall ('files/file')
        for i in file_lst:            
            crc_value = i.find('crc').text
            if str(crc_value).isdigit () and int(crc_value) == crc:
                return i
        return None

    
    def SaveXML (self, filename):
        '''Save xml to file'''
        self.xml_tree.write (filename)
