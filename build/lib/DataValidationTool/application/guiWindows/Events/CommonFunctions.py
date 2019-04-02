import os
from configparser import RawConfigParser
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets

from DataValidationTool.core.configurations.configurations import configurations
from DataValidationTool.core.databases.DatabaseTypes import ConnectionType, getConnectionType
from DataValidationTool.core.databases.Operations import getConnection

iQueriesCount = 0

sFontName = "Carnas Light"
iFontSize = 8
iWindowWidth = 1250
iWindowHeight = 650
stempDirPath = str(Path.home()) + "/.dvt/"


def onClickSelectAllQueries(group: QtWidgets.QGroupBox, checkStatus: bool):
    checkbox: QtWidgets.QCheckBox = None
    for checkbox in group.findChildren(QtWidgets.QCheckBox):
        if checkbox.objectName().lower().startswith("querycheckbox"):
            if checkStatus:
                checkbox.setCheckState(QtCore.Qt.Checked)
            else:
                checkbox.setCheckState(QtCore.Qt.Unchecked)


def onCurrentIndexChanged(comboBox: QtWidgets.QComboBox, group: QtWidgets.QGroupBox, formLayout: QtWidgets.QFormLayout):
    global sFontName
    global iFontSize
    global stempDirPath
    groupName = group.objectName().lower().replace("grp", "")
    print("Value - " + str(comboBox.currentText()))
    for iRow in range(formLayout.rowCount(), 0, -1):
        formLayout.removeRow(iRow)

    # setup Labels & required Objects
    connType = getConnectionType(comboBox.currentText())
    lastConnections = stempDirPath.strip() + "lastConnected/" + comboBox.currentText() + ".ini"

    print(str(groupName) + "-" + lastConnections + " - " + str(os.path.exists(lastConnections)))
    values = {}
    if os.path.exists(lastConnections):
        fileConfig = RawConfigParser()
        fileConfig.sections()
        fileConfig.read(lastConnections)
        if fileConfig.has_section(groupName):
            values = dict(fileConfig.items(groupName))
            print(values)
    if connType == ConnectionType.File:
        objects = {"lblFilePath": "filepath"}
    elif connType == ConnectionType.HadoopHive:
        objects = {"lblHost": "host", "lblPort": "port", "lblDatabase": "database", "lblUsername": "username",
                   "lblPassword": "password", "lblAuth": "auth"}
    elif connType == ConnectionType.select:
        objects = {}
    else:
        objects = {"lblHost": "host", "lblPort": "port", "lblDatabase": "database", "lblUsername": "username",
                   "lblPassword": "password"}

    for name, text in objects.items():
        # Row Label Text
        lblRowLabel = QtWidgets.QLabel(text)
        lblRowLabel.setObjectName(name)
        lblRowLabel.setFont(setFontInfo(sFontName, False, False, iFontSize))
        # Row Text Edit
        txtRowEditbox = QtWidgets.QLineEdit()
        txtRowEditbox.setObjectName(text.lower())
        txtRowEditbox.setFont(setFontInfo(sFontName, False, False, iFontSize))
        if "password" in text.lower():
            txtRowEditbox.setEchoMode(QtWidgets.QLineEdit.Password)
        if text.lower() in values:
            txtRowEditbox.setText(values.get(text.lower()))
        formLayout.addRow(lblRowLabel, txtRowEditbox)
    btnTestConnection = QtWidgets.QPushButton()
    btnTestConnection.setIcon(QtGui.QIcon("./guiWindows/icons/testConnection.png"))
    btnTestConnection.setText("Test Connection")
    btnTestConnection.setFixedSize(150, 25)
    btnTestConnection.setFont(setFontInfo(sFontName, False, False, iFontSize))
    btnTestConnection.clicked.connect(lambda: onClickTestConnection(group))

    # setConnection Status
    wgdConnectionStatus = QtWidgets.QWidget()
    wgdConnectionStatus.setObjectName("wgdConnectionStatus")
    lblConnectionPic = QtWidgets.QLabel()
    lblConnectionStatus = QtWidgets.QLabel()
    lblConnectionPic.setObjectName("lblConnectionPic")
    icoConnection = QtGui.QPixmap("./guiWindows/icons/yellow_light.png")
    icoConnection = icoConnection.scaledToWidth(15)
    lblConnectionPic.setPixmap(icoConnection)
    lblConnectionStatus.setText("Connection Pending")
    lblConnectionStatus.setFont(setFontInfo(sFontName, False, False, iFontSize))
    lblConnectionStatus.setObjectName("lblConnectionStatus")
    statusLayout = QtWidgets.QFormLayout()
    statusLayout.addRow(lblConnectionPic, lblConnectionStatus)
    wgdConnectionStatus.setLayout(statusLayout)
    formLayout.addRow(btnTestConnection, wgdConnectionStatus)


