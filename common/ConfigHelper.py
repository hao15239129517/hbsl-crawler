# coding=utf-8
import sys
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf-8')


class ConfigHelper():

    @staticmethod
    def Get(path, section, name):
        config = ConfigParser.ConfigParser()
        config.read(path)
        return config.get(section, name)
