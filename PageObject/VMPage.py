# -*- coding=utf-8 -*-
# Copyright (C), 2013, China Standard Software Co., Ltd.

"""
虚拟实例的Base模块。
类说明:
    VMPage: 虚拟实例类的超类
方法说明:
    setVMText():设置虚拟机添加对话框中所有的文本输入
    setVMSelect():设置虚拟机添加对话框中所有的下拉选择
    clickVMButton():设置虚拟机添加对话框中所有的文本输入
    clickOpenVmByName():根据虚拟机名称“开启”虚拟机
    clickShutoffVmByName():根据虚拟机名称“关闭”虚拟机
    selectVm():选中一台虚拟机
    clickDeleteVmByName():删除单台或者全部虚拟机
    addVm():添加单台虚拟机
    addMoreVm(): 批量添加虚拟机；
    addVmNormalMessage(): 添加虚拟机-基本信息；
    addVmResourceConfig():添加虚拟机-资源配置；
    addVmNetworkConfig(): 添加虚拟机-网络配置；      
    addVmDeployConfig():  添加虚拟机-部署配置 
    GetVmStatus():  根据虚拟机名称，返回虚拟机状态
    WaitCheckVmStatus(): 等待虚拟机是否到预期的vm_status状态
    clickOpenVmByName():根据虚拟机名称“开启”虚拟机
    clickShutoffVmByName():根据虚拟机名称“关闭”虚拟机
"""

__authors__ = [
  '"Meiying Li" <meiying.li@cs2c.com.cn>',
]
__version__ = "V0.1"

import time
from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from BasePage import BasePage
from Utils.PublicMethod import printLog

