# coding=utf-8
import sys
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ConfigHelper import ConfigHelper
reload(sys)
sys.setdefaultencoding('utf-8')


class SendEmail():

    @staticmethod
    def Send(configPath, content, attPath):
        f = ConfigHelper.Get(
            configPath, 'email', 'from')
        pwd = ConfigHelper.Get(
            configPath, 'email', 'pwd')
        t = ConfigHelper.Get(
            configPath, 'email', 'to')
        message = MIMEMultipart()
# 出现554 是因为from  to没有设置
        message['From'] = f
        message['To'] = t
        message['Subject'] = '爬虫邮件通知'

        # 构造附件
        if os.path.exists(attPath):
            for parent, dirnames, filenames in os.walk(attPath):
                if(len(filenames) == 0):
                    content += "  日志文件夹内日志文件不存在：%s" % attPath
                    break
                for file in filenames:
                    att1 = MIMEText(
                        open(os.path.join(parent, file), 'rb').read(), 'base64', 'utf-8')
                    att1["Content-Type"] = 'application/octet-stream'
                    att1[
                        "Content-Disposition"] = 'attachment; filename="%s"' % file
                    message.attach(att1)
        else:
            content += "  日志文件夹不存在：%s" % attPath
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        server = smtplib.SMTP('smtp.163.com', 25)
        server.login(f, pwd)
        server.sendmail(f, t, message.as_string())
        server.quit()
