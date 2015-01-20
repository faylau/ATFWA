# -*- coding=utf-8 -*-
# Copyright (C), 2013, China Standard Software Co., Ltd.

"""
所有页面的的Base模块。
类说明:
    BasePage: 所有页面类的超类
方法说明:
    gotoPage: 进入页面，进入的页面和具体参数有关
    getPageButtonStatus: 获取按钮当前的状态
    clickBaseButton: 点击页面上的按钮，具体点击对象和参数有关
    getUserName: 获取当前登录用户的用户名
    getSystemMessage: 返回当前的系统信息
    getConfirmMessage:返回confirm提示框中的信息
    logout: 登出系统
    getCurrentPath: 获取当前导航的路径
    getListElement: 获取列表区域的所有的对象
    waitDataLoad: 等待中心区域列表中数据加载完成，仅作延时使用
    clickOperationButton: 点击记录的操作按钮
    findLineByName: 通过名字查找行号
    getOperationButton: 获取当前行中可用的操作按钮
    getMenu: 获取左侧菜单的导航区域
    clickCs2cLink: 点击页面下方的中标软件网站按钮链接
"""

__authors__ = [
  '"Huicong Ding" <huicong.ding@cs2c.com.cn>',
]
__version__ = "V0.4"

# ChangeLog:
# Version    Date            Desc                    Author
#-----------------------------------------------------------
# V0.1       06/09/2013      初始版本                 DHC
# V0.2       06/26/2013      修改至适应NKSCE2.2版本   DHC
# V0.3       12/04/2013      增加公共方法，目前此版本适用于NKSCE2.4版本
#                                                     DHC
# V0.4       12/06/2013      将打印信息改为英文       DHC
#-----------------------------------------------------------

from time import sleep

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
                                       TimeoutException, ElementNotVisibleException

from PageObject._pagetool import PageToolMixin
from Utils.PublicMethod import printLog, catchException, retry

