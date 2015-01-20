# -*- coding=utf-8 -*-
# Copyright (C), 2013, China Standard Software Co., Ltd.

"""
公用函数、方法模块
类说明:
    无
函数说明:
    printLog: 打印日志信息
    getCurInfo: 获取当前执行函数的名字和行号
    execSshCmd: 在远端Linux主机上执行Shell命令
    switchToWindow: 切换到窗口
    getVersion: 获取当前版本的版本号（根据neo version命令）
    catchException: 简单的异常处理
"""

__authors__ = [
  '"Huicong Ding" <huicong.ding@cs2c.com.cn>',
]
__version__ = "V0.4"

# ChangeLog:
# Version    Date            Desc                Author
#--------------------------------------------------------
# V0.1       06/17/2013      初始版本            DHC
# V0.2       12/04/2013      增加SSH远程执行命令的方法
#                                                DHC
# V0.3       12/06/2013      打印信息改为英文    DHC
# V0.4       03/17/2014      完成retry装饰器     DHC
#--------------------------------------------------------

import sys
import os
import paramiko

from datetime import datetime
from traceback import print_exc

from xmlprase import xmlutil

from TestRun.TestCenter import get_log_level
#from TestCase.Base import BaseTestCase

# from selenium.webdriver.support.color import Col
# __LOG_LEVEL = 

def printLog(log, message_type="mess"):
    global log_level
    '''
    消息类型(不区分大小写):
        Mess: 普通消息
        Warn: 警告消息
        Error: 错误消息
        Pass: 用例通过消息
        Fail: 用例失败消息
        Debug: Debug信息
    '''
    log_dict = {
        "mess":  "-MESSAGE-",
        "warn":  "-WARNING-",
        "error": "--ERROR--",
        "pass":  "--PASS---",
        "fail":  "--FAIL---",
        "debug": "--DEBUG--",
    }
    
#     curPath = os.path.abspath(os.path.dirname(__file__))
#     global_config_file = os.path.dirname(curPath) + os.path.sep + "TestRun" + os.path.sep + "GlobleConf.xml"
#     xml = xmlutil()
#     xml.load(global_config_file)
#     try:
#         log_level = int(xml.get_log_level())
#     except ValueError: 
#         print >> sys.stderr, "Only number is supported!"
#         return False
    
    # print log_level
    log_level = get_log_level()
    
    if (log_level == 0 or
            (log_level == 1 and message_type.lower() != "debug") or
            (log_level == 2 and message_type.lower() in ("error", "fail", "warn"))):
        try:
            display_level = log_dict[message_type.lower()]
        except:
            printLog("You can't use this method by %s" % (message_type), "Error")
        else:
            _print_log(log, display_level)
            return True
    elif log_level > 2 or log_level < 0:
        print >> sys.stderr, "Unsupported log level!"
    else:
        return False
        
        
            
def _print_log(log, level):
    now = datetime.now()
    if level in ("--ERROR--", "--FAIL---"):
        print >> sys.stderr, "[%s %s ]: %s" \
                % (str(now.strftime("%Y-%m-%d %H:%M:%S")), level, log)
    else:
        try:
            print "[" + str(now.strftime("%Y-%m-%d %H:%M:%S")) + " " + level + " ]: %s" % (log)
        except:
            printLog("You can't use this method by %s" % (level), "Error")
    


def getCurInfo():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
    return (f.f_code.co_name, f.f_lineno)


def execSshCmd(ip, cmd, user='root', password='neokylin123'):
    '''
    @summary: 使用SSH连接远端主机执行Shell命令（脚本）
    @param: 
        ip: 远端主机的IP地址
        user: SSH登录用户名，默认是root
        password: SSH登录密码，默认是neokylin123
        cmd: 需执行的命令，请传入列表或者元组，序列成员的相对位置决定命令的执行顺序
    @return: 
        执行成功输出执行结果并返回每个命令执行结果的列表，每个列表元素仍是一个列表，如：
            ls 返回 [['anaconda-ks.cfg\n', 'buildInfo\n', 'debuginfo_install', ...]]
            得到字符串需两次索引
        执行失败返回False
    @attention: 尽量避免使用中文，可能有编码问题！
    '''
    output = []
    try:
        ssh = paramiko.SSHClient()  # 创建SSH实例
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 设置添加主机公钥策略为自动添加
        ssh.connect(ip, 22, user, password, timeout=5)
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            # stdin.write("Y")   #简单交互，输入 ‘Y’
            output_mess = stdout.readlines() + stderr.readlines()
            printLog("The output of command '%s' is '%s'." % (m, output_mess), 'debug') 
            output.append(output_mess)
        printLog('"%s"的命令"%s"执行成功。' % (ip, cmd), 'debug')
        ssh.close()
        return output
    except:
        e = sys.exc_info()[0]
        printLog('The command on "%s"("%s") is failed! Reason: %s' % (ip, cmd, e), "Error")
        return False
        
def __switchToWindow(driver, driver_handle):
    '''
    暂时不用
    @param driver:
    @param driver_handle:
    '''
    #print driver.current_window_handle, driver_handle
    if driver.current_window_handle == driver_handle:
        printLog("You don't have to switch to yourself.", "Warn")
    else:
        printLog("Switching to windows %s" % driver_handle)
        driver.switch_to_window(driver_handle)
        
def getVersion(front_end_ip, front_end_user='root', front_end_password='neokylin123'):
    web_version = execSshCmd(
        front_end_ip,
        ["/srv/cloud/neo/bin/neo version | grep web | grep -v Version"], 
        front_end_user, 
        front_end_password
    )
    if web_version:
        version = web_version[0][0].split('-')
        return str(version[-2]) + '.' + str(version[-1])
    else:
        printLog("Failed to get version from back end!", "Error")
        return False

def catchException(message=None):
    '''
    @summary: 异常处理的装饰器
    @param: 
        message: 需要打印的信息
        f: function
    '''
    def _call(f):
        def __call(*args, **kwds):
            try:
                data = f(*args, **kwds)
            except Exception as e:
                printLog(message if message else
                         "There is something wrong in your method(function) %s, here is some messages:" % 
                         f.__name__, 
                         "error")
                print_exc()
                return e.args
            else:
                return data
        return __call
    return _call

def retry(retry_times=3):
    '''
    @summary: 重试的装饰器
    @param f: 需要重试的函数（方法）
    @param retry_times: 重试次数，默认是3次
    '''
    def _call(f):
        def __call(*args, **kwarg):
            for i in range(retry_times + 1):  # 循环因子是“重试次数”，第一次不算重试，所以+1
                if i:
                    printLog(
                        'Retry function: %s, retry times: %d.' % (f.__name__, i),
                        'debug'
                    )
                return_value = f(*args, **kwarg)
                if return_value:
                    break
            else:
                printLog(
                    'Function(Method) %s executed failed after %d times retries.' % 
                    (f.__name__, retry_times), 
                    'error'
                )
            return return_value
        return __call
    return _call

if __name__ == '__main__':
    # ExecSshCmd("10.1.60.154", "ls /root/", password='qwer1234')
    #getImg('http://10.1.80.222/release/Template/v2.4/build06/20131206/', '10.1.60.180')
    #print getVersion("10.1.65.1", front_end_password="qwer1234")
    print printLog("end", 'error')

