from configparser import RawConfigParser

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from DataValidationTool.application.guiWindows import ResultsView
from DataValidationTool.application.guiWindows.Events import CommonFunctions
from DataValidationTool.core.configurations.configurations import configurations
from DataValidationTool.core.databases.DatabaseTypes import ConnectionType

config: configurations = configurations.getInstance()


class DataValidationWindow(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    global config

    def __init__(self, parent=None):
        super(DataValidationWindow, self).__init__(parent=parent)
        self.setupUi()
        self.show()

    # self.setupUi(self)

    def setupUi(self):
        global config
        # Setup Window Size and Basic Information
        _translate = QtCore.QCoreApplication.translate
        self.resize(CommonFunctions.iWindowWidth, CommonFunctions.iWindowHeight)
        self.setFixedSize(CommonFunctions.iWindowWidth, CommonFunctions.iWindowHeight)

        self.setWindowTitle(_translate("MainWindow", config.getPropertyValue("default", "ProjectName") + " v" + config.getPropertyValue("default", "ProjectVersion")))
        self.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, True, False, CommonFunctions.iFontSize))
        self.setObjectName("dataValidationWindow")

        # Set Window Icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./guiWindows/icons/computer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        # Setup Menu bar
        self.topmenubar = QtWidgets.QMenuBar(self)
        self.topmenubar.setGeometry(QtCore.QRect(0, 0, self.width(), 21))
        self.topmenubar.setObjectName("topmenubar")
        # File Menu
        self.menuFile = QtWidgets.QMenu(self.topmenubar)
        self.menuFile.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.setMenuBar(self.topmenubar)

        # Menu Load From Menu bar
        self.menuLoadFromFile = QtWidgets.QAction(self)
        self.menuLoadFromFile.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        self.menuLoadFromFile.setObjectName("menuLoadFromFile")
        self.menuLoadFromFile.setText(_translate("MainWindow", "Load From File"))
        self.menuLoadFromFile.triggered.connect(lambda: self.loadDetailsFromFile())
        # Add Actions
        self.menuFile.addAction(self.menuLoadFromFile)
        self.topmenubar.addAction(self.menuFile.menuAction())

        # Central Widet
        self.windowShown = QtWidgets.QWidget(self)
        self.windowShown.setObjectName("windowShown")
        self.setCentralWidget(self.windowShown)

        # Setup the Window Layout & Central Widget
        self.wdgConnectionView = QtWidgets.QWidget(self.windowShown)
        self.wdgConnectionView.setObjectName("wdgConnection")
        self.wdgResultView = QtWidgets.QWidget(self.windowShown)
        self.wdgResultView.setObjectName("wdgResultView")
        self.wdgResultView.hide()

        # 	Setup Source Database Information Set
        self.wgdSource = QtWidgets.QWidget(self.wdgConnectionView)
        self.wgdSource.setGeometry(QtCore.QRect(10, 10, (self.width() / 2) - 20, (self.height() * 45) / 100))
        self.layoutSource = QtWidgets.QVBoxLayout(self.wgdSource)
        self.layoutSource.addWidget(self.setConnectionGroup("source", self.wgdSource))

        # 	Setup Destination Database Information Set
        self.wgdDestination = QtWidgets.QWidget(self.wdgConnectionView)
        self.wgdDestination.setGeometry(QtCore.QRect((self.width() / 2) + 20, 10, (self.width() / 2) - 20, (self.height() * 45) / 100))
        self.layoutDestination = QtWidgets.QVBoxLayout(self.wgdDestination)
        self.layoutDestination.addWidget(self.setConnectionGroup("destination", self.wgdDestination))

        self.grpQueries = QtWidgets.QGroupBox(self.wdgConnectionView)
        self.grpQueries.setObjectName("grpQueries")
        self.grpQueries.setTitle("Queries")
        self.grpQueries.setGeometry(QtCore.QRect(17, ((self.height() * 46) / 100), (self.width()) - 34, (self.height() * 41) / 100))
        self.wdgQueriesView = QtWidgets.QWidget(self.grpQueries)
        self.wdgQueriesView.setObjectName("wdgQueriesView")
        self.wdgQueriesView.setGeometry(QtCore.QRect(0, 0, (self.grpQueries.width() - 20), (self.grpQueries.height())))

        # Set Queries Option --- File
        self.rdbQueriesFile = QtWidgets.QRadioButton(self.grpQueries)
        self.rdbQueriesFile.setObjectName("rdbQueriesFile")
        self.rdbQueriesFile.setText("Queries File")
        self.rdbQueriesFile.setGeometry(QtCore.QRect(10, 20, 100, 20))
        self.rdbQueriesFile.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        self.rdbQueriesFile.setChecked(True)
        self.wdgQueriesFile = QtWidgets.QWidget(self.wdgQueriesView)
        self.wdgQueriesFile.setGeometry(QtCore.QRect(10, 40, (self.wdgQueriesView.width()), (self.wdgQueriesView.height())))
        # self.layoutQueries = QtWidgets.QVBoxLayout(self.wdgQueriesFile)
        # self.layoutQueries.addWidget(self.setQueriesFilesUi(self.wdgQueriesFile))
        self.setQueriesFilesUi(self.wdgQueriesFile)
        # Set Queries Option --- UI
        self.rdbQueriesUI = QtWidgets.QRadioButton(self.grpQueries)
        self.rdbQueriesUI.setObjectName("rdbQueriesUI")
        self.rdbQueriesUI.setText("Queries From UI")
        self.rdbQueriesUI.setGeometry(QtCore.QRect(150, 20, 200, 20))
        self.rdbQueriesUI.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        self.rdbQueriesUI.setChecked(False)
        self.rdbQueriesFile.toggled.connect(lambda: self.updateQueriesSection())
        self.rdbQueriesUI.toggled.connect(lambda: self.updateQueriesSection())

        # Setup Queries UI
        self.wdgQueries = QtWidgets.QWidget(self.wdgQueriesView)
        self.wdgQueries.setObjectName("wdgQueries")
        self.wdgQueries.setGeometry(QtCore.QRect(10, 40, (self.wdgQueriesView.width()), (self.wdgQueriesView.height())))
        self.layoutQueries = QtWidgets.QVBoxLayout(self.wdgQueries)
        self.layoutQueries.addWidget(self.setupQuerySection("queries", self.wdgQueries))
        self.wdgQueries.hide()
        # 	Validation Button
        self.btnValidateQueries = QtWidgets.QPushButton(self.windowShown)
        self.btnValidateQueries.setObjectName("btnValidateQueries")
        self.btnValidateQueries.setIcon(QtGui.QIcon("./guiWindows/icons/startExecution.ico"))
        self.btnValidateQueries.setText("Validate Queries")
        self.btnValidateQueries.move(20, (self.height() - 80))
        self.btnValidateQueries.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        self.btnValidateQueries.clicked.connect(lambda: ResultsView.startValidation(self.windowShown))

        # Result Path
        self.editResultFolder = QtWidgets.QLineEdit(self.windowShown)
        self.editResultFolder.setObjectName("editResultFolder")
        self.editResultFolder.setPlaceholderText("Report Folder Path")
        self.editResultFolder.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        self.editResultFolder.setGeometry(150, (self.height() - 80), (self.width() * 80) / 100, 25)
        self.editResultFolder.setReadOnly(True)
        self.editResultFolder.setText(str(config.getPropertyValue("execution", "resultsFolder")).replace("\\", "/"))

        # 	Path Selector
        self.btnSelectResultPath = QtWidgets.QToolButton(self.windowShown)
        self.btnSelectResultPath.setObjectName("btnSelectResultPath")
        self.btnSelectResultPath.setGeometry(((self.width() * 80) / 100) + 170, (self.height() - 80), 25, 25)
        self.btnSelectResultPath.setText("...")
        self.btnSelectResultPath.clicked.connect(lambda: self.selectResultFolder())

        # Setup Result Widget
        # Add Tabs To Result
        self.tabResults = QtWidgets.QTabWidget(self.wdgResultView)
        self.tabResults.setGeometry(QtCore.QRect(10, 10, self.width() - 20, (self.height() * 85) / 100))
        self.tabResults.setObjectName("tabResults")
        self.tabResults.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))

        # Summary Tab
        self.tabSummary = QtWidgets.QWidget()
        self.tabSummary.setObjectName("tabSummary")
        self.tabResults.addTab(self.tabSummary, "Summary")
        # Set Summary Tab Layout
        CommonFunctions.setSummaryTabData(self.tabSummary)

        # Mismatches Tab
        self.tabMismatches = QtWidgets.QWidget()
        self.tabMismatches.setObjectName("tabMismatches")
        self.tabResults.addTab(self.tabMismatches, "Unique Records")
        # add Sections to Mismatch Query Tab
        CommonFunctions.setTabDataDetails(self.tabMismatches)
        # Partial Mismatches Tab
        self.tabPartialMismatch = QtWidgets.QWidget()
        self.tabPartialMismatch.setObjectName("tabPartialMismatch")
        self.tabResults.addTab(self.tabPartialMismatch, "Data Mismatched Records")
        CommonFunctions.setTabDataDetails(self.tabPartialMismatch)
        # Matched Tab
        self.tabMatchedRecords = QtWidgets.QWidget()
        self.tabMatchedRecords.setObjectName("tabMatchedRecords")
        self.tabResults.addTab(self.tabMatchedRecords, "Matched Records")
        CommonFunctions.setTabDataDetails(self.tabMatchedRecords)

        # Create Progress Label
        self.lblCurrentProgress = QtWidgets.QLabel(self.windowShown)
        self.lblCurrentProgress.setGeometry(QtCore.QRect(20, (self.height() - 50), 100, 20))
        self.lblCurrentProgress.setObjectName("lblCurrentProgress")
        self.lblCurrentProgress.setText(_translate("MainWindow", "Current Status"))
        self.lblCurrentProgress.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        self.lblCurrentProgress.setEnabled(False)

        # Create Progress bar
        self.validationProgress = QtWidgets.QProgressBar(self.windowShown)
        self.validationProgress.setEnabled(False)
        self.validationProgress.setGeometry(QtCore.QRect(110, (self.height() - 50), ((self.width() * 90) / 100), 20))
        self.validationProgress.setProperty("value", 0)
        self.validationProgress.setObjectName("validationProgress")
        self.validationProgress.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))

    def selectResultFolder(self):
        global config
        self.editResultFolder.setText(str(QFileDialog.getExistingDirectory(self, "Select Directory")) + "/")
        config.addValueToSection("execution", "resultsFolder", self.editResultFolder.text())

    def setConnectionGroup(self, source: str, baseWidget: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        # Create Groups For Source and Destination Database Info
        grpSource = QtWidgets.QGroupBox()
        grpSource.setGeometry(baseWidget.rect())
        grpSource.setObjectName("grp" + str(source).lower())
        grpSource.setTitle(_translate("MainWindow", source.title()))
        grpSource.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, True, False, CommonFunctions.iFontSize))
        # Form Connection
        connectionForm = QtWidgets.QFormLayout()
        connectionForm.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignLeft)
        grpSource.setLayout(connectionForm)
        # Set Type of The connecction
        lblType = QtWidgets.QLabel("Type")
        lblType.setObjectName("type")
        lblType.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        # Type Combobox
        cmbType = QtWidgets.QComboBox()
        cmbType.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        cmbType.setObjectName("type")
        cmbType.addItems(list(map(lambda type: type.value, ConnectionType)))
        connectionForm.addRow(lblType, cmbType)
        cmbType.currentIndexChanged.connect(lambda: CommonFunctions.onCurrentIndexChanged(cmbType, grpSource, connectionForm))

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(grpSource)
        scroll.setWidgetResizable(True)
        scroll.setGeometry(baseWidget.rect())
        return scroll

    def setupQuerySection(self, name: str, baseWidget: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        # Create Groups For Source and Destination Database Info
        grpQueries = QtWidgets.QGroupBox()
        grpQueries.setGeometry(baseWidget.rect())
        grpQueries.setObjectName("grp" + str(name).lower())
        grpQueries.setTitle(_translate("MainWindow", name.title()))
        grpQueries.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, True, False, CommonFunctions.iFontSize))

        # Connection Form
        connectionForm = QtWidgets.QFormLayout()
        connectionForm.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignLeft)
        grpQueries.setLayout(connectionForm)
        # Add Queries Button
        btnAddQuery = QtWidgets.QPushButton()
        btnAddQuery.setText("Add Query")
        btnAddQuery.setIcon(QtGui.QIcon("./guiWindows/icons/add.png"))
        btnAddQuery.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        btnAddQuery.setFixedSize(150, 25)
        btnAddQuery.clicked.connect(lambda: CommonFunctions.onClickAddQuery(grpQueries))

        wdgButtons = QtWidgets.QWidget()
        layoutButtons = QtWidgets.QHBoxLayout()
        wdgButtons.setLayout(layoutButtons)
        # Remove Queries Button
        btnRemoveQuery = QtWidgets.QPushButton()
        btnRemoveQuery.setText("Remove Selected")
        btnRemoveQuery.setIcon(QtGui.QIcon("./guiWindows/icons/remove.png"))
        btnRemoveQuery.setFixedSize(150, 25)
        btnRemoveQuery.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        btnRemoveQuery.clicked.connect(lambda: CommonFunctions.onClickRemoveCheckedQueries(grpQueries))

        # 	Select All Queries
        btnSelectAllQueries = QtWidgets.QPushButton()
        btnSelectAllQueries.setText("Select All Queries")
        btnSelectAllQueries.setIcon(QtGui.QIcon("./guiWindows/icons/checkall.png"))
        btnSelectAllQueries.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        btnSelectAllQueries.setFixedSize(150, 25)
        btnSelectAllQueries.clicked.connect(lambda: CommonFunctions.onClickSelectAllQueries(grpQueries, True))
        # 	Uncheck All Queries
        btnDeselectAllQueries = QtWidgets.QPushButton()
        btnDeselectAllQueries.setText("Deselect All Queries")
        btnDeselectAllQueries.setIcon(QtGui.QIcon("./guiWindows/icons/uncheckall.png"))
        btnDeselectAllQueries.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        btnDeselectAllQueries.setFixedSize(150, 25)
        btnDeselectAllQueries.clicked.connect(lambda: CommonFunctions.onClickSelectAllQueries(grpQueries, False))
        # connectionForm.addRow(btnSelectAllQueries, btnDeselectAllQueries)
        layoutButtons.addWidget(btnAddQuery)
        layoutButtons.addWidget(btnRemoveQuery)
        layoutButtons.addWidget(btnSelectAllQueries)
        layoutButtons.addWidget(btnDeselectAllQueries)

        connectionForm.addRow(wdgButtons)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(grpQueries)
        scroll.setWidgetResizable(True)
        scroll.setGeometry(baseWidget.rect())
        return scroll

    def setQueriesFilesUi(self, baseWidget):
        print("Queries Ui")
        # Widget
        grpQueriesFilesUI = QtWidgets.QWidget(baseWidget)
        grpQueriesFilesUI.setGeometry(0, 0, ((baseWidget.width() * 80) / 100), 50)
        grpQueriesFilesUI.setObjectName("grpQueriesFilesUI")
        # Add File Tab
        labelQueriesFile = QtWidgets.QLabel("Queries File Path : ", grpQueriesFilesUI)
        labelQueriesFile.setObjectName("labelQueriesFile ")
        labelQueriesFile.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))
        labelQueriesFile.setGeometry(QtCore.QRect(20, 20, 100, 20))
        # Add File Edit Box
        editQueriesFilePath = QtWidgets.QLineEdit(grpQueriesFilesUI)
        editQueriesFilePath.setGeometry(QtCore.QRect(140, 20, ((grpQueriesFilesUI.width() * 80) / 100) - 40, 20))
        editQueriesFilePath.setObjectName("editQueriesFilePath")
        editQueriesFilePath.setFont(CommonFunctions.setFontInfo(CommonFunctions.sFontName, False, False, CommonFunctions.iFontSize))

        # Add File Selection Edit Box
        btnQueriesPath = QtWidgets.QToolButton(grpQueriesFilesUI)
        btnQueriesPath.setObjectName("btnQueriesPath")
        btnQueriesPath.setGeometry(QtCore.QRect(((grpQueriesFilesUI.width() * 80) / 100) + 120, 20, 25, 20))
        btnQueriesPath.setText("...")
        btnQueriesPath.clicked.connect(lambda: self.setQueries())
        return grpQueriesFilesUI

    def setQueries(self):
        filepath = CommonFunctions.getFilePath(self)
        print("Queries Path : " + filepath)
        grpQueriesFilesUI: QtWidgets.QGroupBox = self.findChild(QtWidgets.QGroupBox, "grpQueriesFilesUI")
        # 	Set Path For UI Edit box
        editQueriesFilePath: QtWidgets.QLineEdit = self.findChild(QtWidgets.QLineEdit, "editQueriesFilePath")
        editQueriesFilePath.setText(filepath)
        # Set Data To UI From File
        self.loadDataToUIFromFile(self, filepath)

    def updateQueriesSection(self):
        QtCore.QObjectCleanupHandler().add(self.wdgQueriesView.layout())
        if (self.rdbQueriesFile.isChecked()):
            print("File")
            self.wdgQueries.hide()
            self.wdgQueriesFile.show()
        elif (self.rdbQueriesUI.isChecked()):
            print("UI")
            self.wdgQueriesFile.hide()
            self.wdgQueries.show()

        pass

    def loadDetailsFromFile(self):
        print("Load Details From File")
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Properties File", "", "Properties Files (*.ini)")
        # Set Data From File To UI
        self.loadDataToUIFromFile(self.windowShown, filePath)

    # Set Data From File To UI
    def loadDataToUIFromFile(self, windowShown: QtWidgets.QWidget, filePath: str, sectionValue: str = ""):
        config = configurations.getInstance(filePath)
        configFile = RawConfigParser()
        configFile.sections()
        configFile.read(filePath)
        # Remove All Existing Queries
        grpQueriesSection: QtWidgets.QGroupBox = windowShown.findChild(QtWidgets.QGroupBox, "grpqueries")
        formLayout = grpQueriesSection.layout()
        bRemoveAllQueries: bool = True
        bRemoveQueriesData = False
        for section in config.getSections():
            if str(section).lower().startswith("query"):
                config.removeSection(section)
        # Setup Data
        for section in configFile.sections():
            name = str(section)
            if sectionValue.lower() in name:
                if name.lower() == "default" or name.lower() == "thread" or name.lower() == "queue":
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
                elif "execution" == name.lower():
                    if configFile.has_option("execution", "resultsFolder"):
                        self.editResultFolder.setText(str(configFile.get("execution", "resultsFolder")))
                        config.addValueToSection("execution", "resultsFolder", self.editResultFolder.text())
                else:
                    print("Set Section Values - " + name)