class VMPage(BasePage):
    
    
    vm_dict_text = {"VMName": ".//*[@id='createvm_name']",    #设置虚拟机名称
                       "VMUserName": ".//*[@id='create_vm_name']",    #设置虚拟机系统用户名
                       "VMUserPassword": ".//*[@id='createvm_passwd']",    #设置虚拟机系统用户密码
                       "CPUsingle": ".//*[@id='create_cpu']",    #虚拟机CPU单核计算能力
                       "CPUnum": ".//*[@id='create_vcpu']",    #虚拟机CPU核数
                       "VMMemory": ".//*[@id='create_memory']",    #虚拟机内存
                       "SecCpu": ".//*[@id='create_sec_cpu']",    #空闲核数
                       "SecMem": ".//*[@id='create_sec_mem']",    #空闲内存   
                       "VmNumber": ".//*[@id='banthVmNumber']",    #批量创建虚拟机的数量  
                       "OtherUser": ".//*[@id='create_user_new']",    #为他人添加虚拟机
                       
                 }
    
    vm_dict_select = {"VMImage":    ("//div[@class='main_p_4']//span[@class='combo']//span[@class='combo-arrow']",\
                                 "//div[88]//div[@class='combobox-item'][","]"),    #添加虚拟机映像
#                         "OtherUser":    (".//*[@id='myVmDiv']/span/span[1]/span/span",\
#                                 "//div[89]//div//div[","]"),    #为他人添加虚拟机
                         "CpuArch":    (".//*[@id='createvm_Second_form']/div[1]/div[3]/ul/li[1]/span[2]/span[1]/span/span",\
                                 "//div[2]/div[@class='combo-panel panel-body panel-body-noheader']/div",""),    #设置虚拟机架构
                         "DataBlock":    (".//*[@id='createvm_Second_form']/div[1]/div[5]/ul/li[1]/span[2]/span/span/span",\
                                 "//div[89]//div//div[","]"),    #为虚拟机添加磁盘
                         "Vnet":    (".//*[@id='createvm_three_div']/div[1]/div[1]/ul/li[1]/span[2]/span/span/span",\
                                 "//div[90]//div//div[","]"),    #为虚拟机添加虚拟网络
                         "AccessMode":    (".//*[@id='createvm_three_div']/div[1]/div[2]/ul/li[1]/span[2]/span/span/span",\
                                 "//div[3]//div//div",""),    #为虚拟机添加访问方式
                         "DeployType":    (".//*[@id='createvm_four_from']/div[1]/div[1]/ul/li[2]/span[2]/span[1]/span/span",\
                                 "//div[@class='panel']//div//div[@value='","']"),      #为虚拟机设置部署方式:
                                                                                        #  -RUNNING_VMS    虚拟机稀疏型
                                                                                        #  RUNNING_VMS    虚拟机密集型
                                                                                        #  FREECPU    CPU资源敏感
                                                                                        #  FREEMEMORY    内存资源敏感
                         "HostCluster":    (".//*[@id='createvm_four_from']/div[1]/div[1]/ul/li[3]/span[2]/span/span/span",\
                                 "//div[5]//div//div[","]"),    #为虚拟机设置主机资源池
                      
                         "VmCheck":    ("","(//input[@type='checkbox'])[","]")    #选择某个虚拟机
                         
                         }
    
    vm_dict_click = {"VMAdd":    ".//*[@id='btnadd2']",    #添加虚拟机按钮
                        "VMAddOne":    ".//*[@id='first_div_check_1']",    #单台添加
                        "VMAddMuti":    ".//*[@id='first_div_check_2']",    #批量添加
                        "VMAddOwn":    ".//*[@id='myVmCheckbox']",    #我自己
                        "VMAddAutodeploy":    ".//*[@id='choose_scr_1']",    #自动部署
                        "VMAddFreecpunum":    ".//*[@id='choose_scr_2']",    #空闲核数
                        "VMAddFreemem":    ".//*[@id='choose_scr_4']",    #空闲内存
                        "VMAddFirstCansel":    ".//*[@id='create_first_cancel']",    #添加虚拟机，基本信息TAB的取消
                        "VMAddFirstNext":    ".//*[@id='create_first_next']",    #添加虚拟机，基本信息TAB的下一步
                        "VMAddSecondPifx":    ".//*[@id='create_second_pifx']",    #添加虚拟机，资源配置TAB的上一步
                        "VMAddSecondCansel":    ".//*[@id='create_second_cancel']",    #添加虚拟机，资源配置TAB的取消
                        "VMAddSecondNext":    ".//*[@id='create_second_next']",    #添加虚拟机，资源配置TAB的下一步
                        "VMAddThirdPifx":    ".//*[@id='create_three_pifx']",    #添加虚拟机，网络配置TAB的上一步
                        "VMAddThirdCansel":    ".//*[@id='create_three_cancel']",    #添加虚拟机，网络配置TAB的取消
                        "VMAddThirdNext":    ".//*[@id='create_three_next']",    #添加虚拟机，网络配置TAB的下一步
                        "VMAddFourPifx":    ".//*[@id='create_four_pifx']",    #添加虚拟机，部署配置TAB的上一步
                        "VMAddFourCansel":    ".//*[@id='create_four_cancel']",    #添加虚拟机，部署配置TAB的取消
                        "VMAddFourNext":    ".//*[@id='create_four_next']",    #添加虚拟机，部署配置TAB的下一步
                        "VMAddFivePifx":    ".//*[@id='create_Five_pifx']",    #添加虚拟机，完成TAB的上一步
                        "VMAddFiveCansel":    ".//*[@id='create_Five_cancel']",    #添加虚拟机，完成TAB的取消
                        "VMAddFiveNext":    ".//*[@id='create_five_next']",    #添加虚拟机，完成TAB的下一步
                        
                        "VMDelBtn":    ".//*[@id='btncut']/span/span", #删除虚拟机                        
#                        "VMConfirm":    "html/body/div[88]/div[2]/div[4]/a[@id='undefined'][1]/span/span", #删除虚拟机，确定
                        "VMConfirm":    ".//*[@class='messager-button']/a[1]/*[@class='l-btn-left']", #删除虚拟机，确定
                        "VMCancle":    ".//*[@class='messager-button']/a[2]/*[@class='l-btn-left']", #删除虚拟机，取消
    
                        "VMOpenBtn":    ".//*[@id='btnopen']/span/span", #开启虚拟机
                        "VMShutoffBtn":    ".//*[@id='shutoffVm']/span/span" #关闭虚拟机
                        }
    
    
    ID_VM_MAINCONTENT = "vm_maincontent"                  #"虚拟实例"当前位置
    XPATH_VM_CURRENTPATH = ".//*[@id='outside']/div[4]/div[2]/div[1]/h2"  #"虚拟实例"当前位置
    
        
    #删除虚拟机
    ID_VM_DEL_BUTTON = "btncut"                          #"删除"虚拟机按钮
    XPATH_VM_DEL_FIRST = "(//input[@type='checkbox'])[13]"  #删除第一个虚拟机
    
    #刷新
    ID_VM_FRESH = "fresh"                           #“刷新”按钮
    
    
    
    
    def __init__(self, driver):
        '''
        @summary: 初始化
        '''
        self.driver = driver
    
    def setVMText(self,vm_control,vm_text):
        '''
        @summary: 设置虚拟机添加对话框中所有的文本输入
        @return: 成功返回True，失败返回False
        @param: 参数使用vm_dict_text字典定义的值:
            VMName            设置虚拟机名称
            VMUserName        设置虚拟机系统用户名
            VMUserPassword    设置虚拟机系统用户密码       
            CPUsingle         虚拟机CPU单核计算能力
            CPUnum            虚拟机CPU核数
            VMMemory          虚拟机内存
        '''
        #输入创建虚拟机需要的参数
        if vm_control in self.vm_dict_text:
            try:
                input_textbox = WebDriverWait(self.driver, 10).\
                        until(lambda driver: driver.find_element_by_xpath(self.vm_dict_text[vm_control]))
            except (StaleElementReferenceException, NoSuchElementException, TimeoutException), e:
                printLog(vm_control + "VM_CONTROL doesn't work, \n" + str(e), "Error")
            else:
                if input_textbox != None:
                    input_textbox.clear()
                    input_textbox.send_keys(vm_text)
                    printLog("Input messages：" + vm_text)
        
    def setVMSelect(self,vm_control,vm_select):
        '''
        @summary: 设置虚拟机添加对话框中所有的下拉选择
        @return: 成功返回True，失败返回False
        @param: 参数使用vm_dict_select字典定义的值:
            VMImage            虚拟机映像选择
        '''
        
        try:
            #单击下拉按钮
            printLog("Click the drop-down button.")
            dropdown_button = self.driver.find_element_by_xpath(self.vm_dict_select[vm_control][0])
            dropdown_button.click()
            time.sleep(1)
            printLog("Matching the drop-down list.")
            xpath_sel_item = self.vm_dict_select[vm_control][1] + vm_select + self.vm_dict_select[vm_control][2]
            select_item = self.driver.find_element_by_xpath(xpath_sel_item)
            select_item_text = select_item.text
