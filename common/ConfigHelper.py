# coding=utf-8
import sys
import codecs
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf-8')


class ConfigHelper():

    @staticmethod
    def Get(path, section, name):
        config = ConfigParser.ConfigParser()
        config.readfp(codecs.open(path, "r", "utf-8-sig"))
        return config.get(section, name)
