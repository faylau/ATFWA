# -*- coding=utf-8 -*-
# Copyright (C), 2014, China Standard Software Co., Ltd.

'''

类说明:

方法说明:

'''

__authors__ = [
  '"Huicong Ding" <huicong.ding@cs2c.com.cn>'
]

__version__ = "V0.2"

# ChangeLog:
# Version    Date            Desc                Author
#--------------------------------------------------------
# V0.1       01/22/2014      初始版本            DHC 
# V0.2       03/28/2014      完成get_element和select_option两个公共方法
#                                                DHC
#--------------------------------------------------------

from selenium.common.exceptions import NoSuchElementException, TimeoutException, \
                                       StaleElementReferenceException

from Utils.PublicMethod import printLog, catchException

class PageToolMixin:
    '''
    @summary: 工具类，包含了web页面的各种基本操作
    '''
    
    def __init__(self, driver):
        self.driver = driver
    
    def click_button(self, btn_css=None):
        '''
        @summary: 根据xpath参数点击按钮 
        @param:
            btn_css: 按钮的xpath
        @return: 成功返回True，失败返回False
        '''
        if self.is_usable(btn_css):
            try:
                button = self.get_element(btn_css)
                button.click()
                return True
            except (NoSuchElementException, TimeoutException):
                printLog("Can not find the button by xpath: '%s'.", "Error")
                return False
            except StaleElementReferenceException:
                printLog("The element(xpath: %s) is not as same as it has been located, " +\
                        "plese check your code." % btn_css, "Error")
                return False
        else:
            printLog("The button is unusable, and can not be clicked!", "Error")
            return False
    
    @catchException()
    def is_usable(self, element_css=None):
        '''
        @summary: 判断一个对象是否可用
        @param:
            element_css: 对象的xpath
        @return: 可用返回True，不可用返回False
        '''
        element = self.get_element(element_css)
        return element.is_enabled() and element.is_displayed()
    
    @catchException()
    def set_text(self, input_css=None, text=None):
        '''
        @summary: 发送字符到目标element
        @param:
            input_css: 输入框的xpath
            text: 要输入的字符串
        '''
        input_ = self.get_element(input_css)
        input_.clear()
        input_.send_keys(text)
    
    def select_option(self, selector_css=None, item_css=None):
        '''
        @attention: 由于目前安全云的web中没有严格意义上的下拉菜单，此处先不做定义！！！ 
        @summary: 选择下拉菜单的一个选项
        @param:
            selector_css: 下拉菜单的xpath
            item_css: 需要选择的项的xpath
            
        '''
        pass
    
    @catchException('Failed to get the element!')
    def get_element(self, element_css=None, father_element=None):
        '''
        @summary: 获取页面元素
        @param:
            element_css: 要获取的对象的CSS
            father_element: 父对象（即已父对象为基准进行查找）
        @return: 获取成功，返回对象；获取失败，返回False
        '''
        return father_element.find_element_by_css_selector(element_css) \
            if father_element \
            else self.driver.find_element_by_css_selector(element_css)
    