def onClickAddQuery(group: QtWidgets.QGroupBox):
    global sFontName
    global iFontSize
    formLayout = group.layout()
    queriesCount: int = increamentQueriesCount(group.objectName(), 1)
    print("onClickAddQuery" + str(queriesCount))

    wdgQuery = QtWidgets.QWidget()
    wdgQuery.setObjectName(group.objectName() + "QueryWidget" + str(queriesCount))
    layoutQueryWidget = QtWidgets.QVBoxLayout()
    wdgQuery.setLayout(layoutQueryWidget)
    # Create GroupBox
    groupbox = QtWidgets.QGroupBox('Query ' + str(queriesCount))
    groupbox.setObjectName("groupQueries" + str(queriesCount))
    layoutQueryGroup = QtWidgets.QVBoxLayout()
    groupbox.setLayout(layoutQueryGroup)
    # Create Checkbox
    checkBox = QtWidgets.QCheckBox()
    checkBox.setObjectName("queryCheckBox")
    checkBox.setChecked(True)
    layoutQueryGroup.addWidget(checkBox)

    # Datakey Label
    lblDataKey = QtWidgets.QLabel("DataKey")
    lblDataKey.setFont(setFontInfo(sFontName, False, False, iFontSize))
    lblDataKey.setObjectName("lblDataKey")
    layoutQueryGroup.addWidget(lblDataKey)
    # Datakey Text
    txtDataKey = QtWidgets.QLineEdit()
    txtDataKey.setFont(setFontInfo(sFontName, False, False, iFontSize))
    txtDataKey.setObjectName("datakey")
    layoutQueryGroup.addWidget(txtDataKey)
    # Label Query
    lblQuery = QtWidgets.QLabel("Source Query")
    lblQuery.setFont(setFontInfo(sFontName, False, False, iFontSize))
    lblQuery.setObjectName("lblQuery" + str(queriesCount))
    layoutQueryGroup.addWidget(lblQuery)
    # Text Area Query
    txtAreaQuery = QtWidgets.QTextEdit()
    txtAreaQuery.setFont(setFontInfo(sFontName, False, False, iFontSize))
    txtAreaQuery.setObjectName("sourcequery")
    layoutQueryGroup.addWidget(txtAreaQuery)
    # Label Query
    lblQuery = QtWidgets.QLabel("Destination Query")
    lblQuery.setFont(setFontInfo(sFontName, False, False, iFontSize))
    lblQuery.setObjectName("lblQuery" + str(queriesCount))
    layoutQueryGroup.addWidget(lblQuery)
    # Text Area Query
    txtAreaQuery = QtWidgets.QTextEdit()
    txtAreaQuery.setFont(setFontInfo(sFontName, False, False, iFontSize))
    txtAreaQuery.setObjectName("destinationquery")
    layoutQueryGroup.addWidget(txtAreaQuery)
    # Add Group To Widget Layout
    layoutQueryWidget.addWidget(groupbox)
    formLayout.addRow(wdgQuery)
    return groupbox.objectName()


def onClickRemoveCheckedQueries(group: QtWidgets.QGroupBox):
    groupbox: QtWidgets.QGroupBox = None
    for groupbox in group.findChildren(QtWidgets.QGroupBox):
        checkbox: QtWidgets.QCheckBox = groupbox.findChild(QtWidgets.QCheckBox)
        if checkbox.checkState() == QtCore.Qt.Checked:
            print("Removing Query with object name- " + str(checkbox.parent().parent().objectName()))
            grpLayout: QtWidgets.QFormLayout = group.layout()
            grpLayout.removeRow(checkbox.parent().parent())


def collectGroupDataFromUI(group: QtWidgets.QGroupBox):
    config = configurations.getInstance()
    groupName = group.objectName().lower().replace("grp", "")
    config.addSection(groupName)
    for dataObject in group.findChildren((QtWidgets.QLineEdit, QtWidgets.QComboBox)):
        # print(item.objectName())
        if type(dataObject) == QtWidgets.QComboBox:
            config.addValueToSection(str(groupName).strip(), str(dataObject.objectName()).strip(), str(dataObject.currentText()))
        elif type(dataObject) == QtWidgets.QLineEdit:
            config.addValueToSection(str(groupName).strip(), str(dataObject.objectName()).strip(), str(dataObject.text()))
    return dict(config.getConfigSectionData(groupName))


