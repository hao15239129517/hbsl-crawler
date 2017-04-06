# coding=utf-8
import sys
import logging
from logging.handlers import RotatingFileHandler
import datetime
import os

reload(sys)
sys.setdefaultencoding('utf-8')


class LogHelper():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.INFO)

        logPath = os.path.join(os.path.split(sys.path[0])[0], 'log')

        if not os.path.exists(logPath):
            os.makedirs(logPath)

        logPath = os.path.join(logPath, '%s.txt' % datetime.date.today())

        handler = RotatingFileHandler(
            logPath, maxBytes=5 * 1024 * 1024, backupCount=10)
        handler.setLevel(level=logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] => %(message)s ')

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def Log(self, msg):
        print(msg)
        self.logger.info(msg)
