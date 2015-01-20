#-*- coding=utf-8 -*-
'''
Created on 2012-10-16
@summary: The base class for all test case classes.
@author: fei.liu@cs2c.com.cn, huicong.ding@cs2c.com.cn
@version: v0.4
'''

# ChangeLog:
# Version    Date            Desc                Author
# --------------------------------------------------------
# V0.1       10/16/2013      初始版本            LF
# V0.2       01/09/2014      ①数据文件根据test case模块分目录存储；
#                            ②增加全局数据和模块级数据；
#                            ③修改配置文件，默认启动Firefox关闭每日提醒
#                                                DHC
# V0.3       02/27/2014      ①优化tearDownClass，智能退出
#                            ②将setUpClass和tearDownClass改为setUp和tearDown，解决IP地址配置的问题
#                                                DHC
# V0.4       03/17/2014      实现数据驱动的装饰器
#                                                DHC
# --------------------------------------------------------

import os
import unittest

from selenium import webdriver

from Utils.xmlprase import dataload
from Utils.PublicMethod import printLog, execSshCmd
from TestRun.TestCenter import load_global_config
from PageObject.LoginPage import LoginPage

class BaseTestCase(unittest.TestCase):
    # @classmethod
    def setUp(self):
        # 设置firefox的profile文件，使其运行时默认的语言为中文
        profile = webdriver.FirefoxProfile()
        profile.set_preference("intl.accept_languages", "zh-cn, zh, en-us, en")
        profile.set_preference("extensions.addonnotification.showDaytip", "false") # 关闭浏览器的每日提醒
        profile.set_preference("account@mozillaonline.com.autoPopNum", "0")  # 关闭火狐通行证登录提醒
        # 初始化WebDriver实例对象，并指定要打开的主页地址
        self.driver = webdriver.Firefox(profile)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        # dict_data = self.initData()
        # ip = dict_data['globalconf']['ip']['value']
        # 此处无法调用initData方法，否则htmltestrunner的buffer会溢出
        
        # xml = xmlutil()
        # xml.load(self.global_config_file)
        # ip = xml.get_frontend_ip()
        # ip = get_global_config()
        # print ip
        dict_data = load_global_config()
        
        self.driver.get('http://' + dict_data['globalconf']['ip']['value'] + '/')
        
    def initData(self):
        '''
        @summary: 为用例初始化测试数据集；
        @param : 无
        @return: 返回一个测试数据集data；
        '''
        curPath = os.path.abspath(os.path.dirname(__file__))
        # module_name = os.path.realpath(sys.argv[0]).split(os.path.sep)[-1][:-3]
        module_name = str(self.__module__).split(".")[-1]
        test_case = str(self.__class__.__name__)
        dataPath = os.path.dirname(curPath) + os.path.sep + "Data" + os.path.sep + module_name
        dataFilePath = dataPath + os.path.sep + test_case + ".xml"
        # print dataFilePath
        if os.path.exists(dataFilePath):
            dl = dataload(dataFilePath)
#            self.data = dl.load()
            private_dict_data = dl.load()
        else:
            printLog("The TestCase <" + test_case + "> has no data file.", "warn")
            private_dict_data = {}
            
        # 读取模块通用测试数据文件
        module_data = dataPath + '.xml'
        if os.path.exists(module_data):
            module_dict_data = dataload(module_data).load()
        else:
            printLog("The TestCase <%s> has no module data file." % test_case, "Warn")
            module_dict_data = {}
        
        # 读取全局配置文件
#         global_config_file = os.path.dirname(curPath) + os.path.sep + "TestRun" + os.path.sep + "globalConf.xml"
#         data_load = dataload(global_config_file)
#         global_dict_data = data_load.load()
        
        global_dict_data = load_global_config()
        dict_data = dict(dict(private_dict_data, **module_dict_data), **global_dict_data)
        
        # 获取当前IP地址和hostname
        # url = self.driver.current_url
        #print url
        ip = load_global_config()['globalconf']['ip']['value']
        # dict_data['globalconf']['ip']['value'] = ip
        host_name = execSshCmd(ip, ['hostname'], dict_data["globalconf"]['ssh_username']['value'], dict_data['globalconf']['ssh_password']['value'])
        dict_data['globalconf']['hostname']['value'] = host_name
        
        return dict_data

    # @classmethod
    def tearDown(self):
        if 'logout.action' in self.driver.current_url:
            pass
        else:
            lp = LoginPage(self.driver)
            if lp.getUserName():
                lp.logout()
            
        self.driver.quit()
    
    def setTestResult(self, result='pass', message='No more message.'):
        if result.lower() == 'pass':
            printLog("Test case has been executed successfully, here is the message: %s" % message, 'pass')
            # self.assertTrue(True, "True")
        elif result.lower() == 'fail':
            printLog(message)
            raise self.failureException("Test case execute failed, here is the message: %s" % message)
        else:
            printLog("The test result should be 'pass' or 'fail', your input is not supported.", "error")
            return False
        
    def setResultFasle(self, message):
        return self.setTestResult('fail', message)

    def drive_data(self):
        '''
        @summary: 数据驱动用例使用的装饰器
        @param:
            f: function
        @bug: 还未找到装饰器调用函数时，传递给函数参数的方法
        '''
        def _call(f):
            def __call():
                # return_ = []
                dict_data = self.initData()
                for key in dict_data['case']['datadrive']:
                    if key != 'value':
                        data = dict_data['case']['datadrive'][key]
                        return_ = f(data)
                        # return_.append(f(data))
                return return_
            return __call
        return _call
            
if __name__ == "__main__":
    
    unittest.main()
