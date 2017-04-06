# coding=utf-8
import sys
import urllib
import re
import os
import time
import traceback
import win32serviceutil
import win32service
import win32event
import datetime

import bs4
from apscheduler.schedulers.blocking import BlockingScheduler

sys.path.append(os.path.split(sys.path[0])[0])
from common.ConfigHelper import ConfigHelper
from common.LogHelper import LogHelper
from common.DbHelper import DbHelper
from common.EmailHelper import SendEmail
reload(sys)
sys.setdefaultencoding('utf-8')

log = LogHelper()


def sendLogJob():
    try:
        SendEmail.Send(os.path.join(sys.path[0], 'config.ini'), '每天的日志文件', os.path.join(os.path.split(
            sys.path[0])[0], 'log', '%s.txt' % (datetime.timedelta(days=-1) +
                                                datetime.datetime.now()).date()))
    except:
        log.Log(traceback.format_exc())

# 新闻抓取


def crawlerJob():
    sys.setrecursionlimit(1000000000)
    page = 1
    configPath = os.path.join(sys.path[0], 'config.ini')
    totalPape = ConfigHelper.Get(
        configPath, 'base', 'totalPage')
    dbHelper = DbHelper(configPath, 'News')
    log.Log(
        '-------------------------crawlerJob start-------------------------')
    while page <= int(totalPape):
        if page != 1:
            url = 'http://www5.ncwu.edu.cn/channels/4_%s.html' % page
        else:
            url = 'http://www5.ncwu.edu.cn/channels/4.html'
        html = urllib.urlopen(url)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        if soup == None:
            log.Log('%s没有获取到列表页html文档内容：%s' %
                    (sys._getframe().f_code.co_name, url))
            continue
        div = soup.find('div', class_='xinxilist')
        ul = div.find('ul')
        for li in ul.find_all('li'):
            href = li.find('a')['href']
            date = li.find('i').get_text()
            id = re.search(r'(\d+).html', href).groups(1)[0]
            title = li.find('a').get_text()
            try:
                time.sleep(1)
                html = urllib.urlopen(href)
                contentHtml = bs4.BeautifulSoup(html.read(), 'html.parser')
            except:
                log.Log(
                    traceback.format_exc() + '====%s获取内容页HTML文档内容异常：%s' % (sys._getframe().f_code.co_name, href))
                continue

            if contentHtml == None:
                log.Log('%s没有获取到内容页HTML文档内容：%s' %
                        (sys._getframe().f_code.co_name, href))
                continue
            content = contentHtml.find('div', attrs={'align': 'left'})
            if content == None:
                log.Log(
                    '%s没有获取到内容页div{align: left}内容：%s' % (sys._getframe().f_code.co_name, href))
                continue
            content = content.find_parent('div', attrs={'align': 'center'})

            if content == None:
                log.Log('%s没有获取到内容页div{align: center}内容：%s' % (
                    sys._getframe().f_code.co_name, href))
                continue

            try:
                res = dbHelper.Select(id)
                if res.fetchone() == None:
                    dbHelper.Add([{'articleid': id.strip(), 'href': href.strip(), 'Title': title.strip(
                    ), 'date': date.strip(), 'NeiRong': content.prettify(), 'LeiXing': 0, 'UserID': 1}])
                else:
                    continue
            except Exception:
                log.Log(
                    traceback.format_exc() + '====%s数据库操作异常：%s' % (sys._getframe().f_code.co_name, href))
                # 应该是重试
        log.Log('%s的-----------------------page=%s---------------------' %
                (sys._getframe().f_code.co_name, page))
        page += 1

    LogHelper.Log(
        'crawlerJob-------------------------ok------------------------------- page=%s' % page, False)

# 公告抓取


