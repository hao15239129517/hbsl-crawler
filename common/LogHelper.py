# coding=utf-8
import sys
import logging
from logging.handlers import RotatingFileHandler
import datetime
import os

reload(sys)
sys.setdefaultencoding('utf-8')


class LogHelper():

    def __init__(self, name=''):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level=logging.INFO)

        logPath = os.path.join(
            os.path.split(sys.path[0])[0], 'log', str(datetime.date.today()))

        if not os.path.exists(logPath):
            os.makedirs(logPath)
        logPath = os.path.join(
            logPath, '%s.txt' % (str(datetime.date.today()) + name))

        handler = RotatingFileHandler(
            logPath, maxBytes=5 * 1024 * 1024, backupCount=10)
        handler.setLevel(level=logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] =>  %(message)s ')

        handler.setFormatter(formatter)
        # 日志重复打印问题  是因为每次都会添加一个handler，因此每次都会执行一下
        self.logger.handlers = []
        self.logger.addHandler(handler)

    def Log(self, msg):
        #         print(msg)
        self.logger.info(msg)
