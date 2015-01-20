# -*- coding:UTF-8 -*-

'''
Created on 2012-04-18
@summary: 
@author: fei.liu@cs2c.com.cn, huicong.ding@cs2c.com.cn
@version: v0.2
'''

#ChangeLog:
# Version    Date            Desc                    Author
#-----------------------------------------------------------
# V0.2       01/22/2014      增加获取loglevel和IP地址的方法
#                                                    DHC
#-----------------------------------------------------------
import os
from xml.dom import minidom
from Utils.xml2dict import XML2Dict

   
class xmlutil:
    def __init__(self):
        pass
    
    def load(self,xml):
        if not os.path.exists(xml):
            return
        self.xml_doc = minidom.parse(xml)
        
    def __getRootElement(self):
        return self.xml_doc.childNodes[0]

    def  __getValueByElemetn(self, e):
        return "".join(t.nodeValue for t in e.childNodes if t.nodeType == t.TEXT_NODE)
    
    def __getAttrByName(self, e, name):
        if not e.hasAttribute(name):
            return 
        return e.getAttribute(name)
              
    def getOperationNodes(self, testCaseNode):
        nodes = []
        leafs = testCaseNode["operation"]
        for leaf in leafs:
            nodes.append(dict(modulename=self.__getAttrByName(leaf, 'modulename'), classname=self.__getAttrByName(leaf, 'classname')))
        return nodes
    
    def getTestCaseNodes(self):
        nodes = []
        root = self.__getRootElement()
        leafs = root.getElementsByTagName("TestCase")
        for leaf in leafs:
            desc = self.__getValueByElemetn(leaf.getElementsByTagName("description")[0])
            operation = leaf.getElementsByTagName("operation")
            run = self.__getValueByElemetn(leaf.getElementsByTagName("run")[0])
            name = self.__getAttrByName(leaf, "name")
            id_ = self.__getAttrByName(leaf, "id")
            nodes.append({"desc":desc, "operation":operation, "run":run, "name":name, "id":id_})
        return nodes
    
    def get_module_nodes(self):
        nodes = []
        root = self.__getRootElement()
        leafs = root.getElementsByTagName("module")
        for leaf in leafs:
            name = self.__getAttrByName(leaf, "name")
            id_ = self.__getAttrByName(leaf, "id")
            desc = self.__getValueByElemetn(leaf.getElementsByTagName("description")[0])
            file_name = self.__getValueByElemetn(leaf.getElementsByTagName("filename")[0])
            run = self.__getValueByElemetn(leaf.getElementsByTagName("run")[0])
            nodes.append({'name': name, 'id': id_, 'desc': desc, 'filename': file_name, 'run': run})
            # print name, id_, desc
        return nodes
    
    def get_log_level(self):
        root = self.__getRootElement()
        leaf = self.__getValueByElemetn(root.getElementsByTagName("loglevel")[0])
        return leaf
    
    def get_frontend_ip(self):
        root = self.__getRootElement()
        leaf = self.__getValueByElemetn(root.getElementsByTagName("ip")[0])
        return leaf
            
class dataload:
    def __init__(self,dataFile):
        self.file = dataFile
        
    def load(self):
        if not os.path.exists(self.file):
            return 
        x2d = XML2Dict()
        return x2d.parse(self.file)
    
def main():
    xml = xmlutil()
    xml.load('D:\NKSCloud\WebAutomaticTest\TestRun\GlobleConf.xml')
    print xml.get_frontend_ip()
#     x2d = XML2Dict()
#     r = x2d.parse('D:\Share\JavaProject\PostTestPy\TestRun\BasicSuite.xml')
#     print r["root"]["operation"][0]["description"]["value"]
        
if __name__ == "__main__":
    main()       