#            select_item = (select_item_text,)
        except NoSuchElementException:
            printLog("FAILED: Matching the drop-down list", "Error")
            return False
        else:
            if select_item != None:
                printLog("Select one item'" + vm_control + "'。")
                select_item.click()
                return select_item_text
            else:
                return None
            
    def clickVMButton(self,vm_control):
        '''
        @summary: 设置虚拟机添加对话框中所有的文本输入
        @return: 成功返回True，失败返回False        
        @param: 参数使用vm_dict_click字典定义的值:
            VMAdd             添加虚拟机按钮
            VMAddOne          单台添加
            VMAddMuti         批量添加
            VMAddOwn          批量添加
            VMAddAutodeploy   自动部署
            VMAddFreecpunum   空闲核数
            VMAddFreemem      空闲内存
        '''
        #输入创建虚拟机需要的参数
        if vm_control in self.vm_dict_click:
            try:
                click_btn = WebDriverWait(self.driver, 10).\
                        until(lambda driver: driver.find_element_by_xpath(self.vm_dict_click[vm_control]))
            except (StaleElementReferenceException, NoSuchElementException, TimeoutException), e:
                printLog(vm_control + "VM_CONTROL doesn't work, \n" + str(e), "Error")
                return False
            else:
                if click_btn != None:
                    time.sleep(1)
                    click_btn.click()
                    printLog(vm_control+"button has been clicked！")
                    return True
         
    def addVm(self, vm_name):    
        '''
        @summary: 添加虚拟机；
        @param : 无
        @return: True/False
        
        @param: 参数使用vm_dict_text字典定义的值:
            VMName            设置虚拟机名称
            VMUserName        设置虚拟机系统用户名
            VMUserPassword    设置虚拟机系统用户密码       
            CPUsingle         虚拟机CPU单核计算能力
            CPUnum            虚拟机CPU核数
            VMMemory          虚拟机内存
            VmNumber          设置虚拟机的数量
            
        @param: 参数使用vm_dict_select字典定义的值:
            VMImage           添加虚拟机映像
            OtherUser         为他人添加虚拟机
            CpuArch           设置虚拟机架构
            DataBlock         为虚拟机添加磁盘
            Vnet              为虚拟机添加虚拟网络
            AccessMode        为虚拟机添加访问方式
            DeployType        为虚拟机设置部署方式: #  -RUNNING_VMS    虚拟机稀疏型
                                                   #  RUNNING_VMS    虚拟机密集型
                                                   #  FREECPU    CPU资源敏感
                                                   #  FREEMEMORY    内存资源敏感 
            HostCluster       为虚拟机设置主机资源池
            
        @param: 参数使用vm_dict_click字典定义的值:     
            VMAdd             添加虚拟机按钮
            VMAddOne          单台添加
            VMAddMuti         批量添加
            VMAddOwn          我自己
            VMAddAutodeploy   自动部署
            VMAddFreecpunum   空闲核数
            VMAddFreemem      空闲内存
            VMAddFirstCansel  添加虚拟机，基本信息TAB的取消
            VMAddFirstNext    添加虚拟机，基本信息TAB的下一步
            VMAddSecondPifx   添加虚拟机，资源配置TAB的上一步
            VMAddSecondCansel 添加虚拟机，资源配置TAB的取消
            VMAddSecondNext   添加虚拟机，资源配置TAB的下一步
            VMAddThirdPifx    添加虚拟机，网络配置TAB的上一步
            VMAddThirdCansel  添加虚拟机，网络配置TAB的取消
            VMAddThirdNext    添加虚拟机，网络配置TAB的下一步
            VMAddFourPifx     添加虚拟机，部署配置TAB的上一步
            VMAddFourCansel   添加虚拟机，部署配置TAB的取消
            VMAddFourNext     添加虚拟机，部署配置TAB的下一步
            VMAddFivePifx     添加虚拟机，完成TAB的上一步
            VMAddFiveCansel   添加虚拟机，完成TAB的取消
            VMAddFiveNext     添加虚拟机，完成TAB的下一步
        '''
        #单击添加虚拟机按钮