class BasePage(PageToolMixin, object):
    '''
    @summary: 所有PageObject类的超类
    '''
    
    # 页面字典，索引为参数page_name
    # 第一个值含义是按钮的父按钮
    # 第二个值是将要进入页面的名字
    # 第三个字段是页面的URL，用来校验是否进入了正确的页面
    page_dict = {
        "GroupMgmt":           ("left_nav1_u", "用户组及组角色管理", "group/manage.action"),
        "RoleMgmt":            ("left_nav1_u", "组内角色管理", "role/manage.action"),
        "UserMgmt":            ("left_nav1_u", "用户管理", "user/manage.action"),
        "HostClusterMgmt":     ("left_nav2_u", "主机资源池管理", "hostCluster/manage.action"),
        "HostMgmt":            ("left_nav2_u", "主机管理", "host/manage.action"),
        "NetworkMgmt":         ("left_nav2_u", "网络管理", "virtualNetwork/manage.action"),
        "ImgMgmt":             ("left_nav2_u", "映像管理", "image/manage.action"),
        "MyResc":              ("left_nav2_u", "我的资源", "resource/manage.action"),
        "VM":                  ("left_nav3_u", "虚拟实例", "virtualMachine/manage.action"),
        "Log&Audit":           ("left_nav4_u", "日志与审计", "security/auditrecord/manage.action"),
        # "ConfBak":             ("left_nav4_u", "配置信息备份与恢复", "security/bakconfig/manage.action"),
        "UKeyConf":            ("left_nav4_u", "USBkey配置", "security/ukeyauth/manage.action"),
        "AuthConf":            ("left_nav4_u", "多因子认证配置", "security/authinfo/manage.action"),
        "RealtimeMonitor":     ("left_nav5_u", "实时监控", "icinga/manage.action"),
        "Statistics":          ("left_nav5_u", "统计报表", "statistics/hostList.action"),
        "Alarm":               ("left_nav5_u", "预警信息", "statistics/monitorwarmlog.action"),
        # "Topology":            ("left_nav5_u", "网络拓扑", "tuopu/manage.action"),
        "StorageClusterMgmt":  ("left_nav6_u", "集群管理", ""),
        "StorageNodeMgmt":     ("left_nav6_u", "存储节点管理", ""),
        "VolumeMgmt":          ("left_nav6_u", "卷管理", ""),
        # "TaskMgmt":            ("left_nav6_u", "任务管理", ""), 此页面已删除
        "LoadBalance":         ("left_nav7_u", "负载均衡", "statistics/balancelog.action"),
        "SoftwareDownload":    ("left_nav7_u", "软件下载", "softdownload/manage.action"),
    }
    
    # 存储左下角的翻页相关元素、右上角用户操作区的元素、全局添加删除按钮
    dict_page_button = {
        "First":"//*[@class='l-btn-empty pagination-first']",                           # 首页按钮
        "Prev":"//*[@class='l-btn-empty pagination-prev']",                             # 上一页按钮
        "Next":"//*[@class='l-btn-empty pagination-next']",                             # 下一页按钮
        "Last":"//*[@class='l-btn-empty pagination-last']",                             # 最后一页按钮
        "Refresh":"//*[@class='l-btn-empty pagination-load']" ,                         # 刷新按钮
        "Refreshing":"//*[@class='l-btn-empty pagination-load pagination-loading']",    # 刷新加载时的按钮
        "Add":"//*[@class='l-btn-text icon-add']",                                      # 添加按钮
        "Del":"//*[@class='l-btn-text icon-cancel']",                                   # 删除按钮
        "ConfirmOk":".//*[@class='messager-button']/a[1]/*[@class='l-btn-left']",       # 确认框确定按钮
        "ConfirmCancel":".//*[@class='messager-button']/a[2]/*[@class='l-btn-left']",   # 确认框取消按钮
        "HomePage": "//*[@class='icon1']",                                              # 主页按钮
        "PersonalInformation":"//*[@class='icon2']",                                    # 个人信息
        "ChangePasswd":"//*[@class='icon3']",                                           # 修改密码
        "About":"//*[@class='icon4']",                                                  # 关于
        "Authorization":"//*[@class='icon6']",                                          # 授权信息
        "Logout":"//*[@class='icon5']",                                                 # 登出
        # "Cancel":"//*[text()='取消']"  # 一个弹出窗口有n个text是取消的按钮，暂不实现
    }
    
    dict_page_exist = {
        "ValidateTip":".//span[@class='validatebox-tip-content']",
        "PageNum":"//div[@id='user_display']/div/div/div[3]/table/tbody/tr/td[8]/span",
        "PageNo":"//div[@id='user_display']/div/div/div[3]/table/tbody/tr/td[7]/input",
        "VolLogPageNum":".//div[@id='volumelog-pager']/table/tbody/tr/td[7]/input",
        "PasswdDialog":".//div[@id='passwd-dialog']",
        "UserDelBtn":    ".//*[@id='btndeleteUser']",
        "EditDialog":".//div[@id='edit-dialog']",
    }
    
#     pop_window_button_dict = {#"Cancel":"取消",
#                               "NextStep":"下一步",
#                               "PrevStep":"上一步",
#                               "OK":"确定",
#                               "Done":"完成",
#                               "Reset":"重置"
#                               }
    
    XPATH_ELEMENT_USER_NAME = '//*[@class="user_top"]'  # 当前登录用户
    XPATH_POP_WINDOW = '//*[@class="panel window"]'  # 页面弹出窗口的XPath
    
    def __init__(self, driver):
        '''
        @summary: 构造函数
        '''
        self.driver = driver  # 将浏览器实例传递给self.driver
            
    def keyPress(self,key,dict_control=None):        
        ac = ActionChains(self.driver)  # 模拟鼠标动作的实例
        if dict_control != None:
            try:
                element=self.driver.find_element_by_xpath(self.dict_page_exist[dict_control])
            except (StaleElementReferenceException, NoSuchElementException, TimeoutException), e:
                printLog(dict_control + "USER_CONTROL doesn't work, \n" + str(e), "Error")
            else:
                if element != None:
                    element.send_keys(key)
                else:
                    ac.send_keys(key).perform()   
        