def crawlerNoticeJob():
    sys.setrecursionlimit(1000000000)
    page = 1
    configPath = os.path.join(sys.path[0], 'config.ini')
    totalPape = ConfigHelper.Get(
        configPath, 'base', 'totalPage')
    dbHelper = DbHelper(configPath, 'News')
    log.Log(
        '-------------------------crawlerNoticeJob start-------------------------')
    while page <= int(totalPape):
        if page != 1:
            url = 'http://www5.ncwu.edu.cn/channels/5_%s.html' % page
        else:
            url = 'http://www5.ncwu.edu.cn/channels/5.html'
        html = urllib.urlopen(url)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        if soup == None:
            log.Log('%s没有获取到列表页html文档内容：%s' %
                    (sys._getframe().f_code.co_name, url))
            continue
        div = soup.find('div', class_='tzlist')
        ul = div.find('ul')
        for li in ul.find_all('li'):
            href = li.find('a', attrs={'target': '_blank'})['href']
            date = li.find('i').get_text()
            id = re.search(r'(\d+).html', href).groups(1)[0]
            title = li.find('a', attrs={'target': '_blank'}).find(
                'span').get_text()
            try:
                time.sleep(1)
                html = urllib.urlopen(href)
                contentHtml = bs4.BeautifulSoup(html.read(), 'html.parser')
            except:
                log.Log(
                    traceback.format_exc() + '====%s获取内容页HTML文档内容异常：%s' % (sys._getframe().f_code.co_name, href))
                continue

            if contentHtml == None:
                log.Log('%s没有获取到内容页HTML文档内容：%s' %
                        (sys._getframe().f_code.co_name, href))
                continue
            content = contentHtml.find('div', attrs={'class': 'xinxi_con'})
            if content == None:
                log.Log('%s没有获取到内容页div{class: xinxi_con}内容：%s' % (
                    sys._getframe().f_code.co_name, href))
                continue

            try:
                resNotice = dbHelper.Select(id)
                if resNotice.fetchone() == None:
                    dbHelper.Add([{'articleid': id.strip(), 'href': href.strip(), 'Title': title.strip(
                    ), 'date': date.strip(), 'NeiRong': content.prettify(), 'LeiXing': 1, 'UserID': 1}])
                else:
                    continue
            except Exception:
                log.Log(
                    traceback.format_exc() + '====%s数据库操作异常：%s' % (sys._getframe().f_code.co_name, href))
                # 应该是重试
        log.Log('%s的-----------------------page=%s---------------------' %
                (sys._getframe().f_code.co_name, page))
        page += 1

    LogHelper.Log(
        'crawlerNoticeJob-------------------------ok------------------------------- page=%s' % page, False)


class CrawlerService(win32serviceutil.ServiceFramework):

    # 服务名
    _svc_name_ = "CrawlerService"
    # 服务显示名称
    _svc_display_name_ = "CrawlerService"
    # 服务描述
    _svc_description_ = "CrawlerService description"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.scheduler = BlockingScheduler(logger=None)
        log.Log('.......job init..........')
        self.scheduler.add_job(crawlerJob, 'cron', hour=ConfigHelper.Get(os.path.join(sys.path[
                               0], 'config.ini'), 'quartz', 'hour'), minute=ConfigHelper.Get(os.path.join(sys.path[0], 'config.ini'), 'quartz', 'minute'))
        self.scheduler.add_job(crawlerNoticeJob, 'cron', hour=ConfigHelper.Get(os.path.join(sys.path[
                               0], 'config.ini'), 'quartz', 'hour'), minute=ConfigHelper.Get(os.path.join(sys.path[0], 'config.ini'), 'quartz', 'minute'))
#         self.scheduler.add_job(sendLogJob, 'cron', hour=ConfigHelper.Get(os.path.join(sys.path[
# 0], 'config.ini'), 'email', 'hour'),
# minute=ConfigHelper.Get(os.path.join(sys.path[0], 'config.ini'),
# 'email', 'minute'))

    def SvcDoRun(self):
        while True:  # 要加while循环 否则服务只能运行1次 启动服务时有提示
            if win32event.WaitForSingleObject(self.hWaitStop, 5000) == win32event.WAIT_OBJECT_0:
                # 当stop的时候 会再次触发进入到 while里面  这时会break
                break
            if not self.scheduler.running:
                log.Log('.......job start..........')
                # 此时程序 会停到这里 此时的running是true 之前都是false
                self.scheduler.start()

    def SvcStop(self):
        # 先告诉SCM停止这个过程
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # 设置事件
        win32event.SetEvent(self.hWaitStop)
        # 停止 true表示执行完job再停止
        if self.scheduler.running:
            self.scheduler.shutdown(False)
        log.Log('.......job stop..........')

# 必须要加 否则会出现Python could not import the service's module 错误代码1
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(CrawlerService)