#        self.clickAddVmButton()
        self.clickVMButton("VMAdd")
#        self.clickAddCancelButton()  

        #添加虚拟机-基本信息
#        self.cancleAddVmOwn()
##        self.setAddVmOther("1")
#        self.setVMSelect("OtherUser", "3")
#        self.clickVMButton("VMAddMuti")
#        self.clickVMButton("VMAddOne")
#        self.clickVMButton("VMAddMuti")
#        self.setVMText("VmNumber", "2")
#        self.clickVMButton("VMAddOwn")
#        self.setVMSelect("OtherUser", "2")
        time.sleep(3)
        self.setVMText("VMName",vm_name)        
        self.setVMSelect("VMImage","2")
#        self.setVMText("VMUserName","tester")    #设置虚拟机系统用户名
#        self.setVMText("VMUserPassword","Qwer1234")    #设置虚拟机系统用户密码
        self.clickVMButton("VMAddFirstNext")
        
        #添加虚拟机-资源配置
#        self.setVMText("CPUsingle","50")    #设置虚拟机CPU单核计算能力
#        self.setVMText("CPUnum","1")    #设置虚拟机CPU核数
#        self.setVMSelect("CpuArch", "")    #设置虚拟机CPU架构
#        self.setVMText("VMMemory","512")    #设置虚拟机内存
#        self.setVMSelect("DataBlock", "2")
        self.clickVMButton("VMAddSecondNext")
        
        #添加虚拟机-网络配置
#        self.setVMSelect("Vnet", "2")    #设置虚拟机的虚拟网络
#        self.setVMSelect("AccessMode", "")    #设置虚拟机的访问方式
#        time.sleep(2)
        self.clickVMButton("VMAddThirdNext")
        
        #添加虚拟机-部署配置
#        self.setVMSelect("DeployType", "RUNNING_VMS")    
        self.setVMSelect("HostCluster", "2")    #为虚拟机设置部署方式