#    __retry_times = 5
    @retry()
    def gotoPage(self, page_name):
        '''
        @summary: 进入页面方法
        @return: 成功返回True，失败返回False
        @param: 参数使用page_dict字典定义的值:
            GroupMgmt           用户组及组角色管理       
            RoleMgmt            组内角色管理              
            UserMgmt            用户管理
            HostClusterMgmt     主机资源池管理
            HostMgmt            主机管理                  
            NetworkMgmt         网络管理               
            ImgMgmt             映像管理                
            MyResc              我的资源               
            VM                  虚拟实例                              
            Log&Audit           日志与审计  
            ConfBak             配置信息备份与恢复
            UKeyConf            USBkey配置
            AuthConf            多因子认证配置
            RealtimeMonitor     实时监控
            Statistics          统计报表
            Alarm               预警信息
            Topology            网络拓扑
            StorageClusterMgmt  集群管理
            StorageNodeMgmt     存储节点管理
            VolumeMgmt          卷管理
            TaskMgmt            任务管理
            LoadBalance         负载均衡
            SoftwareDownload    软件下载
        @bug: 存在一定机率失败的情况
        '''
        
        # 主页上等待2秒，防止flash图对本方法的干扰
        if "index.action" in self.driver.current_url:
            sleep(2)
        
        try:
            menu = self.getMenu()
            father_button = menu.find_element_by_id(self.page_dict[page_name][0])
            # father_button.click()
        except NoSuchElementException:
            printLog(
                "Can not enter page '" + page_name + "', please make sure that you have the correct right!", 
                "Error"
            )
            return False
        except KeyError:
            printLog(
                "The parameter of 'gotoPage' is wrong, please Refer to documents of the method!",
                "Error"
            )
            return False
        try:           
            ac = ActionChains(self.driver)  # 模拟鼠标动作的实例
            ac.move_to_element_with_offset(father_button, 0, 20).perform()
            printLog("Moving to " + page_name + "'s father button...", "debug")
            page_button = menu.find_element_by_link_text(self.page_dict[page_name][1])
            # ac.move_by_offset(0, -25).perform()
            ac.move_by_offset(100, 0).perform()  # 移动鼠标位置，防止鼠标离开菜单造成二级菜单不可点击
            # page_button = self.driver.find_element_by_link_text(self.page_dict[page_name][1])
        except NoSuchElementException, TimeoutException:
            printLog("Failed to turn to page %s." % page_name)
            return False
            #print self.__retry_times
            #sleep(5 * i)
        else:
            printLog("Turning to page '%s' ..." % page_name, "debug")
            page_button.click()
            current_url = self.driver.current_url
            current_path = self.getCurrentPath()
            printLog("The URL of current page is" + current_url, "debug") 
            if self.page_dict[page_name][2] in current_url\
                    and self.page_dict[page_name][1] in current_path:
                printLog("Successfully turned to page '" + page_name + "'.")
                return True
            else:
                printLog("Method 'gotoPage' failed, stop this testcase!", "Error")
                raise NoSuchElementException
    
    def getPageButtionStatus(self, button_xpath):
        '''
        @summary: 检查按钮是否可用
        @param obj_button: 按钮实例
        @return: 按钮可用返回True，不可用返回False 
        '''
        try:
            father_element_xpath = button_xpath + "/../../.."
            father_element = self.driver.find_element_by_xpath(father_element_xpath)
            is_disable = father_element.get_attribute("class").endswith("disabled")  # 按钮如果被禁用，此处会以disabled结尾
            button = self.driver.find_element_by_xpath(button_xpath)
        except ElementNotVisibleException:
            return False
        else:
            is_clickable = not is_disable
            return button.is_displayed() and button.is_enabled() and is_clickable 
        
    def clickBaseButton(self, button):
        '''
        @param : 
            First                    首页按钮
            Prev                     上一页按钮
            Next                     下一页按钮
            Last                     最后一页按钮
            Refresh                  刷新按钮
            Add                      添加按钮
            Del                      删除按钮
            HomePage                 主页按钮
            PersonalInformation      个人信息
            ChangePasswd             修改密码
            About                    关于
            Authorization            授权信息
            Logout                   登出
            ConfirmOk                弹出的确认框的确定按钮
            ConfirmCancle            弹出的确认框的取消按钮
        '''
