# -*- coding=utf-8 -*-
# Copyright (C), 2013-2014, China Standard Software Co., Ltd.

'''
Created on 2013-11-21

虚拟实例的用例模块。
类说明:
    TC0902010101_AddOneVMforMe: 09-02-01-01-01-添加单台虚拟机,
        选择属主用户“我自己”,其他项设置均合法
    TC0902010102_AddOneVMforOther(BaseTestCase): 09-02-01-01-02-添加单台虚拟机，
        选择属主用户为其他用户，其他项设置均合法
方法说明:
    
'''
__all__ = []

__authors__ = [
  '"Meiying Li" <meiying.li@cs2c.com.cn>',
  '"Huicong Ding" <huicong.ding@cs2c.com.cn>',
]

__version__ = "V0.2"

# ChangeLog:
# Version    Date            Desc                                Author
# ----------------------------------------------------------------------------------------
# V0.1       11/21/2013      初始版本                            LMY
# V0.2       03/31/2014      修改为DEMO                          DHC

import time

from Base import BaseTestCase
from PageObject.LoginPage import LoginPage
from PageObject.VMPage import VMPage
from Utils.PublicMethod import printLog
                
class TC0902010102_AddOneVMforOther(BaseTestCase):
    '''
    @summary: 09-02-01-01-02-添加单台虚拟机，选择属主用户为其他用户，其他项设置均合法
    @attention: 必须继承BaseTestCase类！！！
    '''

    #===========================================================================
    #前提：
    #1.存在一个普通用户组的普通用户；
    #2.存在可用的系统映像、主机、虚拟网络等资源；
    #3.待指定属主用户的配额足够，其中用户配额指【权限控制】中【用户管理】的该用户的用户配额。
    #操作步骤：
    #1.以普通用户组普通用户登录管理平台，点击【虚拟实例】，进入虚拟实例界面，点击【添加】按钮；
    #2.选择【单台添加】，并选择属主用户；
    #3.设置合法虚拟机名、系统映像、CPU单核计算能力、CPU核数、CPU架构、内存、网络设置、访问方式、
    #    虚拟机类型、主机资源池及部署类型，点击【完成】。
    #预期结果
    #3.添加一台虚拟机成功，提示信息准确，可在虚拟机列表中查看到新增加的虚拟机。
    #===========================================================================

    def setUp(self):
        BaseTestCase.setUp(self) # 执行Base的setUp方法
        # 也可用super(TC0902010102_AddOneVMforOther, self).setUp()
        self.dictData = self.initData()
        self.login_page = LoginPage(self.driver)   
        self.vm_page = VMPage(self.driver)
        # 为了简洁此处省略创建用户，正常此处需要执行‘前提’中的操作。

    def test_AddOneVMforOther(self):
        username = self.dictData["module"]["username"]["value"]
        password = self.dictData["module"]["password"]["value"]
        OtherUser = self.dictData["case"]["OtherUser"]["value"]        
        vmName = self.dictData["case"]["vmName"]["value"]

        printLog( "[STEP 1]: Open the login page, login with user meiying in the normal group," \
            "goto VM page and click addvm button.")
               
        self.login_page.loginAs(username, password)  
        self.login_page.gotoPage("VM")   
        self.vm_page.clickVMButton("VMAdd")

        printLog("[STEP 2]: Set otherUser name, click Next btn.")
        self.vm_page.addVmNormalMessage(vmName, OtherUser, "0", "2", "", "")
        
        printLog("[STEP 3]: Set other messages.")
        self.vm_page.addVmResourceConfig()
        self.vm_page.addVmNetworkConfig()
        self.vm_page.addVmDeployConfig()
        self.vm_page.waitDataLoad()

    def tearDown(self):
        '''
        @summary: 删除虚拟机，初始化测试环境。 
        '''
        self.login_page.gotoPage("VM") 
        if not self.vm_page.clickDeleteVmByName(""):
            self.setResultFalse()
        
        self.login_page.logout()
        printLog("[END]")
        BaseTestCase.tearDown(self) # 执行Base的tearDown方法

if __name__ == "__main__":
    pass