#        self.clickVMButton("VMAddAutodeploy")
#        time.sleep(2)
#        self.clickVMButton("VMAddFreecpunum")
#        self.setVMText("SecCpu", "5")
#        time.sleep(2)
#        self.clickVMButton("VMAddFreemem")
#        self.setVMText("SecMem", "1024")
#        time.sleep(5)
        self.clickVMButton("VMAddFourNext")
        
        #添加虚拟机-完成
        time.sleep(2)
        self.clickVMButton("VMAddFiveNext") #完成

    def addMoreVm(self, vm_name, vm_num):    
        '''
        @summary: 添加虚拟机；
        @param : 无
        @return: True/False
        
        @param: 参数使用vm_dict_text字典定义的值:
            VMName            设置虚拟机名称
            VMUserName        设置虚拟机系统用户名
            VMUserPassword    设置虚拟机系统用户密码       
            CPUsingle         虚拟机CPU单核计算能力
            CPUnum            虚拟机CPU核数
            VMMemory          虚拟机内存
            VmNumber          设置虚拟机的数量
            
        @param: 参数使用vm_dict_select字典定义的值:
            VMImage           添加虚拟机映像
            OtherUser         为他人添加虚拟机
            CpuArch           设置虚拟机架构
            DataBlock         为虚拟机添加磁盘
            Vnet              为虚拟机添加虚拟网络
            AccessMode        为虚拟机添加访问方式
            DeployType        为虚拟机设置部署方式: #  -RUNNING_VMS    虚拟机稀疏型
                                                   #  RUNNING_VMS    虚拟机密集型
                                                   #  FREECPU    CPU资源敏感
                                                   #  FREEMEMORY    内存资源敏感 
            HostCluster       为虚拟机设置主机资源池
            
        @param: 参数使用vm_dict_click字典定义的值:     
            VMAdd             添加虚拟机按钮
            VMAddOne          单台添加
            VMAddMuti         批量添加
            VMAddOwn          我自己
            VMAddAutodeploy   自动部署
            VMAddFreecpunum   空闲核数
            VMAddFreemem      空闲内存
            VMAddFirstCansel  添加虚拟机，基本信息TAB的取消
            VMAddFirstNext    添加虚拟机，基本信息TAB的下一步
            VMAddSecondPifx   添加虚拟机，资源配置TAB的上一步
            VMAddSecondCansel 添加虚拟机，资源配置TAB的取消
            VMAddSecondNext   添加虚拟机，资源配置TAB的下一步
            VMAddThirdPifx    添加虚拟机，网络配置TAB的上一步
            VMAddThirdCansel  添加虚拟机，网络配置TAB的取消
            VMAddThirdNext    添加虚拟机，网络配置TAB的下一步
            VMAddFourPifx     添加虚拟机，部署配置TAB的上一步
            VMAddFourCansel   添加虚拟机，部署配置TAB的取消
            VMAddFourNext     添加虚拟机，部署配置TAB的下一步
            VMAddFivePifx     添加虚拟机，完成TAB的上一步
            VMAddFiveCansel   添加虚拟机，完成TAB的取消
            VMAddFiveNext     添加虚拟机，完成TAB的下一步
        '''
        #单击添加虚拟机按钮
#        self.clickAddVmButton()
        self.clickVMButton("VMAdd")
#        self.clickAddCancelButton()  

        #添加虚拟机-基本信息
#        self.cancleAddVmOwn()
        self.clickVMButton("VMAddMuti")
        self.setVMText("VmNumber", vm_num)
#        self.clickVMButton("VMAddOwn")
#        self.setVMSelect("OtherUser", "2")
        time.sleep(3)
        self.setVMText("VMName",vm_name)        
        self.setVMSelect("VMImage","2")
#        self.setVMText("VMUserName","tester")    #设置虚拟机系统用户名
#        self.setVMText("VMUserPassword","Qwer1234")    #设置虚拟机系统用户密码
        self.clickVMButton("VMAddFirstNext")
        
        #添加虚拟机-资源配置
        self.setVMText("CPUsingle","50")    #设置虚拟机CPU单核计算能力
        self.setVMText("CPUnum","1")    #设置虚拟机CPU核数
#        self.setVMSelect("CpuArch", "")    #设置虚拟机CPU架构
        self.setVMText("VMMemory","512")    #设置虚拟机内存
        self.clickVMButton("VMAddSecondNext")
        
        #添加虚拟机-网络配置
        time.sleep(1)
        self.clickVMButton("VMAddThirdNext")
        
        #添加虚拟机-部署配置
#        self.setVMSelect("DeployType", "RUNNING_VMS")    
        self.setVMSelect("HostCluster", "2")    #为虚拟机设置部署方式
#        self.clickVMButton("VMAddAutodeploy")
#        time.sleep(2)
#        self.clickVMButton("VMAddFreecpunum")
#        self.setVMText("SecCpu", "5")
#        time.sleep(2)
#        self.clickVMButton("VMAddFreemem")
#        self.setVMText("SecMem", "1024")
#        time.sleep(5)
        self.clickVMButton("VMAddFourNext")
        
        #添加虚拟机-完成
        time.sleep(2)
        self.clickVMButton("VMAddFiveNext") #完成

    def addVmNormalMessage(self, vm_name="meiying_vm", other_user="meiying", vm_number="0", vm_image="2", vm_username="cs2c", vm_passwd="Qwer1234"):    
        '''
        @summary: 添加虚拟机-基本信息；
        @param : 无
        @return: True/False
        
        @param: 参数使用vm_dict_text字典定义的值:
            VMName            设置虚拟机名称
            VMUserName        设置虚拟机系统用户名
            VMUserPassword    设置虚拟机系统用户密码       
            VmNumber          设置虚拟机的数量
            OtherUser         为他人添加虚拟机
            
        @param: 参数使用vm_dict_select字典定义的值:
            VMImage           添加虚拟机映像            
                        
        @param: 参数使用vm_dict_click字典定义的值:     
            VMAdd             添加虚拟机按钮
            VMAddOne          单台添加
            VMAddMuti         批量添加
            VMAddOwn          我自己
            VMAddFirstCansel  添加虚拟机，基本信息TAB的取消
            VMAddFirstNext    添加虚拟机，基本信息TAB的下一步
        '''
        #单击添加虚拟机按钮
