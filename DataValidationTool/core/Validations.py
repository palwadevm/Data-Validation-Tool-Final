import datetime
import json
import math
import os
import threading
import time

from PyQt5 import QtWidgets, QtGui

from DataValidationTool.core.configurations import configurations
from DataValidationTool.core.databases import Operations, DatabaseTypes
from DataValidationTool.core import ConnectionType
from DataValidationTool.core import DataNode
from DataValidationTool.core import DataSyncQueue
from DataValidationTool.core.structs.DataTreeStruct import DataTreeStructure
from DataValidationTool.core import Match_Status

activeThreadsList = []
bSourceDataCollected = False
bDestinationDataCollected = False
globalConfig = configurations.getInstance()


def readAndPushDataToQueue(sourceType, query, dataKey):
    global bSourceDataCollected
    global bDestinationDataCollected
    print("Current Thread Name : " + threading.currentThread().name)
    config = configurations.getInstance()
    dataQueue = DataSyncQueue.getQueueInstance()
    print('--------------------------------------------------------------------------------------------------')
    print(config.getConfigSectionData(sourceType))
    print('--------------------------------------------------------------------------------------------------')
    try:

        dbconnection = Operations.getConnection(sourceType)
        dbType = DatabaseTypes.getConnectionType(config.getPropertyValue(sourceType, "type"))

        records = Operations.getRecords(dbconnection, dbType, query)
        if str(sourceType).lower() == "source":
            bSourceDataCollected = True
        else:
            bDestinationDataCollected = True
        bcolNames = False
        columns = []
        if dbType == ConnectionType.File or dbType == ConnectionType.MongoDB:
            bcolNames = True
        else:
            columns = [str(i[0]).lower() for i in records.description]
            key = columns.index(dataKey)
        print("******************************Records connected from " + str(dbType.name) + "******************************")
        print("Start Pushing data to Tree from " + str(dbType.name))
        for line in records:
            keyValue = ""
            dataDict = {}
            if type(line) == dict:
                dataDict = dict((k.lower(), getTypeCastedValue(v)) for k, v in dict(line).items())
                keyValue = str(dataDict.get(dataKey))
                dataDict.pop("_id")
            else:
                if bcolNames:
                    bcolNames = False
                    if dbType == ConnectionType.MongoDB:
                        columns = list(str(key).lower() for key in line.keys())
                        columns.remove("_id")
                        key = columns.index(dataKey)
                    else:
                        columns = list(col.lower() for col in line.replace("\n", "").split(','))
                        key = columns.index(dataKey)
                        continue

                if dbType == ConnectionType.File:
                    # data = line.split(',')
                    data = [getTypeCastedValue(dataElement).replace("\n", "") for dataElement in line.split(',')]
                else:
                    # data = list(line)
                    data = [getTypeCastedValue(dataElement) for dataElement in line]
                keyValue = str(data[key])
                dataDict = dict(zip(columns, data))
            # print(line)
            dataQueue.addNodeToQueue(DataNode(keyValue, dataDict, sourceType))
    except Exception as e:
        raise Exception("Exception in Thread " + threading.currentThread().name + ".\n" + str(e))


def pushDataToComparison():
    # Create Tree Structure for data comparisona
    tree = DataTreeStructure()
    dataQueue = DataSyncQueue()

    while True:
        try:
            tree.insert_dataNode(dataQueue.getFirstNode())
        except:
            if bSourceDataCollected and bDestinationDataCollected:
                print("Push data operation completed from both databases")
                break
            else:
                while bSourceDataCollected and bDestinationDataCollected:
                    print('Queue is empty now..... waiting for another db to connect and send records, ' +
                          '\nData status' +
                          '\nSource : ' + str(bSourceDataCollected) +
                          "\nDesitnation : " + str(bDestinationDataCollected))
                    time.sleep(1)
                    break


def getTypeCastedValue(val, checknum=False):
    global globalConfig
    if type(val) == int:
        return str(int(val))
    elif type(val) == float:
        return str(float(globalConfig.getPropertyValueOrDefaultValue("dataformats", "float", "{0:.2f}").format(val)))
    elif type(val) == datetime.datetime:
        val = datetime.datetime.strftime(val, globalConfig.getPropertyValueOrDefaultValue("dataformats", "datetime", "%Y-%m-%d %H:%M:%S.%f"))
        if "%Y-%m-%d %H:%M:%S.%f" == globalConfig.getPropertyValueOrDefaultValue("dataformats", "datetime", "%Y-%m-%d %H:%M:%S.%f"):
            val = str(val[:-3])
        return val
    elif type(val) == str:
        return str(val)
    else:
        return str(val)


