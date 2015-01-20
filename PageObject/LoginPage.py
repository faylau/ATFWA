# -*- coding=utf-8 -*-
# Copyright (C), 2013, China Standard Software Co., Ltd.

"""
登录页面的类。
类说明:
    LoginPage: 登录页面类 
方法说明:
    getVerificationCode: 获取验证码，暂未实现
    setUserName: 在用户名输入框输入用户名
    setPassword: 在密码输入框输入密码
    setVerificationCode: 输入验证码
    clickLoginButton: 点击登录按钮
    loginAs: 以参数中的用户名和密码登录系统
    getFailedLoginMessage: 获取登录失败信息
"""

__authors__ = [
  '"Meiying Li" <meiying.li@cs2c.com.cn>'
  '"Huicong Ding" <huicong.ding@cs2c.com.cn>',
]
__version__ = "V0.3"

# ChangeLog:
# Version    Date            Desc                Author
#----------------------------------------------------------
# V0.1       03/20/2013      初始版本            meiying.li
# V0.2       06/09/2013      重新封装本类提供的方法
#                                                DHC
# V0.3       06/26/2013      修改至适应NKSCE2.2版本
#                                                DHC
#----------------------------------------------------------

import time
import socket
from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from BasePage import BasePage
from Utils.PublicMethod import printLog, catchException

class LoginPage(BasePage):
    '''
    @summary: 登录页面中的元素和方法定义
    '''
    
    # 通过firebug获取空间的id或者xpath，并赋值给特定的变量
    ID_INPUT_USER_NAME = "userName"             # 常量：登录用户名的id
    ID_INPUT_PASSWORD  = "passwd"               # 常量：登录用户密码的id
    ID_VERIFICATION_Code = "checkCode"          # 常量：验证码输入框的id
    ID_BTN_LOGIN       = "login-button"         # 常量：登录按钮的id
    ID_SPAN_ERROR_MSG  = "errorMsg"             # 登录失败提示错误信息的控件id
    
    def __init__(self, driver):
        super(LoginPage, self).__init__(driver)
        # BasePage.__init__(self, driver)
        self.login_retry_times = 5  #登录时IP没有释放时的重试次数设置。
    
    def getVerificationCode(self):
        '''
        @summary: 获取验证码
        '''
        return 8888  # 暂未实现，先返回个假的
    
    def setUserName(self, user_name):
        input_userName = self.driver.find_element_by_id(self.ID_INPUT_USER_NAME)
        input_userName.clear()
        input_userName.send_keys(user_name)  # 输入登录用户名
        return True
    
    def setPassword(self, password):
        input_userPwd = self.driver.find_element_by_id(self.ID_INPUT_PASSWORD)
        input_userPwd.clear()
        input_userPwd.send_keys(password)    # 输入密码
        return True
    
    def setVerificationCode(self):
        input_verificationCode = self.driver.find_element_by_id(self.ID_VERIFICATION_Code)
        input_verificationCode.clear()
        input_verificationCode.send_keys(self.getVerificationCode())  # 输入验证码
        return True
            
    def clickLoginButton(self):
        btn_login = self.driver.find_element_by_id(self.ID_BTN_LOGIN)
        btn_login.click()                   # 单击登录按钮
        return True

    def loginAs(self, user_name="neoadmin", password="qwer1234"):
        '''
        @summary: 登录系统方法，会自动处理IP地址被自己占用的情况
        @return: 
            正常登录返回True
            登录后用户名异常，返回当前登录的用户名
            出错且无法处理时，返回错误信息
        '''  
        try:
            self.setUserName(user_name)
            self.setPassword(password)
            self.setVerificationCode()
            self.clickLoginButton()
        except NoSuchElementException:
            printLog("Can not perform login operation, please make sure if you are on login page.", "Error")
         
        #需要验证登录是否成功，及登录成功的用户名是什么
        real_user_name = self.getUserName()
        # print real_user_name
        if user_name == real_user_name:
            printLog("Login successfully, the current user is: " + real_user_name, "Pass")
            return True
        elif real_user_name:
            return real_user_name
        else:
            try:
                error_message = self.getFailedLoginMessage()
            except NoSuchElementException:
                printLog("Login failed, did't find the reason.", "Fail")
            else:
                printLog('Login failed, the reason is: "' + error_message + '".', "Fail")
                if "当前用户已经登录" in error_message:
                    ip_start = error_message.index("登录IP为")
                    ip_end = error_message.index("，错误码")
                    login_ip = error_message[ip_start+5: ip_end]  # 获取用户的当前登录IP
                    my_name = socket.getfqdn(socket.gethostname())
                    my_addr = socket.gethostbyname(my_name)  # 获取本地IP
                    if login_ip == my_addr:
                        printLog("This user have not logout after login on the current computer, waiting for timeout，retry time: "\
                                 + str(6 - self.login_retry_times))
                        if self.login_retry_times:
                            time.sleep(10)
                            self.login_retry_times -= 1
                            return self.loginAs(user_name, password)
                        else:
                            printLog("Login error! This user is still online via %s after %d times' retry." \
                                     %(str(login_ip), self.login_retry_times), "Error")
                            return error_message
                    else:
                        printLog("This user is online via IP: " + login_ip, "Error")
                        return False
                else:
                    return False
        
    def getFailedLoginMessage(self):
        '''
        @summary: 获取登录失败时系统返回的错误信息
        '''
        try:
            error_message = self.driver.find_element_by_id("errorMsg").text
        except NoSuchElementException:
            printLog("No error message of login output.")
        else:
            return error_message

#     def loginInvalidUser(self, userName, userPwd):
#         '''
#         @summary: 非法用户登录，包括用户名或密码错误等情况
#         @param userName: 用户名； userPwd：用户密码
#         @return: True or False
#         '''
#         input_userName = self.driver.find_element_by_id(self.ID_INPUT_USER_NAME)
#         input_userPwd = self.driver.find_element_by_id(self.ID_INPUT_PASSWORD)
#         btn_login = self.driver.find_element_by_id(self.ID_BTN_LOGIN)
#         
#         input_userName.send_keys(userName)      # 输入用户名
#         input_userPwd.send_keys(userPwd)        # 输入密码
#         btn_login.click()                       # 点击登录
# 
#         # 10秒内动态判断span_errorMsg按钮是否出现
#         try:
#             span_errorMsg = WebDriverWait(self.driver, 10).until(lambda driver : driver.find_element_by_id(self.ID_SPAN_ERROR_MSG))
#         except TimeoutException:
#             print "FAIL: Cannot display failed login message!"
#             return False
#         else:
#             print "PASS: The message of failed login is: " + span_errorMsg.text
#             return True

    @catchException()
    def computeDeltaDay(self, start_time, end_time):
        strp_start_time = time.strptime(start_time, "%Y/%m/%d %H:%M:%S")
        start_year = int(time.strftime('%Y', strp_start_time))
        start_mounth = int(time.strftime('%m', strp_start_time))
        start_day = int(time.strftime('%d', strp_start_time))
        strp_end_time = time.strptime(end_time, "%Y/%m/%d %H:%M:%S")
        end_year = int(time.strftime('%Y', strp_end_time))
        end_mounth = int(time.strftime('%m', strp_end_time))
        end_day = int(time.strftime('%d', strp_end_time))
        
        delta_day = datetime(end_year, end_mounth, end_day) - datetime(start_year, start_mounth, start_day)
        return delta_day.days

if __name__ == '__main__':
    pass