#         if button in self.pop_window_button_dict:
#             try:
#                 pop_window_button = WebDriverWait(self.driver, 10).\
#                         until(lambda driver: driver.find_element_by_link_text(self.pop_window_button_dict[button]))
#             except (StaleElementReferenceException, NoSuchElementException, TimeoutException), e:
#                 printLog(button + "按钮不可用！详情信息如下：\n" + str(e), "Error")
#             else:
#                 if self.getPageButtionStatus(pop_window_button):
#                     sleep(5)  # 等待页面加载
#                     pop_window_button.click()
#                     printLog("点击按钮" + button)
#                 else:
#                     printLog(button + "按钮不可用！", "Error")
#         else:

        self.waitDataLoad()
        try:
            btn_xpath = self.dict_page_button[button]
            btn_page_button_tmp = WebDriverWait(self.driver, 3).\
                        until(lambda driver: driver.find_element_by_xpath(btn_xpath))
            if "@class='icon" in btn_xpath:
                # print 1
                btn_page_button = btn_page_button_tmp.find_element_by_tag_name('a')
            else:
                btn_page_button = btn_page_button_tmp
        except (KeyError, UnboundLocalError):
            printLog("Wrong parameters of method clickBaseButton, please Refer to documents of the method!", "Error")
        except (StaleElementReferenceException, NoSuchElementException, TimeoutException), e:
            printLog(button + "is unavailable! Here are the messages:\n" + str(e), "Error")
        else:
            if self.getPageButtionStatus(self.dict_page_button[button]):
                btn_page_button.click()
                printLog("Click button " + button)
            else:
                printLog(button + "is unavailable!", "Error")
    
    def is_element_exist(self,dict_control):
        if dict_control in self.dict_page_exist:
            try:
                WebDriverWait(self.driver, 10).\
                        until(lambda driver: driver.find_element_by_xpath(self.dict_page_exist[dict_control]))
            except (StaleElementReferenceException, NoSuchElementException, TimeoutException), e:
                print dict_control + "is not exist." 
                return False
            return True
        else:
            try: 
                self.driver.find_element_by_xpath(dict_control)
            except (StaleElementReferenceException, NoSuchElementException, TimeoutException), e:
                printLog(dict_control + "CONTROL doesn't work, \n" + str(e), "Error")
                return False
            return True
    def is_element_visiable_by_xpath(self,dict_control):        
        result=False
        if dict_control in self.dict_page_exist:
            xpath= self.dict_page_exist[dict_control]
        else:
            xpath=dict_control
        try:
            ele= WebDriverWait(self.driver, 10).\
                    until(lambda driver: driver.find_element_by_xpath(xpath))
            if ele.is_displayed():
                result=True
                 
        except (StaleElementReferenceException, NoSuchElementException, TimeoutException), e:
            printLog(dict_control + "VM_CONTROL doesn't work, \n" + str(e), "Error")
            return result
        return result
        #可用        
    def setSelectByText(self,ID,text):
        '''
        @summary: 根据值选择下拉列表
        @return: 成功返回True，失败返回False
        @param: 参数使用元素ID值:         
        '''        
        XPATH_DATA = "//*[@id='"+ID+"']"  # 列表中所有元素所在的body        
        try:
            select = self.driver.find_element_by_xpath(XPATH_DATA)
        except NoSuchElementException:
            printLog("Can't find select in the page，please make sure that you are on the correct page!", "Error")
            return False        
        list_ = select.find_elements_by_tag_name("option")  
        count_row = len(list_)        
        if not count_row:
            printLog("There is no element in the select.", "Error")
            return False
                
        # 将所有body中的对象存储到dict_list字典中
        for i in range(count_row):
            if text==list_[i].text:
                list_[i].click()
                return i
    def getUserName(self):
        '''
        @summary: 获取当前登录用户的用户名
        @return: 获取成功返回用户名，否则返回False
        '''
        try:
            user_top = self.driver.find_element_by_xpath(self.XPATH_ELEMENT_USER_NAME)
            user_name = user_top.text
            printLog("Greeting message: " + user_name)
        except NoSuchElementException:
            return False
        else:
            user_name_text = user_name.split()
            return user_name_text[1]
    
    def getSystemMessage(self):
        '''
        @attention: 该方法应该系统信息出现后立即调用，否则可能返回错误的返回值
        @summary: 获取系统信息窗口的文本内容
        @return: 获取成功返回系统提示信息的内容，否则返回False
        '''
        try:
            system_message = WebDriverWait(self.driver, 10).\
                        until(lambda driver: driver.find_element_by_css_selector(".messager-body.panel-body.panel-body-noborder.window-body"))           
            sleep(1)
            system_message = self.driver.find_element_by_css_selector(".messager-body.panel-body.panel-body-noborder.window-body")
                
        except NoSuchElementException:
            printLog("Can not find the system information on the lower right corner.", "Warn")
            return False
        else:
            return system_message.text
    def getConfirmMessage(self):
        '''
        @summary: 获取fonfirm信息窗口的文本内容
        @return: 获取成功返回系统提示信息的内容，否则返回False
        '''
        try:
            system_message = WebDriverWait(self.driver, 3).\
                        until(lambda driver: driver.find_element_by_css_selector(".messager-body.panel-body.panel-body-noborder.window-body"))           
            sleep(1)
            system_message = self.driver.find_element_by_css_selector(".messager-body.panel-body.panel-body-noborder.window-body")
            confirm_message = system_message.find_element_by_css_selector("div:nth-child(2)")
        except NoSuchElementException:
            printLog("Can not find the system information on the lower right corner.", "Warn")
            return False
        else:
            return confirm_message.text
    def notLegalInput(self):
        '''
        @attention: 该方法应该系统信息出现后立即调用，否则可能返回错误的返回值
        @summary: 获取系统信息窗口的文本内容
        @return: 获取成功返回系统提示信息的内容，否则返回False
        '''
        try:
            self.driver.find_element_by_xpath(self.dict_page_exist["ValidateTip"])
        except  NoSuchElementException:
