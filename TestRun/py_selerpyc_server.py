#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mellon
# @Date:   2014-03-07 16:02:20
# @Last Modified by:   mellon
# @Last Modified time: 2014-03-21 15:46:28

import os
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12450

from subprocess import PIPE, Popen
from rpyc import Service
from rpyc.utils.server import ThreadedServer


def now():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


class RpycServer(Service):
    """
    all remote functions should be defined as exposed_*
    """

    def exposed_getlog(self):
        """
        return the newest log file in directory "..\result\"
        """
        result_logs = sorted(os.listdir('..\\result'))
        # result of autotest should be named as ***_autotest_*
        log_name = ''
        for log in result_logs:
			# the latest log is the last one
            if 'autotest' in log:
                log_name = log
				
        if log_name:
            print "%s getlog: %s" % (now(), log_name)
            with open('..\\result\\' + log_name, 'r') as f:
                data = f.read()
                f.close()
            return data
        else:
            return False

    def exposed_test(self, num):
        print "%s test: %s" % (now(), num)
        return 520 + num

    def exposed_sendtext(self, file_name,  data):
        print "%s sendtext: %s" % (now(), file_name)
        with open(file_name, 'w') as f:
            f.write(data)
            f.close()
        return True

    def exposed_execcommand(self, command):
        print "%s exec command: %s" % (now(), command)
        job = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        res = job.stdout.read().strip()
        # print res
        return res

    def exposed_gettext(self, file_name):
        print "%s gettext: %s" % (now(), file_name)
        with open(file_name, 'r') as f:
            data = f.read()
            f.close()
        return data


sr = ThreadedServer(RpycServer, port=SERVER_PORT)
sr.start()
