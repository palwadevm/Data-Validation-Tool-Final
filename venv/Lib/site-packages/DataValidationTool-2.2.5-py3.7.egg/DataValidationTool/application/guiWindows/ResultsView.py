import os
import threading
from configparser import RawConfigParser

import psutil
from PyQt5 import QtGui, QtWidgets

from DataValidationTool.application.guiWindows.Events import CommonFunctions
from DataValidationTool.core import Validations
from DataValidationTool.core.configurations.configurations import configurations

activeThreads = []


def collectQueriesFromFile(windowShown: QtWidgets.QWidget):
    print("Collecting queries from file from path ")
    editQueriesFilePath: QtWidgets.QLineEdit = windowShown.findChild(QtWidgets.QLineEdit, "editQueriesFilePath")
    filePath = editQueriesFilePath.text()
    loadDataToUIFromFile(windowShown, filePath, "query")


def collectQueriesFromUI(windowShown: QtWidgets.QWidget):
    grpQueries: QtWidgets.QGroupBox = windowShown.findChild(QtWidgets.QWidget, "wdgQueries").findChild(QtWidgets.QGroupBox)
    print("Collect Queries From UI - " + grpQueries.title())
    config = configurations.getInstance()
    # Remove All Other Queries before execution
    for section in config.getSections():
        if str(section).lower().startswith("query"):
            config.removeSection(section)

    for grpQuery in grpQueries.findChildren(QtWidgets.QGroupBox):
        grpQuery: QtWidgets.QGroupBox
        sectionName = str(grpQuery.objectName()).replace("groupQueries", "query")
        if grpQuery.findChild(QtWidgets.QCheckBox, "queryCheckBox").isChecked():
            for textObject in grpQuery.findChildren((QtWidgets.QTextEdit, QtWidgets.QLineEdit)):
                if type(textObject) == QtWidgets.QTextEdit:
                    config.addValueToSection(sectionName, textObject.objectName(), textObject.toPlainText())
                elif type(textObject) == QtWidgets.QLineEdit:
                    config.addValueToSection(sectionName, textObject.objectName(), textObject.text())
    pass


def collectConfigInformationFromUI(windowShown: QtWidgets.QWidget):
    print("Collecting Data From UI")
    config = configurations.getInstance()
    config.readBaseConfigurations()
    CommonFunctions.collectGroupDataFromUI(windowShown.findChild(QtWidgets.QGroupBox, "grpsource"))
    CommonFunctions.collectGroupDataFromUI(windowShown.findChild(QtWidgets.QGroupBox, "grpdestination"))
    # Collect Queries
    if windowShown.findChild(QtWidgets.QRadioButton, "rdbQueriesFile").isChecked():
        # Get Data From File
        collectQueriesFromFile(windowShown)
        pass  # Get Data From File
    elif windowShown.findChild(QtWidgets.QRadioButton, "rdbQueriesUI").isChecked():
        # Get Data From UI Queries
        collectQueriesFromUI(windowShown)
        pass