#            print "ValidateTip not exist" 
            return False
        else:
            return True
        
    def logout(self):
        '''
        @summary: 登出系统
        @return: 成功返回True，失败返回False
        '''
        # self.driver.refresh()
        self.clickBaseButton("Logout")
        printLog("Logging out...")
        # return not self.getUserName()
        return 'logout.action' in self.driver.current_url
    
    def getCurrentPath(self):
        '''
        @summary: 获取当前页面的导航路径信息
        @return: 成功返回页面导航路径，失败返回False
        '''
        try:
            full_path = self.driver.find_element_by_xpath("//*[@class='position']").text
        except NoSuchElementException:
            printLog("Can not find navigation path on the current page 。", "Warn")
            return False
        else:
            path = full_path[5:]
            printLog("The navigation path on the current page is " + path, "debug")
            return path
    
    def getListHeadElement(self):
        # XPATH_DATA_HEAD = "//*[@class='datagrid-view2']/*[@class='datagrid-header']"  # 列表title的XPath
        # data_head = self.driver.find_element_by_xpath(XPATH_DATA_HEAD)
        # table_head = data_head.find_element_by_tag_name("tbody")
        
        _data_head = 'div.datagrid-view2 > div.datagrid-header tbody'
        table_head = self.driver.find_element_by_css_selector(_data_head)
        list_head = table_head.find_elements_by_css_selector("td")  # 存储所有head中的对象
        return list_head
       
    def getListElement(self):
        '''
        @summary: 获取列表区域的所有的对象
        @param : None
        @return: 获取成功，返回含有列表所有元素的字典，获取失败返回False
            字典的格式举例：
            {"复选框": [全选框, 复选框1, 复选框2, 复选框3, ...]
             "虚拟机ID": [<虚拟机ID>, 34, 38, 104, ...],
             "虚拟机名称": [<虚拟机名称>, 'win7', 'XP', 'nk6', ...],
              ...
            }
        @attention:
            ①返回的字典的key一定要使用utf编码！！！如list_obj[u"虚拟机名称"]
            ②返回的字典的列表中的成员都是WebElement对象而不是文本
            ③每个字典中的值都是一个列表(list)，其中索引为0的是界面中title那一样的对象（如全选框），
                body中的对象索引从1开始。
        '''
        
        self.waitDataLoad()
        
        # XPATH_DATA_BODY = "//*[@class='datagrid-view2']/*[@class='datagrid-body']"  # 列表中所有元素所在的body
        # self.TAG_TBODY = "tbody"
        TAG_TBODY = "div.datagrid-view2 > div.datagrid-body tbody"
        
        try:
            # data_body = self.driver.find_element_by_xpath(XPATH_DATA_BODY)
            table_body = self.driver.find_element_by_css_selector(TAG_TBODY)
        except NoSuchElementException:
            printLog("Can't find datagrid in the page，please make sure that you are on the correct page!", "Error")
            return False
        
        printLog("Starting to get the elements on the body...", "debug")
        dict_list = {}
        list_body_row = table_body.find_elements_by_css_selector("tr")  # 存储body中的行
        list_head = self.getListHeadElement()
        count_column = len(list_head)
        count_row = len(list_body_row)
        output_format = "There are %d row(s), %d column(s) in the body." % (count_row, count_column)
        printLog(output_format, "debug")
        
        if not count_row:
            printLog("There is no element in the body.", "Error")
            return False
        
        for k in range(count_column):
            dict_list[list_head[k].text] = [list_head[k]]  # 初始化dict_list字典，将head中的对象存储在索引0的位置
        
        # 将所有body中的对象存储到dict_list字典中
        for i in range(count_row):
            list_body_field = list_body_row[i].find_elements_by_css_selector("td")
            for j in range(count_column):
                dict_list[list_head[j].text].append(list_body_field[j])
        
        # 为复选框添加字典的key，并去掉key的空格
        try:
            dict_list['']
        except Exception:
            pass
        else:
            dict_list[u'复选框'] = dict_list['']
            del dict_list['']
        
        dict_list_tmp = {}
        for key in dict_list:
            dict_list_tmp[key.strip()] = dict_list[key]
        dict_list = dict_list_tmp
        
        printLog("Successfully got elements in the list area(%d row(s), %d column(s)), return a dictionary of elements." % (count_row, count_column), 'debug')
        return dict_list
    
    def getListNum(self):
        '''
        @summary: 获取列表区域的所有的对象
        @param : None
        @return: 获取成功，返回含有列表所有元素的字典，获取失败返回False
            字典的格式举例：
            {"复选框": [全选框, 复选框1, 复选框2, 复选框3, ...]
             "虚拟机ID": [<虚拟机ID>, 34, 38, 104, ...],
             "虚拟机名称": [<虚拟机名称>, 'win7', 'XP', 'nk6', ...],
              ...
            }
        @attention:
            ①返回的字典的key一定要使用utf编码！！！如list_obj[u"虚拟机名称"]
            ②返回的字典的列表中的成员都是WebElement对象而不是文本
            ③每个字典中的值都是一个列表(list)，其中索引为0的是界面中title那一样的对象（如全选框），
                body中的对象索引从1开始。
        '''
        
        self.waitDataLoad()
        
        XPATH_DATA_BODY = "//*[@class='datagrid-view2']/*[@class='datagrid-body']"  # 列表中所有元素所在的body
        self.TAG_TBODY_ = "tbody"        
        try:
            data_body = self.driver.find_element_by_xpath(XPATH_DATA_BODY)
            table_body = data_body.find_element_by_tag_name(self.TAG_TBODY_)
        except NoSuchElementException:
            printLog("Can't find datagrid in the page，please make sure that you are on the correct page!", "Error")
            return False        
        list_body_row = table_body.find_elements_by_tag_name("tr")  # 存储body中的行        
        count_row = len(list_body_row)        
        return count_row
    
    
    # XPATH_IMG_ADDDIALOG_REFRESH = "//div[@id='add-dialog']//div[@class='loadmask-label']"
    __XPATH_REFRESHING_TEXT_BOX = "//div[@class='datagrid-mask-msg']"
    __XPATH_GLUSTER_REFRESHING_TEXT_BOX = "//div[@class='datagrid-mask-msg bb-mask-msg']"
    def waitDataLoad(self):
        '''
        @summary: 等待加载数据完成，仅作延时使用
        '''
        
        self.driver.implicitly_wait(1)
        try:
            # 找“正在处理，请稍后”的处理框（映像管理页面）
            # WebDriverWait(self.driver, 120, 0.2)\
            #         .until_not(lambda driver: driver.find_element_by_xpath(self.XPATH_IMG_ADDDIALOG_REFRESH).is_displayed())
                    
            # 等待“正在处理，请稍后”消失
            # printLog("Waiting for refresh button displayed.", "debug")
            WebDriverWait(self.driver, 120, 0.2)\
                    .until_not(lambda driver: driver.find_element_by_xpath(self.__XPATH_REFRESHING_TEXT_BOX).is_displayed())
                    
            # 等待“正在处理，请稍后”消失（存储服务界面的）
            WebDriverWait(self.driver, 120, 0.2)\
                    .until_not(lambda driver: driver.find_element_by_xpath(self.__XPATH_GLUSTER_REFRESHING_TEXT_BOX).is_displayed())
            
            