def validateBackend():
    # get Instance of the Configuations Class
    config = configurations.getInstance()
    global activeThreadsList
    #######################################################################################################################
    print("Main thread name: {}".format(threading.main_thread().name))
    print(config.getConfigSectionData("execution"))
    # Multiple Queries implementation
    reportsBaseFolder = str(config.getPropertyValue("execution", "resultsFolder"))
    os.makedirs(reportsBaseFolder)
    reportJson = open(reportsBaseFolder + "/Summary.json", mode='a+', encoding='utf-8')
    print("Summary Report - " + reportsBaseFolder + "/Summary.json")
    reportJson.write("{\"SUMMARY\": [")

    # Multiple Queries implementation
    for section in config.getSections():
        if "query" in str(section).lower():
            print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
            startTimer = time.time()
            activeThreadsList = []
            # Setup The Tree For the Operations
            tree = DataTreeStructure()
            # Collect Section Data
            sectionData = dict(config.getConfigSectionData(section))
            # Thread 1 Connect To the database/file 1 and start pushing data to the DataQueue
            source1Thread = threading.Thread(target=readAndPushDataToQueue,
                                             args=['source', str(sectionData.get("sourcequery")).strip(),
                                                   str(sectionData.get("datakey")).strip()],
                                             name='Read Data From Source 1 and Push to Data Queue')
            # Thread 2 Connect To the database/file 2 and start pushing data to the DataQueue
            source2Thread = threading.Thread(target=readAndPushDataToQueue,
                                             args=['destination', str(sectionData.get("destinationquery")).strip(),
                                                   str(sectionData.get("datakey")).strip()],
                                             name='Read Data From Source 2 and Push to Data Queue')
            # Compare Thread
            comparisonThread = threading.Thread(target=pushDataToComparison, name='Start Pushing Data To the Tree')

            activeThreadsList.append(source1Thread)
            activeThreadsList.append(source2Thread)
            activeThreadsList.append(comparisonThread)
            # Start Threads
            for execThread in activeThreadsList:
                execThread.start()

            # Wait For Thread To Complete
            for execThread in activeThreadsList:
                execThread.join()
                activeThreadsList.remove(execThread)

            # Create Reports Folder
            reportsFolder = str(config.getPropertyValue("execution", "resultsFolder")) + str(section) + "/"
            os.makedirs(reportsFolder)
            endTimer = time.time()
            matchCount = tree.getRecordsWithState(set([Match_Status.MATCHED]), reportsFolder)
            fieldMismatchCount = tree.getRecordsWithState(set([Match_Status.FIELDS_MISMATCH]), reportsFolder)
            mismatchCount = tree.getRecordsWithState(set([Match_Status.MISSING_DATA]), reportsFolder)
            execTime = "{0:.2f}".format(endTimer - startTimer)
            print("#######################################################################################################################")
            print("Summary for " + str(section))
            print("Source Query \t\t\t\t\t: " + str(sectionData.get("sourcequery")).strip())
            print("Destination Query \t\t\t\t: " + str(sectionData.get("destinationquery")).strip())
            print("Total Passed Records\t\t\t: " + str(matchCount))
            print("Total Failed Records\t\t\t: " + str(mismatchCount))
            print("Total Fields Mismatch Records\t: " + str(fieldMismatchCount))
            print("Result Log Files\t\t\t\t: " + reportsFolder.replace("\\", "/"))
            print("Time taken to validate\t\t\t: " + str(execTime) + " Second(s)")
            print("#######################################################################################################################")
            # Reset The Tree Once Operations Are completed
            tree.resetTree()
            print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
            #######################################################################################################################
            print("Execution For Queries Complete")
            jsonData = "{\"name\":\"" + str(section) + "\", " \
                       + "\"sourcequery\": \"" + str(sectionData.get("sourcequery")).strip() + "\", " \
                       + "\"destinationquery\": \"" + str(sectionData.get("destinationquery")).strip() + "\", " \
                       + "\"passed\": " + str(matchCount) + ", " \
                       + "\"failed\": " + str(mismatchCount) + ", " \
                       + "\"fieldsmismatch\": " + str(fieldMismatchCount) + ", " \
                       + "\"exectime\": " + str(execTime) + ", " \
                       + "\"resultpath\": \"" + str(reportsFolder.replace("\\", "/")) + "\" " \
                       + "},"
            reportJson.write(jsonData)

    # Close Json File
    reportJson.write("]}")
    reportJson.close()