def startValidation(windowShown: QtWidgets.QWidget):
    btnValidateQueries: QtWidgets.QPushButton = windowShown.findChild(QtWidgets.QPushButton, "btnValidateQueries")
    config = configurations.getInstance()
    process = psutil.Process(os.getpid())
    print("Current CPU Usage - " + str(os.getpid()) + " - " + str(process.memory_info().rss))  # in bytes
    collectConfigInformationFromUI(windowShown)
    if btnValidateQueries.text().lower() == "stop execution":
        # Update Button To Stop Execution
        btnValidateQueries.setText("Validate Queries")
        btnValidateQueries.setIcon(QtGui.QIcon("./guiWindows/icons/startExecution.ico"))
        # Show Connection Widget and Hide Result Widget
        wdgConnection: QtWidgets.QWidget = windowShown.findChild(QtWidgets.QWidget, "wdgConnection")
        wdgConnection.show()
        wdgResultView: QtWidgets.QWidget = windowShown.findChild(QtWidgets.QWidget, "wdgResultView")
        wdgResultView.hide()
    elif btnValidateQueries.text().lower() == "validate queries":
        lblTotalValidatedCount: QtWidgets.QLabel = windowShown.findChild(QtWidgets.QLabel, "lblTotalValidatedCount")
        lblTotalValidatedCount.setText("")
        # Update Button To Stop Execution
        btnValidateQueries.setText("Stop Execution")
        btnValidateQueries.setIcon(QtGui.QIcon("./guiWindows/icons/stopExecution.ico"))
        # Hide Connection Widget and Show Result Widget
        wdgConnection: QtWidgets.QWidget = windowShown.findChild(QtWidgets.QWidget, "wdgConnection")
        wdgConnection.hide()
        wdgResultView: QtWidgets.QWidget = windowShown.findChild(QtWidgets.QWidget, "wdgResultView")
        wdgResultView.show()

        windowShown.findChild(QtWidgets.QLabel, "lblCurrentProgress").setEnabled(True)
        validationProgress: QtWidgets.QProgressBar = windowShown.findChild(QtWidgets.QProgressBar, "validationProgress")
        validationProgress.setEnabled(True)
        validationProgress.setProperty("value", 0)

        # Tab mismatches
        for tabName in ["tabMismatches", "tabPartialMismatch", "tabMatchedRecords"]:
            tabResults = windowShown.findChild(QtWidgets.QWidget, tabName)
            CommonFunctions.setTabDataDetails(tabResults)
        startExecution(windowShown)


def startExecution(windowShown: QtWidgets.QWidget):
    config = configurations.getInstance()
    executionThread = threading.Thread(target=Validations.validateUI, args=[windowShown], name='Start Validation From UI.')
    activeThreads.append(executionThread)
    executionThread.start()


def stopExecution():
    config = configurations.getInstance()


def updateUIStatus(windowShown: QtWidgets.QWidget):
    i = 1


def loadDataToUIFromFile(windowShown: QtWidgets.QWidget, filePath: str, sectionValue: str = ""):
    config = configurations.getInstance(filePath)
    configFile = RawConfigParser()
    configFile.sections()
    configFile.read(filePath)
    # Remove All Existing Queries
    grpQueriesSection: QtWidgets.QGroupBox = windowShown.findChild(QtWidgets.QGroupBox, "grpqueries")
    formLayout = grpQueriesSection.layout()
    bRemoveAllQueries: bool = True

    # Setup Data
    for section in configFile.sections():
        name = str(section)
        if sectionValue.lower() in name:
            if name.lower() == "default" or name.lower() == "thread" or name.lower() == "queue" or name.lower() == "execution":
                print("Skip Section For UI- " + name)
                continue
            elif name.lower() == "source" or name.lower() == "destination":
                grpSectionUI: QtWidgets.QGroupBox = windowShown.findChild(QtWidgets.QGroupBox, "grp" + name.lower())
                print("Section Found : " + grpSectionUI.objectName())
                for key, value in dict(config.getConfigSectionData(name)).items():
                    print(key + " : " + value)
                    objValue = grpSectionUI.findChild((QtWidgets.QLineEdit, QtWidgets.QComboBox), str(key))
                    # Set Value
                    if type(objValue) == QtWidgets.QComboBox:
                        objValue.setCurrentText(value)
                    elif type(objValue) == QtWidgets.QLineEdit:
                        objValue.setText(value)
            elif "query" in name.lower():
                if bRemoveAllQueries:
                    editQueriesFilePath: QtWidgets.QLineEdit = windowShown.findChild(QtWidgets.QLineEdit, "editQueriesFilePath")
                    editQueriesFilePath.setText(filePath)
                    for iRow in range(formLayout.rowCount(), 0, -1):
                        formLayout.removeRow(iRow)
                bRemoveAllQueries = False
                grpQueriesSection: QtWidgets.QGroupBox = windowShown.findChild(QtWidgets.QGroupBox, "grpqueries")
                grpName = CommonFunctions.onClickAddQuery(grpQueriesSection)
                grpQuery: QtWidgets.QGroupBox = windowShown.findChild(QtWidgets.QGroupBox, grpName)
                for key, value in dict(config.getConfigSectionData(name)).items():
                    print(grpName + " - " + key + " : " + value)
                    objValue = grpQuery.findChild((QtWidgets.QTextEdit, QtWidgets.QLineEdit), key)
                    objValue.setText(value)
            else:
                print("Set Section Values - " + name)