#        self.clickVMButton("VMAdd")  
        
        #添加虚拟机-基本信息
        if int(vm_number) > 0:
            self.clickVMButton("VMAddMuti")
            self.setVMText("VmNumber", vm_number)                     
        else:
            self.clickVMButton("VMAddOne")
        
        if other_user != "":
            self.clickVMButton("VMAddOwn")
            self.setVMText("OtherUser", other_user)                  
                
        self.setVMText("VMName",vm_name)        
        self.setVMSelect("VMImage",vm_image)
        self.setVMText("VMUserName",vm_username)    #设置虚拟机系统用户名
        self.setVMText("VMUserPassword",vm_passwd)    #设置虚拟机系统用户密码
        self.clickVMButton("VMAddFirstNext")
        return True
    
    def addVmResourceConfig(self, cpu_single="50", cpu_num="1", cpu_arch="2",vm_mem="512", data_block=""):    
        '''
        @summary: 添加虚拟机-资源配置；
        @param : 无
        @return: True/False
        
        @param: 参数使用vm_dict_text字典定义的值:   
            CPUsingle         虚拟机CPU单核计算能力
            CPUnum            虚拟机CPU核数
            VMMemory          虚拟机内存
            
        @param: 参数使用vm_dict_select字典定义的值:
            CpuArch           设置虚拟机架构
            DataBlock         为虚拟机添加磁盘
                       
        @param: 参数使用vm_dict_click字典定义的值:     
            VMAddSecondPifx   添加虚拟机，资源配置TAB的上一步
            VMAddSecondCansel 添加虚拟机，资源配置TAB的取消
            VMAddSecondNext   添加虚拟机，资源配置TAB的下一步
         '''
                
        #添加虚拟机-资源配置
        self.setVMText("CPUsingle",cpu_single)    #设置虚拟机CPU单核计算能力
        self.setVMText("CPUnum",cpu_num)    #设置虚拟机CPU核数
#        self.setVMSelect("CpuArch",cpu_arch)    #设置虚拟机CPU架构
        self.setVMText("VMMemory",vm_mem)    #设置虚拟机内存
        if data_block != "":          
            self.setVMSelect("DataBlock", data_block)
            
        self.clickVMButton("VMAddSecondNext")
        return True

    def addVmNetworkConfig(self, vnet="", access_mode=""):    
        '''
        @summary: 添加虚拟机-网络配置；
        @param : 无
        @return: True/False
            
        @param: 参数使用vm_dict_select字典定义的值:
            Vnet              为虚拟机添加虚拟网络
            AccessMode        为虚拟机添加访问方式
    
        @param: 参数使用vm_dict_click字典定义的值:     
            VMAddThirdPifx    添加虚拟机，网络配置TAB的上一步
            VMAddThirdCansel  添加虚拟机，网络配置TAB的取消
            VMAddThirdNext    添加虚拟机，网络配置TAB的下一步
           
        '''
        #添加虚拟机-网络配置
        if vnet != "":
            self.setVMSelect("Vnet", vnet)    #设置虚拟机的虚拟网络
            
        if access_mode != "": 
            self.setVMSelect("AccessMode", access_mode)    #设置虚拟机的访问方式
        self.clickVMButton("VMAddThirdNext")
        return True
        
    def addVmDeployConfig(self, deploy_type="-RUNNING_VMS", host_cluster="2", free_cpu="0", free_mem="0"):    
        '''
        @summary: 添加虚拟机-部署配置
        @param : 无
        @return: True/False
            
        @param: 参数使用vm_dict_select字典定义的值:
            DeployType        为虚拟机设置部署方式: #  -RUNNING_VMS    虚拟机稀疏型
                                                   #  RUNNING_VMS    虚拟机密集型
                                                   #  FREECPU    CPU资源敏感
                                                   #  FREEMEMORY    内存资源敏感 
            HostCluster       为虚拟机设置主机资源池
            
        @param: 参数使用vm_dict_click字典定义的值:     
            VMAddAutodeploy   自动部署
            VMAddFreecpunum   空闲核数
            VMAddFreemem      空闲内存
            VMAddFourPifx     添加虚拟机，部署配置TAB的上一步
            VMAddFourCansel   添加虚拟机，部署配置TAB的取消
            VMAddFourNext     添加虚拟机，部署配置TAB的下一步
            VMAddFivePifx     添加虚拟机，完成TAB的上一步
            VMAddFiveCansel   添加虚拟机，完成TAB的取消
            VMAddFiveNext     添加虚拟机，完成TAB的下一步
        '''      
        #添加虚拟机-部署配置
        self.setVMSelect("DeployType", deploy_type)    
        self.setVMSelect("HostCluster", host_cluster)    #为虚拟机设置部署方式
        
        if int(free_cpu) > 0:
            self.clickVMButton("VMAddFreecpunum")
            self.setVMText("SecCpu", free_cpu)
        elif int(free_mem) > 0:
            self.clickVMButton("VMAddFreemem")
            self.setVMText("SecMem", free_mem)
        else:
            self.clickVMButton("VMAddAutodeploy")

        self.clickVMButton("VMAddFourNext")
        
        #添加虚拟机-完成
        time.sleep(2)
        self.clickVMButton("VMAddFiveNext") #完成
        
        return True

     
    def selectVm(self,vm_control,vm_select):
        '''
        @summary: 选中一台虚拟机
        @param : 无
        @return: True/False
        '''
        
        try:

            vmSelect = str(int(vm_select) + 1)
            
            xpath_sel_item = self.vm_dict_select[vm_control][1] + vmSelect + self.vm_dict_select[vm_control][2]
            select_item = self.driver.find_element_by_xpath(xpath_sel_item)
            