def onClickTestConnection(group: QtWidgets.QGroupBox):
    global stempDirPath
    groupname = group.objectName().replace("grp", "")
    # print("Test Connection Request From : " + str(groupname))
    wgdConnectionStatus: QtWidgets.QWidget = group.findChild(QtWidgets.QWidget, "wgdConnectionStatus")
    lblConnectionStatus: QtWidgets.QLabel = wgdConnectionStatus.findChild(QtWidgets.QLabel, "lblConnectionStatus")
    lblConnectionPic: QtWidgets.QLabel = wgdConnectionStatus.findChild(QtWidgets.QLabel, "lblConnectionPic")
    print("Connection Status from " + groupname)
    dictData = collectGroupDataFromUI(group)

    if getConnection(groupname):
        lblConnectionStatus.setText("Connection successful...")
        lblConnectionPic.setPixmap(QtGui.QPixmap("./guiWindows/icons/green_light.png").scaledToWidth(15))
        # Write Connection Data To Last Connection File
        lastConnections = stempDirPath.strip() + "lastConnected/"
        print("Home Dir - " + lastConnections)
        if not os.path.exists(lastConnections):
            print("Create Connections Dir - " + lastConnections)
            os.makedirs(lastConnections)
        writeInfoToPropertiesFile(lastConnections + "/" + dictData.get("type") + ".ini", groupname, dictData)
        print("Save Connection For Last Connected as : " + lastConnections + "/" + dictData.get("type") + ".ini")
    else:
        lblConnectionStatus.setText("Connection failed...")
        lblConnectionPic.setPixmap(QtGui.QPixmap("./guiWindows/icons/red_light.png").scaledToWidth(15))

    print("Test Connection Complete")


def writeInfoToPropertiesFile(filePath: str, groupName: str, data: dict):
    config = RawConfigParser()
    config.sections()
    if os.path.exists(filePath):
        config.read(filePath)
    if not config.has_section(groupName):
        config.add_section(groupName)
    for key, value in data.items():
        print(key + ":" + value)
        config.set(groupName, key, value)
    # WriteToFile
    configfile = open(filePath, 'w');
    config.write(configfile)
    configfile.close()


def increamentQueriesCount(name: str, iVal: int):
    global iQueriesCount
    iQueriesCount += iVal
    return iQueriesCount


def setFontInfo(name, bold, italic, size):
    font = QtGui.QFont()
    font.setFamily(name)
    font.setBold(bold)
    font.setItalic(italic)
    font.setPointSize(size)
    return font


def getFilePath(windowShown):
    filePath, _ = QtWidgets.QFileDialog.getOpenFileName(windowShown, "Select Properties File", "", "Properties Files (*.ini)")
    return filePath


def setSummaryTabData(tabSummary: QtWidgets.QWidget):
    layoutSummary = QtWidgets.QHBoxLayout()
    tabSummary.setLayout(layoutSummary)
    lblTotalValidatedCount = QtWidgets.QLabel("")
    lblTotalValidatedCount.setWordWrap(True)

    lblTotalValidatedCount.setObjectName("lblTotalValidatedCount")
    layoutSummary.addWidget(lblTotalValidatedCount)
    scroll = QtWidgets.QScrollArea()
    scroll.setWidget(lblTotalValidatedCount)
    scroll.setWidgetResizable(True)
    scroll.setGeometry(tabSummary.rect())
    layoutSummary.addWidget(scroll)


def setTabDataDetails(tabRecords: QtWidgets.QWidget):
    if tabRecords.layout() is None:
        layoutRecords = QtWidgets.QFormLayout()

        tabRecords.setLayout(layoutRecords)
    else:
        layoutRecords = tabRecords.layout()

    # Clear All Records
    config = configurations.getInstance()
    # for i in reversed(range(layoutRecords.count())):
    #     wdgRemoveItem = layoutRecords.itemAt(i).widget()
    #     layoutRecords.removeWidget(wdgRemoveItem)
    #     del wdgRemoveItem
    for iRow in range(layoutRecords.rowCount(), -1, -1):
        layoutRecords.removeRow(iRow)
    wdgResources = QtWidgets.QWidget()
    layoutResults = QtWidgets.QVBoxLayout()
    wdgResources.setLayout(layoutResults)
    for section in config.getSections():
        if "query" in section.lower():
            grpSection = QtWidgets.QGroupBox()
            grpSection.setTitle(section)
            grpSection.setObjectName(section)
            grpSection.setMinimumHeight(500)
            layoutGroup = QtWidgets.QHBoxLayout()
            grpSection.setLayout(layoutGroup)
            layoutGroup.setObjectName("layout" + section)
            tableData = QtWidgets.QTableView()
            tableData.setObjectName("table" + section)
            layoutTestTable = QtWidgets.QHBoxLayout()
            tableData.setLayout(layoutTestTable)
            resultTable = QtWidgets.QTableWidget()
            resultTable.setObjectName("resultTable" + section)
            layoutTestTable.addWidget(resultTable)
            layoutGroup.addWidget(tableData)
            layoutResults.addWidget(grpSection)

    scroll = QtWidgets.QScrollArea()
    scroll.setWidget(wdgResources)
    scroll.setFixedHeight(500)
    scroll.setWidgetResizable(True)
    scroll.setGeometry(tabRecords.rect())
    layoutRecords.addWidget(scroll)