def validateUI(windowShown: QtWidgets.QWidget):
    print("Execute UI Connection Validation")
    # get Instance of the Configuations Class
    config = configurations.getInstance()
    global activeThreadsList
    global bSourceDataCollected
    global bDestinationDataCollected
    #######################################################################################################################
    print("Main thread name: {}".format(threading.main_thread().name))
    print(config.getConfigSectionData("execution"))
    # Multiple Queries implementation
    reportsBaseFolder = str(config.getPropertyValue("execution", "resultsFolder")) + str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    os.makedirs(reportsBaseFolder)
    reportJson = open(reportsBaseFolder + "/Summary.json", mode='a+', encoding='utf-8')
    print("Summary Report - " + reportsBaseFolder + "/Summary.json")
    reportJson.write("{\"SUMMARY\": [")
    totalQueriesCounter = 0
    for section in config.getSections():
        if "query" in str(section).lower():
            totalQueriesCounter += 1
    queryCounter = 0
    progress: QtWidgets.QProgressBar = windowShown.findChild(QtWidgets.QProgressBar, "validationProgress")
    for section in config.getSections():
        if "query" in str(section).lower():
            bSourceDataCollected = False
            bDestinationDataCollected = False
            startTimer = time.time()
            activeThreadsList = []
            # Setup The Tree For the Operations
            tree = DataTreeStructure()
            # Collect Section Data
            sectionData = dict(config.getConfigSectionData(section))
            # Thread 1 Connect To the database/file 1 and start pushing data to the DataQueue
            source1Thread = threading.Thread(target=readAndPushDataToQueue,
                                             args=['source', str(sectionData.get("sourcequery")).strip(),
                                                   str(sectionData.get("datakey")).strip()],
                                             name='Read Data From Source 1 and Push to Data Queue')
            # Thread 2 Connect To the database/file 2 and start pushing data to the DataQueue
            source2Thread = threading.Thread(target=readAndPushDataToQueue,
                                             args=['destination', str(sectionData.get("destinationquery")).strip(),
                                                   str(sectionData.get("datakey")).strip()],
                                             name='Read Data From Source 2 and Push to Data Queue')
            # Compare Thread
            comparisonThread = threading.Thread(target=pushDataToComparison, name='Start Pushing Data To the Tree')

            activeThreadsList.append(source1Thread)
            activeThreadsList.append(source2Thread)
            activeThreadsList.append(comparisonThread)
            # Start Threads
            for execThread in activeThreadsList:
                execThread.start()

            # Wait For Thread To Complete
            for execThread in activeThreadsList:
                execThread.join()
                # activeThreadsList.remove(execThread)

            print("#######################################################################################################################")
            # Create Reports Folder

            reportsFolder = reportsBaseFolder + "/" + str(section) + "/"
            os.makedirs(reportsFolder)
            lblTotalValidatedCount: QtWidgets.QLabel = windowShown.findChild(QtWidgets.QLabel, "lblTotalValidatedCount")
            endTimer = time.time()
            matchCount = tree.getRecordsWithState(set([Match_Status.MATCHED]), reportsFolder)
            fieldMismatchCount = tree.getRecordsWithState(set([Match_Status.FIELDS_MISMATCH]), reportsFolder)
            mismatchCount = tree.getRecordsWithState(set([Match_Status.MISSING_DATA]), reportsFolder)
            execTime = "{0:.2f}".format(endTimer - startTimer)
            threadExecSummary = lblTotalValidatedCount.text() + "\n" \
                                + "#######################################################################################################################" + "\n" \
                                + "Summary for " + str(section) + "\n" \
                                + "Source Query \t\t\t\t: " + str(sectionData.get("sourcequery")).strip() + "\n" \
                                + "Destination Query \t\t\t\t: " + str(sectionData.get("destinationquery")).strip() + "\n" \
                                + "Total Passed Records\t\t\t: " + str(matchCount) + "\n" \
                                + "Total Failed Records\t\t\t: " + str(mismatchCount) + "\n" \
                                + "Total Fields Mismatch Records\t\t: " + str(fieldMismatchCount) + "\n" \
                                + "Result Log Files\t\t\t\t: " + reportsFolder.replace("\\", "/") + "\n" \
                                + "Time taken to validate\t\t\t: " + str(execTime) + " Second(s)\n" \
                                + "#######################################################################################################################\n"
            time.sleep(1)
            lblTotalValidatedCount.setText(threadExecSummary)
            jsonData = "{\"name\":\"" + str(section) + "\", " \
                       + "\"sourcequery\": \"" + str(sectionData.get("sourcequery")).strip() + "\", " \
                       + "\"destinationquery\": \"" + str(sectionData.get("destinationquery")).strip() + "\", " \
                       + "\"passed\": " + str(matchCount) + ", " \
                       + "\"failed\": " + str(mismatchCount) + ", " \
                       + "\"fieldsmismatch\": " + str(fieldMismatchCount) + ", " \
                       + "\"exectime\": " + str(execTime) + ", " \
                       + "\"resultpath\": \"" + str(reportsFolder.replace("\\", "/")) + "\" " \
                       + "},"
            reportJson.write(jsonData)
            # Reset The Tree Once Operations Are completed
            tree.resetTree()
            # Add Report Files Data to Report Data Tables
            updateJsonToUITable(windowShown, section.lower(), reportsFolder + "FIELDS_MISMATCH.json", "FIELDS_MISMATCH", int(config.getPropertyValueOrDefaultValue("execution", "maxresultrows", "1000"), 10))
            updateJsonToUITable(windowShown, section.lower(), reportsFolder + "MISSING_DATA.json", "MISSING_DATA", int(config.getPropertyValueOrDefaultValue("execution", "maxresultrows", "1000"), 10))
            updateJsonToUITable(windowShown, section.lower(), reportsFolder + "MATCHED.json", "MATCHED", int(config.getPropertyValueOrDefaultValue("execution", "maxresultrows", "1000"), 10))
            # Report Update Progress bar
            print("Execution Time For " + str(section) + " : " + str(execTime))
            queryCounter += 1
            percentage = math.ceil((queryCounter / totalQueriesCounter) * 100)
            progress.setValue(percentage)
    # Close Json File
    reportJson.write("]}")
    reportJson.close()
    #######################################################################################################################
    print("Execution For Queries Complete")