#            print "xpath_sel_item::"+xpath_sel_item
               
        except TimeoutException:
            print "FAIL: SELECT-ONE-VM combox CANNOT display."
            self.driver.close()
            return False
        else:
            time.sleep(1)   # 此处等待1秒，等页面加载完成，否则出现“服务不可用”的提示信息；后续的处理方式要进一步优化；
            select_item.click()        
            print "PASS: Click the combox successfully."
            return True    
          
        
#可用    
    def clickDeleteVmByName(self, vm_name):
        '''
        @summary: 根据虚拟机名称“删除”虚拟机
        @param : 无
        @return: True/False
        '''
        print "Begin: delete vm."
        if vm_name=="":
            self.selectVm("VmCheck", "0")  #选中所有的虚拟机
            time.sleep(2)
            self.clickVMButton("VMDelBtn")
            self.clickVMButton("VMConfirm")
            time.sleep(2)            
            message=self.getSystemMessage()
            print message
            if message=="False":
                return False
            else:
                return True
        else:        
            vmName=vm_name 
            row=self.findLineByName(vmName) # 选中某个虚拟机
            row=str(row)
            self.selectVm("VmCheck", row)
            time.sleep(2)
            self.clickVMButton("VMDelBtn")
            self.clickVMButton("VMConfirm")
        
            if row=="1":
                return True
            else:
                return False
             
        
#可用    
    def clickOpenVmByName(self, vm_name):
        '''
        @summary: 根据虚拟机名称“开启”虚拟机
        @param : 无
        @return: True/False
        '''
        vm_row = self.findLineByName(vm_name)
        self.selectVm("VmCheck", str(vm_row))
        time.sleep(5)
        self.clickVMButton("VMOpenBtn")
        print self.getSystemMessage()

        
#可用        

    def clickShutoffVmByName(self, vm_name):
        '''
        @summary: 根据虚拟机名称“关闭”虚拟机
        @param : 无
        @return: True/False
        '''     
        vm_row = self.findLineByName(vm_name)
        self.selectVm("VmCheck", str(vm_row))
        time.sleep(5)
        self.clickVMButton("VMShutoffBtn")
        self.clickVMButton("VMConfirm")  
        print self.getSystemMessage()
    
    def GetVmStatus(self, vm_name):
        '''
        @summary: 根据虚拟机名称，返回虚拟机状态
        @param : vm_name 虚拟机的名称
        @return: vm_status
        '''
        
        vm_row = self.findLineByName(vm_name)
        dict_list_element = self.getListElement()
        # title_wanna_find = (((self.getListHeadElement())[5]).text).strip()
        list_wanna_find = dict_list_element[u'虚拟机状态']
        vm_status = list_wanna_find[vm_row].text
        return vm_status

    def WaitCheckVmStatus(self, vm_name, vm_status):
        '''
        @summary: 等待虚拟机vm_name是否到预期的vm_status状态
        @param : vm_name 虚拟机的名称,vm_status 该虚拟机的目标状态
        @return: line/Fasle
        '''
        
        objVmStauts=vm_status
        
        times=0
        while times <= 100 :
            self.driver.refresh()
            vmStatus=self.GetVmStatus(vm_name)
            if vmStatus != objVmStauts:
                times=times+1
                # print "times=="+ str(times)
            else:
                return True
                break
    
