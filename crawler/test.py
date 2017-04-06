# coding=utf-8
import sys
import os
import traceback
import datetime
import urllib
import logging
from logging.handlers import RotatingFileHandler
import bs4
from apscheduler.schedulers.blocking import BlockingScheduler

import common.DbHelper
from common.ConfigHelper import ConfigHelper
from common.LogHelper import LogHelper
from common.EmailHelper import SendEmail
'''
要在调用setdefaultencoding时必须要先reload一次sys模块，因为这里的import语句其实并不是sys的第一次导入语句，也就是说这里其实可能是第二、三次进行sys模块的import，这里只是一个对sys的引用，只能reload才能进行重新加载。

那么为什么要重新加载，而直接引用过来则不能调用该函数呢？因为setdefaultencoding函数在被系统调用后被删除了，所以通过import引用进来时其实已经没有了，所以必须reload一次sys模块，这样setdefaultencoding才会为可用，才能在代码里修改解释器当前的字符编码。

在Python安装目录的Lib文件夹下，有一个叫site.py的文件，在里面可以找到main() --> setencoding()-->sys.setdefaultencoding(encoding),因为这个site.py每次启动python解释器时会自动加载，所以main函数每次都会被执行，setdefaultencoding函数一出来就已经被删除了。
'''
reload(sys)
sys.setdefaultencoding('utf-8')
# '%s.txt' % datetime.date.today()

html = urllib.urlopen('http://www5.ncwu.edu.cn/contents/13/39646.html')
soup = bs4.BeautifulSoup(html, 'html.parser')
content = soup.find('div', attrs={'class': 'xinxi_con'})
i = 0
log = LogHelper()
print('是的范德萨')


# class Log():
#
#     log = logging.getLogger('ll')
#     log.setLevel(level=logging.INFO)
#
#     @staticmethod
#     def Log(msg):
#
#         logPath = os.path.join(os.path.split(sys.path[0])[0], 'log')
#
#         if not os.path.exists(logPath):
#             os.makedirs(logPath)
#
#         logPath = os.path.join(logPath, '%s.txt' % datetime.date.today())
#
#         handler = RotatingFileHandler(
#             logPath, maxBytes=5 * 1024 * 1024, backupCount=10)
#         handler.setLevel(level=logging.INFO)
#         formatter = logging.Formatter(
#             '[%(asctime)s] => %(message)s ')
#
#         handler.setFormatter(formatter)
#         log.addHandler(handler)
#         log.info(msg)