#             printLog("Waiting for data loading...")
#             # 等待60s，直到刷新按钮出现，刷新完毕
#             WebDriverWait(self.driver, 60, 0.2, (StaleElementReferenceException))\
#                     .until(lambda driver: driver.find_element_by_xpath(self.dict_page_button["Refresh"])\
#                     .is_displayed())
        except:
            pass
               
#         else:
#             printLog("Waiting for data loading...")
#             # 等待60s，直到刷新消失，刷新完毕
#             WebDriverWait(self.driver, 60, 0.2, (StaleElementReferenceException))\
#                     .until_not(lambda driver: driver.find_element_by_xpath(self.XPATH_IMG_ADDDIALOG_REFRASH)\
#                     .is_displayed())

        self.driver.implicitly_wait(5)
            
    
    def clickOperationButton(self, key=1, btn_name=None):
        '''
        @summary: 点击记录的操作按钮
        @param:
            key: 操作行的关键字，可以是行号或名字
            btn_name: 要点击的按钮的中文完整名字
        @return: 点击成功返回True，否则返回False
        @change: 
            2013/11/22  去掉by_what参数，用getOperationButton方法获取操作按钮
        '''

        try:
            all_btn = self.getOperationButton(key)
            btn = all_btn[unicode(btn_name)]
        except KeyError:
            printLog("The raw you selected have no '" + btn_name + "'button!", "Error")
            return False
        else:
            btn.click()
            printLog("Successfully clicked '" + btn_name + "' button.", "Mess")
            return True

    @catchException()    
    def findLineByName(self, key):
        '''
        @summary: 通过行的名字返回行号
        '''
        dict_list_element = self.getListElement()
        if not dict_list_element:
            return False
        
        if "虚拟实例" in self.getCurrentPath():
            title_wanna_find = (((self.getListHeadElement())[2]).text).strip()
        else:
            title_wanna_find = (((self.getListHeadElement())[1]).text).strip()
        list_wanna_find = dict_list_element[title_wanna_find]
        list_wanna_find_text = []
        for obj in list_wanna_find:
            list_wanna_find_text.append(obj.text)
        
        # print list_wanna_find_text
        try:
            line = list_wanna_find_text.index(key)
        except ValueError:
            printLog("Can not find the line number that corresponding to " + key + ", please make sure if the name is exist.", "Error")
            return False
        
        return line
            
    
    def getOperationButton(self, key):
        '''
        @summary: 获取当前行支持的操作
        @param:
            key: 可以是名字或者行号
        @return: 包括操作名称和按钮对象的字典，如：
            {
            "负载均衡配置": <Obj>,
            "IPMI配置": <Obj>,
            ...
            }
        '''
        
        # 将key转化为行号
        str_key = str(key)
        if str_key.isdigit():
            int_key = key
        else:
            int_key = self.findLineByName(key)
        
        btn = {}
        dict_list_element = self.getListElement()
        operation_field = dict_list_element[u"操作"][int_key]
        all_div = operation_field.find_elements_by_tag_name("div")  # 此处的div结构：索引为0的无用，为1的是第一个按钮，为2的是第一个按钮的中文名字，以此类推
        btn_count = (len(all_div) - 1) / 2
        # print btn_count, len(all_div)
        # print all_div[2].text
        for i in range(1, btn_count + 1):
            ac = ActionChains(self.driver)
            ac.move_to_element(all_div[i*2 - 1])
            ac.perform()
            btn[all_div[i*2].text] = all_div[i*2 - 1]
        # print btn
        printLog("Successfully got the buttons of the operation column.")
        return btn

    def onlyNum(self,s):
        '''
        @summary:        
        '''
        fomart = "0123456789"
        for c in s:
            if not c in fomart:
                s=s.replace(c,"")
        return int(s)
    
    def getMenu(self):
        '''
        @summary: 获取左侧导航区域
        '''
        try:
            menu = self.driver.find_element_by_xpath("//div[@class='left_nav_block']")
        except:
            printLog("Failed to get the menu area.", "error")
        else:
            printLog("Successfully got the Menu area.", 'debug')
            return menu
    
    def clickCs2cLink(self):
        '''
        @summary: 点击页面下方的中标软件网站按钮链接
        '''
        cs2c_link = self.driver.find_element_by_link_text(u"中标软件有限公司")
        cs2c_link.click()
        return True
    
    def getElement(self, xpath, father_element=None):
        '''
        @summary: 根据xpath和父对象返回对象
        '''
        try:
            if father_element:
                element = father_element.find_element_by_xpath(xpath)
            else:
                element = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException, e:
            printLog("Error, the detail is: %s" % e)
            return False
        else:
            return element
    
    @catchException()    
    def selectBoxByName(self, name):
        '''
        @summary: 根据名字选中复选框
        '''
        line = self.findLineByName(name)
        list_element = self.getListElement()
        box = list_element[u'复选框'][line]
        box.click()
    
    def getConfirmWindow(self):
        try:
            confirm_window = self.driver.find_element_by_xpath("//*[@class='panel window messager-window']")
        except:
            printLog("Can not find the confirm window!", "Error")
            return False
        else:
            return confirm_window

if __name__ == "__main__":
    pass
