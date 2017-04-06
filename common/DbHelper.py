# coding=utf-8
import sys
import urllib
from ConfigHelper import ConfigHelper

import sqlalchemy
from sqlalchemy.sql import select
from msilib import Table
reload(sys)
sys.setdefaultencoding('utf-8')


class DbHelper():

    def __init__(self, configPath, table):
        self.server = ConfigHelper.Get(configPath, 'db', 'server')
        self.uid = ConfigHelper.Get(configPath, 'db', 'uid')
        self.pwd = ConfigHelper.Get(configPath, 'db', 'pwd')
        self.database = ConfigHelper.Get(configPath, 'db', 'database')
        self. params = urllib.quote_plus(
            "DRIVER={SQL Server Native Client 10.0};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (self.server, self.database, self.uid, self.pwd))
        self.engine = sqlalchemy.create_engine(
            "mssql+pyodbc:///?odbc_connect=%s" % self.params)

        self.metaData = sqlalchemy.MetaData(bind=self.engine)
        self.table = sqlalchemy.Table(table, self.metaData, autoload=True)

    def Add(self, data):
        try:

            conn = self.engine.connect()
            res = conn.execute(self.table.insert().return_defaults(), data)
            return res.returned_defaults
        except Exception:
            raise Exception
        finally:
            res.close()

    def Delete(self, where):
        try:
            conn = self.engine.connect()
            # 列名  有大小写区分
            res = conn.execute(
                self.table.delete().where(self.table.c.articleid == where).returning(self.table.c.articleid))
#             返回一个元祖
            return res
        except Exception:
            raise Exception

    def Select(self, where):
        try:
            conn = self.engine.connect()
            res = conn.execute(
                self.table.select().where(self.table.c.articleid == where))
#             返回一个元祖
            return res
        except Exception:
            raise Exception
