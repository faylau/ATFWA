# -*- coding=utf-8 -*-
# Copyright (C), 2013-2014, China Standard Software Co., Ltd.

"""
测试框架的主入口及配置文件解析
类说明:
    无
函数说明:
    load_tests: 根据全局变量test_cases来装载测试用例
    initialize: 根据用例的配置文件，返回tc_list
    createTestCase: 根据配置文件名字，返回测试用例集的列表
    create_testcase_by_module: 根据测试用例模块的名字返回测试用例集
    get_log_level: 从GlobalConf文件中获取当前的log_level值
    load_global_config: 用dataload装载全局配置文件GlobalConf.xml
    get_project_dir: 获取本项目的绝对路径
    get_testcase_dir: 获取测试用例目录的绝对路径
    get_test_result_path: 获取结果文件存放的绝对路径
    executeTest: 执行测试用例
"""

__authors__ = [
    '"Fei Liu" <fei.liu@cs2c.com.cn>',
    '"Huicong Ding" <huicong.ding@cs2c.com.cn>',
]

__version__ = "V0.3"

__all__ = []

# ChangeLog:
# Version    Date            Desc                                Author
# ----------------------------------------------------------------------------------------
# V0.1       10/16/2013      初始版本                            LF
# V0.2       01/09/2014      增加用例的执行方式——全部、根据模块、BVT、冒烟和根据配置文件
#                                                                DHC
# V0.3       02/27/2014      ①增加根据模块执行用例方式
#                            ②继续抽象函数
#                            ③将测试结果同意放到testresult目录
#                            ④增加详细的函数和模块的说明文档
#                            ⑤修改测试结果命名，并统一放到result目录中
#                                                                DHC
# ----------------------------------------------------------------------------------------

import os
import sys
import re
import time

reload(sys)
sys.setdefaultencoding('utf-8')

def get_project_dir():
    '''
    @summary: 获取本项目的绝对路径
    '''
    cur_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.dirname(cur_path) + os.path.sep

project_path = get_project_dir()
if get_project_dir() not in sys.path:
    sys.path.append(get_project_dir())

from copy import deepcopy
from unittest import TestSuite
from unittest import TestLoader

from Utils.xmlprase import dataload
from Utils.HTMLTestRunner import HTMLTestRunner
from Utils.xmlprase import xmlutil

# sys.path.append(os.path.dirname((os.path.abspath(os.path.dirname(__file__)))))

tc_list = []  # 由xml文件解析出的配置文件中的信息
xu = xmlutil()
test_cases = []  # 本次测试要执行的testcase
# _log_level = None

def load_tests():
    '''
    @summary: 根据全局变量test_cases来装载测试用例
    @return: 返回测试套件
    '''
    suite = TestSuite()
    loader = TestLoader()
    # print loader.loadTestsFromName(u'TestCase.UserLogin.TC060201_TC060202_TC060204_WrongLogin')
    tests = loader.loadTestsFromNames(test_cases)
    suite.addTests(tests)
    return suite
#    for test_class in test_cases:
#        tests = loader.loadTestsFromNames(test_cases)
#        suite.addTests(tests)

def initialize(suite_name, type_='case'):
    '''
    @summary: 根据用例的配置文件，返回tc_list——一个测试用例集的列表
    @param:
        suite_name: 测试用例配置文件的名字
        type_: 通过用例或者模块返回列表，如果是模块，则会自动分析模块文件的用例
    @return: 全局变量tc_list
    '''
    global tc_list
    abs_path = os.path.abspath(os.path.dirname(__file__)) + os.path.sep + suite_name
    if not os.path.exists(abs_path):
        print "Test suite %s is not exist!" % abs_path
        exit(0)
    xu.load(abs_path)
    if type_ == 'case':
        tc_list = xu.getTestCaseNodes()
    elif type_ == 'module':
        tc_list = xu.get_module_nodes()
    
def createTestCase(suite_name):
    '''
    @summary: 根据配置文件名字，返回测试用例集的列表
    @param:
        suite_name: 用例配置文件名字
    @return: 全局变量test_cases 
    '''
    for tc in tc_list:
        if tc["run"] != "True":
            continue
        abs_path = os.path.abspath(os.path.dirname(__file__)) + os.path.sep + suite_name
        xu.load(abs_path)
        oper_list = xu.getOperationNodes(tc)
    
        for oper in oper_list:
            clsname =  oper["modulename"] + "." + oper["classname"] 
    #       modname = oper["modulename"]
    #       module = __import__("TestCase"+"."+modname)
    #       cls_instance = getClass(clsname)
            test_cases.append("TestCase."+clsname)

