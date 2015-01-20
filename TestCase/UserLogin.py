# -*- coding=utf-8 -*-
# Copyright (C), 2013, China Standard Software Co., Ltd.

'''
用户的用例模块。
类说明:
    TC060201_TC060202_TC060204_WrongLogin: 包含三个用例：
                06-02-01-用户名为空，无法登录web管理平台
                06-02-02-密码为空，无法登录web管理平台
                06-02-04-用户名或密码或验证码错误，无法登录web管理平台
方法说明:
    各个类中的方法都是相应用例的执行方法
'''
#from test.lock_tests import BaseTestCase

__authors__ = [
  '"Huicong Ding" <huicong.ding@cs2c.com.cn>'
]

__version__ = "V0.1"

# ChangeLog:
# Version    Date            Desc                Author
#--------------------------------------------------------
# V0.1       12/18/2013      初始版本            DHC 
#--------------------------------------------------------

import time
import sys

from selenium.common.exceptions import ElementNotVisibleException

from Base import BaseTestCase
from PageObject.LoginPage import LoginPage
from Utils.PublicMethod import printLog, getVersion
      
class TC060201_TC060202_TC060204_WrongLogin(BaseTestCase):
    '''
    @summary: 
        06-02-01-用户名为空，无法登录web管理平台
        06-02-02-密码为空，无法登录web管理平台
        06-02-04-用户名或密码或验证码错误，无法登录web管理平台
    @attention: 包括了三个用例的执行
    '''
    #===========================================================================
    # 06-02-01-用户名为空，无法登录web管理平台：
    # 前提：
    # 1.成功进入web管理平台登录界面。
    # 操作步骤：
    # 1.在登录界面输入任意密码和正确的验证码，用户名为空，点击【登录】按钮。
    # 预期结果：
    # 1.无法登录管理平台，错误提示合理正确。
    #
    # 06-02-02-密码为空，无法登录web管理平台：
    # 前提：1.已存在用户test。
    # 操作步骤：
    # 1.在登录界面输入用户名test，密码为空，点击【登录】按钮。
    # 预期结果：
    # 1.显示错误提示：密码不能为空，请输入您的密码。
    #
    # 06-02-04-用户名或密码或验证码错误，无法登录web管理平台
    # 操作步骤：
    # 1.在登录界面输入正确的用户名、错误的密码和正确的验证码，点击【登录】按钮；
    # 2.输入错误的用户名、密码和正确的验证码，点击【登录】按钮；
    # 3.输入任意用户名，输入任意密码和错误的验证码，点击【登录】按钮。
    # ******************************步骤3还无法实现****************************
    # 说明：在验证码正确的基础上首先检查用户是否存在，其次检查密码是否正确。
    # 1.不能登录管理平台，显示错误提示：密码错误，请重新输入；
    # 2.不能登录管理平台，显示错误提示：“您输入的用户名不存在，请重新输入”；
    # 3.不能登录管理平台，显示错误提示：验证码输入不正确，请重新输入，如看不清可点击验证码图片进行更换。
    #===========================================================================
    
    def test_WrongLogin(self):
        @BaseTestCase.drive_data(self)
        def do_test(data):
            user_name = data['username']['value'].strip()
            password = data['password']['value'].strip()
            expect_result = data['expectresult']['value'].strip()
            
            lp = LoginPage(self.driver)
            lp.setUserName(user_name)
            lp.setPassword(password)
            lp.setVerificationCode()
            lp.clickLoginButton()
            time.sleep(1)
            reality_result = lp.getFailedLoginMessage()
            # print expect_result, reality_result
            printLog("The current message for login error is '%s.'" % (reality_result))
                    
            if expect_result in reality_result:
                # self.result = True
                printLog("The message for login via user: %s & password: %s is right." % (user_name, password), "pass")
                # self.assertTrue(self.result)
            else:
                # self.result = False
                # printLog("The message for login via user: %s & password: %s is wrong!!!" % (user_name, password), "fail")
                self.setResultFasle(
                    "The message for login via user: %s & password: %s is wrong!!!" % 
                    (user_name, password)
                )
                        
            # self.assertTrue(self.result)
        
        do_test()
        
if __name__ == "__main__":
    pass
