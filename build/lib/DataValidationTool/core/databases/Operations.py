import platform
import pyodbc

import cx_Oracle
import pymongo
from pyhive import hive

from DataValidationTool.core.configurations.configurations import configurations
from DataValidationTool.core.databases import DatabaseTypes
from DataValidationTool.core.databases.DatabaseTypes import ConnectionType


def getRecords(dbconnection, sourceType: ConnectionType, query: str):
    if sourceType != ConnectionType.File:
        if sourceType == ConnectionType.MongoDB:
            db = dbconnection[(str(query).split("|")[0])]
            filters = {}
            if str(str(query).split("|")[1]).strip() != "":
                filters = dict((k.strip(), v.strip()) for k, v in (item.split(':') for item in str(query).split("|")[1]).split(','))
            cursor = db.find()
        else:
            cursor = dbconnection.cursor()
            print(query)
            cursor.execute(query)
        return cursor
    else:
        # if File Return as it is
        return dbconnection


def getConnection(sourceSectionName):
    try:
        configs = configurations.getInstance()
        connectionType = DatabaseTypes.getConnectionType(configs.getPropertyValue(sourceSectionName, "type"))
        if connectionType == ConnectionType.HadoopHive:
            conn = hive.Connection(host=configs.getPropertyValue(sourceSectionName, "host"), port=int(configs.getPropertyValue(sourceSectionName, "port")), username=configs.getPropertyValue(sourceSectionName, "username"),
                                   password=configs.getPropertyValue(sourceSectionName, "password"), auth=configs.getPropertyValue(sourceSectionName, "auth"), database=configs.getPropertyValue(sourceSectionName, "database"))
        elif connectionType == ConnectionType.Oracle:
            connstr = str(configs.getPropertyValue(sourceSectionName, "username")) + '/' + str(
                configs.getPropertyValue(sourceSectionName, "password")) + '@' + configs.getPropertyValue(
                sourceSectionName, "host") + ':' + configs.getPropertyValue(
                sourceSectionName, "port") + '/' + configs.getPropertyValue(sourceSectionName, "database")
            conn = cx_Oracle.connect(connstr)
        elif connectionType == ConnectionType.SQLServer:
            driverName = "SQL Server" if "windows" in platform.system().lower() else "ODBC Driver 17 for SQL Server"
            connstr = 'DRIVER={' + driverName + '};SERVER=' + str(configs.getPropertyValue(sourceSectionName, "host")) + ',' + str(configs.getPropertyValue(sourceSectionName, "port")) + ';DATABASE=' + str(
                configs.getPropertyValue(sourceSectionName, "database")) + ';UID=' + str(configs.getPropertyValue(sourceSectionName, "username")) + ';PWD=' + str(configs.getPropertyValue(sourceSectionName, "password")) + ''
            conn = pyodbc.connect(connstr)
        elif connectionType == ConnectionType.MySQL:
            connstr = 'DRIVER={MySQL ODBC 3.51 Driver}; SERVER=' + str(configs.getPropertyValue(sourceSectionName, "host")) + '; PORT=' + str(configs.getPropertyValue(sourceSectionName, "port")) + ';DATABASE=' + str(
                configs.getPropertyValue(sourceSectionName, "database")) + '; UID=' + str(configs.getPropertyValue(sourceSectionName, "username")) + '; PASSWORD=' + str(configs.getPropertyValue(sourceSectionName, "password")) + ';'
            conn = pyodbc.connect(connstr)
        elif connectionType == ConnectionType.File:
            return open(configs.getPropertyValue(sourceSectionName, "filepath"), 'r').readlines()
        elif connectionType == ConnectionType.MongoDB:
            if str(configs.getPropertyValue(sourceSectionName, "username")).strip() != "" and str(configs.getPropertyValue(sourceSectionName, "password")).strip() != "":
                client = pymongo.MongoClient(
                    "mongodb://" + str(configs.getPropertyValue(sourceSectionName, "username")) + '/' + str(configs.getPropertyValue(sourceSectionName, "password")) + '@' + str(configs.getPropertyValue(sourceSectionName, "host")) + ":" + str(
                        configs.getPropertyValue(sourceSectionName, "port")) + "/")
            else:
                client = pymongo.MongoClient("mongodb://" + str(configs.getPropertyValue(sourceSectionName, "host")) + ":" + str(configs.getPropertyValue(sourceSectionName, "port")) + "/")

            conn = client[str(configs.getPropertyValue(sourceSectionName, "database"))]

        print(str(configs.getConfigSectionData(sourceSectionName)).replace('[', '\n').replace('), (', '\n').replace('(', '').replace(')]', '').replace('\'', '').replace(',', ':'))
        if conn:
            print("Connection to " + sourceSectionName + " successful.")
        else:
            print("Connection to " + sourceSectionName + " failed.")

        return conn
    except Exception as e:
        # raise Exception("Connection Failed!" + str(e))
        return False