#    def GetSelectline(self,vm_control):
#        '''
#        @summary: 获取下拉列表最大行数
#        @param : vm_control
#        @return: line
#        '''
#        i = 2
#        maxLine=10000
#        for i in range(2, str(maxLine)):
#            print "i==" + i
#            select_item_text=self.setVMSelect(vm_control, i)
#            if select_item_text == "":
#                return i
            
            
    def CheckDatablock(self,vm_control, vm_select,db_name):
        '''
        @summary: 检查datablock name
        @param : db_name
        @return: Ture/Fasle
        '''
        select_item_text=self.setVMSelect(vm_control, vm_select)
        print select_item_text
#        print db_name
        if select_item_text == db_name:
            return True
        else:
            return False
        
    def WaitCheckDatablock(self, vm_control, db_name):
        '''
        @summary: 检查datablock name
        @param : db_name 虚拟机数据盘的名称,vm_control 虚拟机控件名称
        @return: True/Fasle
        '''       
        db_flag=False
        DataBlock=2
        print self.vm_dict_select[vm_control][1]
        text= self.vm_dict_select[vm_control][1][:-1]
        maxLine=self.getListCountByXpath(text)
        
        while not db_flag:
            db_flag = self.CheckDatablock(vm_control, str(DataBlock), db_name)
            if db_flag:
                return True
                break
            else:
                DataBlock = DataBlock+1
                if DataBlock > int(maxLine):
                    return False
                    break


    def getListCountByXpath(self,xpath):
        '''
        return elements specified by xpath 's count
        
        '''
        try:
            elements = WebDriverWait(self.driver, 3).until(lambda driver: driver.find_elements_by_xpath(xpath))
                              
        except (StaleElementReferenceException, NoSuchElementException, TimeoutException), e:
            printLog(xpath + " is NOT available, \n" + str(e), "Error")
            return 0
        else :
            return len(elements)    
        

if __name__ == "__main__":
    # 设置firefox的profile文件，使其运行时默认的语言为中文
    profile = webdriver.FirefoxProfile()
    profile.set_preference("intl.accept_languages", "zh-cn, zh, en-us, en")  
    
    driver = webdriver.Firefox(profile)
    driver.get("http://10.1.60.180")  #最大化
    driver.implicitly_wait(5)
    
    from LoginPage import LoginPage    
    loginPage = LoginPage(driver)
    
    loginPage.loginAs("meiying", "qwer1234")   
    basePage = BasePage(driver)
    basePage.gotoPage("VM") 
    
    vmManagePage = VMPage(driver)
    
#添加虚拟机，可用
#    vmManagePage.addVmNormalMessage("meiying_vm", "meiying", "5", "2", "cs2c", "Qwer1234")
#    vmManagePage.addVmResourceConfig("50", "1", "", "2")
#    vmManagePage.addVmNetworkConfig("2", "")
#    vmManagePage.addVmDeployConfig("-RUNNING_VMS", "2", "50", "1024")
    vmManagePage.addVm("meiying_vm")
#    vmManagePage.clickVMButton("VMAdd")
#    vmManagePage.addVmNormalMessage()
#    vmManagePage.addVmResourceConfig()
#    vmManagePage.addVmNetworkConfig()
#    vmManagePage.addVmDeployConfig()
    
    vmManagePage.GetVmStatus("meiying_vm")    
    vmManagePage.CheckVmStatus("meiying_vm", u"正在运行")
 
#    vmManagePage.addVm("meiying_vm")
#    
#    row=0
#    while row <= 0 :
#        row=vmManagePage.CheckVmStatus(u"正在运行")  
#         
#        if row > 0:
#            vmManagePage.clickShutoffVmByName("meiying_vm", row)
    
#    rowShutoff=0
#    while rowShutoff <= 0 :
#        rowShutoff=vmManagePage.CheckVmStatus("已关机")  
#         
#        if rowShutoff > 0:
#            vmManagePage.clickOpenVmByName("meiying_vm", rowShutoff)
#            
#
#按照名字删除虚拟机可用    
    vmManagePage.clickDeleteVmByName("")

#按照名字开启虚拟机
#    vmManagePage.clickOpenVmByName("meiying_vm-0")

#按照名字关闭虚拟机
#    vmManagePage.clickShutoffVmByName("meiying_vm-0")

    
    loginPage.getUserName()
    
    loginPage.clickBaseButton("HomePage")
    
    loginPage.logout()
    driver.close()