def getTableDataFromJson(filePath, type, maxDataCount=1000):
    json_file = open(filePath, "r")
    data = json.load(json_file)
    returnData = []
    rowsCount = 0
    for resultItem in data[type]:
        rowsCount += 1
        failedFields = str(resultItem["failedColumns"])
        if failedFields != "":
            failedFields = list(failedFields.split("|"))
            print("Failed Fields : " + str(failedFields))
        else:
            failedFields = []

        if resultItem["isAvailableInSrc"]:
            for values in resultItem["source"]:
                temp = {"datafrom": "Source", "datakey": resultItem["datakey"]}
                temp.update(values)
                for failedKey in failedFields:
                    temp[failedKey.lower()] = temp[failedKey.lower()] + "|RED"
                returnData.append(temp)
        # TODO Add Empty Row if Not Available In Source
        if resultItem["isAvailableInDest"]:
            for values in resultItem["destination"]:
                temp = {"datafrom": "Destination", "datakey": resultItem["datakey"]}
                temp.update(values)
                for failedKey in failedFields:
                    temp[failedKey.lower()] = temp[failedKey.lower()] + "|RED"
                returnData.append(temp)
        # TODO Add Empty Row if Not Available In Destination
        if rowsCount > maxDataCount:
            break
    json_file.close()
    return returnData


def updateJsonToUITable(windowShown: QtWidgets.QWidget, querySection: str, filePath: str, type: str, maxDataRows=1000):
    print("Load Data From Json file " + filePath)
    tabName = ""
    if type == "FIELDS_MISMATCH":
        tabName = "tabPartialMismatch"
    elif type == "MISSING_DATA":
        tabName = "tabMismatches"
    elif type == "MATCHED":
        tabName = "tabMatchedRecords"
    else:
        return None;
    fileData = getTableDataFromJson(filePath, type, maxDataRows)
    tabsResults = windowShown.findChild(QtWidgets.QTabWidget, "tabResults")
    tabResults: QtWidgets.QWidget = tabsResults.findChild(QtWidgets.QWidget, tabName)
    tableView: QtWidgets.QTableView = tabResults.findChild(QtWidgets.QTableView, "table" + querySection)
    resultTable: QtWidgets.QTableWidget = tableView.findChild(QtWidgets.QTableWidget, "resultTable" + querySection)
    print(tabResults.objectName() + " - " + tableView.objectName() + " - Table View")
    if len(fileData) > 0:
        dataColumns = list(fileData[0].keys())
        resultTable.setRowCount(0)
        resultTable.setColumnCount(len(dataColumns))
        print(resultTable.objectName())
        resultTable.setHorizontalHeaderLabels(dataColumns)
        resultTable.setRowCount(len(fileData))
        iRowCounter = 0
        for data in fileData:
            for key in data.keys():
                resultTable.setItem(iRowCounter, dataColumns.index(key.lower()), QtWidgets.QTableWidgetItem(str(data[key]).replace("|RED", "")))
                if "|RED" in data[key]:
                    print(str(data[key]))
                    resultTable.item(iRowCounter, dataColumns.index(key.lower())).setBackground(QtGui.QColor(255, 134, 134))
            iRowCounter += 1
        # resultTable.resizeColumnsToContents()
    else:
        pass
