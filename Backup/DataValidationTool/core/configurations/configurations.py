# Global Properties Load from properties folder
import os
from configparser import RawConfigParser

from DataValidationTool.core import configurations


def getInstance():
    configurations.getInstance()


class configurations:
    __instanceConfigurations: configurations = None
    __config: RawConfigParser = None

    @staticmethod
    def getInstance(filename: str = ""):
        if configurations.__instanceConfigurations is None:
            configurations(filename)
        if filename.strip() != "":
            configurations.readConfigDetailsFromFile(filename)
        return configurations.__instanceConfigurations

    @staticmethod
    def readConfigDetailsFromFile(baseFile=""):
        if os.path.exists(baseFile):
            configurations.__config.read(baseFile)

    def __init__(self, fileName=""):

        if configurations.__instanceConfigurations is not None:
            configurations.getInstance()
        else:
            configurations.__instanceConfigurations = self

        if configurations.__config is None:
            print("Config Initialized")
            configurations.__config = RawConfigParser()
            configurations.__config.sections()
        if fileName != "":
            print("Loading Information from " + fileName)
            configurations.__config.read(fileName)
        configurations.__instance = self

    # get Config data
    def getConfigSectionData(self, section):
        return configurations.__config.items(section)

    def getSections(self):
        return configurations.__config.sections()

    # get Config Property Value - if sectioned property use . to append it
    def getPropertyValue(self, section, propertyName):
        if configurations.__config.has_option(section, propertyName):
            return configurations.__config.get(section, propertyName)
        else:
            raise Exception("No Property found in section '" + section + "' with name '" + propertyName + "'")

    def getPropertyValueOrDefaultValue(self, section, propertyName, defaultValue):
        if configurations.__config.has_option(section, propertyName):
            return configurations.__config.get(section, propertyName)
        else:
            return defaultValue

    def addSection(self, section):
        if (not configurations.__config.has_section(section)):
            configurations.__config.add_section(section)

    def addValueToSection(self, section, key, value):
        if (configurations.__config.has_section(section)):
            configurations.__config.set(section, key, value)
        else:
            configurations.__config.add_section(section)
            configurations.__config.set(section, key, value)

    # print("Set Config Value - [" + section + "][" + key + "] = " + configurations.__config.get(section, key))

    def readBaseConfigurations(self, baseFile=""):
        if (os.path.exists(baseFile)):
            print("Setup Base Configurations for executions: " + str(baseFile))
            configurations.__config.read(baseFile)
        else:
            print("Setup Base Configurations for executions: default")
            self.__setDefaultBaseInfo()

    def __setDefaultBaseInfo(self):
        if not self.__config.has_section("default"):
            # [default]
            self.addSection("default")
            # ProjectName = Data Validation Tool
            self.addValueToSection("default", "ProjectName", "Data Validation Tool")
            # ProjectVersion = 1.2.0
            self.addValueToSection("default", "ProjectVersion", "1.2.0")
        if not self.__config.has_section("thread"):
            # [thread]
            self.addSection("thread")
            # MaxThreads = 6
            self.addValueToSection("thread", "MaxThreads", "6")
            # DataCapacity = 50
            self.addValueToSection("thread", "DataCapacity", "500")
        if not self.__config.has_section("queue"):
            # [queue]
            self.addSection("queue")
            # ququeSize = 5000
            self.addValueToSection("queue", "ququeSize", "5000")
            # queueWaitTime = 1
            self.addValueToSection("queue", "queueWaitTime", "1")
        if not self.__config.has_section("dataformats"):
            # [dataformats]
            self.addSection("dataformats")
            # string = CASE SENSITIVE
            self.addValueToSection("dataformats", "string", "CASE SENSITIVE")
            # float = {0: .2f}
            self.addValueToSection("dataformats", "float", "{0: .2f}")
            # datetime = % Y - % m - % d % H: % M: % S. % f
            self.addValueToSection("dataformats", "datetime", "%Y-%m-%d %H:%M:%S.%f")

    def updateConfigData(self, fileName: str = ""):
        if os.path.exists(fileName):
            configurations.__config.read(fileName)
        else:
            # Setup Source Keys
            configurations.__config.add_section("source")
            self.addValueToSection("source", "type", "")
            self.addValueToSection("source", "host", "")
            self.addValueToSection("source", "port", "")
            self.addValueToSection("source", "database", "")
            self.addValueToSection("source", "username", "")
            self.addValueToSection("source", "password", "")
            self.addValueToSection("source", "datakey", "")
            self.addValueToSection("source", "auth", "")
            self.addValueToSection("source", "filepath", "")
            # Setup Destination Keys
            configurations.__config.add_section("destination")
            self.addValueToSection("destination", "type", "")
            self.addValueToSection("destination", "host", "")
            self.addValueToSection("destination", "port", "")
            self.addValueToSection("destination", "database", "")
            self.addValueToSection("destination", "username", "")
            self.addValueToSection("destination", "password", "")
            self.addValueToSection("destination", "datakey", "")
            self.addValueToSection("destination", "auth", "")
            self.addValueToSection("destination", "filepath", "")