def create_testcase_by_module():
    '''
    @summary: 根据tc_list全局变量的内容返回测试用例集列表
    @param: tc_list全局变量
    @return: 全局变量test_cases 
    '''
    
    # print tc_list
    for tc in tc_list:
        if tc['run'] == 'True':
            module_file_name = tc['filename']
            # testcase_file = get_testcase_dir() + module_file_name
            get_testcases_from_module(module_file_name)
        else:
            continue
    
def get_testcases_from_module(module_name):
    '''
    @summary: 根据测试用例模块的名字返回测试用例集
    @param module_name: 模块的名字
    @return: 全局变量test_cases
    '''
    module_path = get_testcase_dir() + module_name
    f = open(module_path)
    for line in f.readlines(): # 遍历每个用例的模块，找出所有的类的名字
        if re.match("^class", line) and "(BaseTestCase)" in line:
            test_cases.append("TestCase.%s.%s" % (module_name[:-3], line[6:-16]))
    f.close()  

_log_level = None
def get_log_level():
    '''
    @summary: 从GlobalConf文件中获取当前的log_level值
    '''
    global _log_level
    
    if _log_level is None:
        dict_data = load_global_config()
        _log_level = int(dict_data['globalconf']['loglevel']['value'])
    # print _log_level
    return _log_level

def load_global_config(): 
    '''
    @summary: 用dataload装载全局配置文件GlobalConf.xml
    @return: 全局配置信息的字典
    '''
    global_config_file = get_project_dir() + "TestRun" + os.path.sep + "GlobalConf.xml"
    data_load = dataload(global_config_file)
    return data_load.load()


def get_testcase_dir():
    '''
    @summary: 获取测试用例目录的绝对路径
    '''
    return get_project_dir() + "TestCase" + os.path.sep

def get_test_result_path():
    '''
    @summary: 获取结果文件存放的绝对路径
    '''
    cur_time = time.localtime(time.time())
    format_time = time.strftime('%Y-%m-%d_%H%M%S', cur_time)
    return get_project_dir() + 'result' + os.path.sep + format_time +\
        '_' + get_exec_type() + '_' + str(len(test_cases)) + '.html'

def get_exec_type():
    '''
    @summary: 获取当前的执行方式
    '''
    dict_data = load_global_config()
    return dict_data['globalconf']['exec_type']['value']
    
def exectueTest():
    '''
    @summary: 执行测试用例
    @param test_cases: 测试用例集的列表 
    '''
    global test_cases
    # global _log_level
    
    # btc = BaseTestCase()
    # dict_data = btc.initData()
    # dict_data = load_global_config()
    exec_type = get_exec_type()
    # _log_level = dict_data['globalconf']['loglevel']['value']
    
    if exec_type == 'all':
        # print test_cases
        # curPath = os.path.abspath(os.path.dirname(__file__))
        test_case_dir = get_testcase_dir()
        all_case_file = os.listdir(test_case_dir)
        all_case_module = deepcopy(all_case_file) # 遍历TestCase目录
        #print all_case_module
        for case_file in all_case_file:
            if ".pyc" in case_file:
                all_case_module.remove(case_file)
        all_case_module.remove("__init__.py")
        all_case_module.remove("Base.py")
        all_case_module.remove("SmokeTesting.py")

        for module in all_case_module:
            get_testcases_from_module(module)
        
    elif exec_type == 'module':
        suite_name = 'ModuleConf.xml'
        initialize(suite_name, 'module')
        create_testcase_by_module()
    
    elif exec_type == 'autotest':
        suite_name = 'autotest.xml'
        initialize(suite_name)
        createTestCase(suite_name)
    
    elif exec_type == 'config':
        suite_name = "BasicSuite.xml"
        initialize(suite_name)
        createTestCase(suite_name)
        
    elif exec_type == 'bvt':
        suite_name = "BVTSuite.xml"
        initialize(suite_name)
        createTestCase(suite_name)
    
    elif exec_type == 'smoke':
        test_cases = ["TestCase.SmokeTesting.SmokeTesting"]
        
    else:
        print "Can't identify the execute type, existing..."
        
    print 'There is(are) %d testcase(s) to execute:' % len(test_cases)
    print test_cases
       
    testSuite = load_tests() 
                
    # fileName = r"D:\result.html"   #美英 2013-11-21 增加r
    result_file = get_test_result_path()
    fp = file(result_file, 'wb')
    runner = HTMLTestRunner(
        stream=fp, 
        title=u"自动化测试报告",
        description=(
            u"中标麒麟安全云web管理平台自动化测试报告\n"
            u'测试执行方式：%s' % exec_type
        )
    )
    runner.run(testSuite)

if __name__ == "__main__":
    exectueTest()
