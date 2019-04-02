import json
import sys

from PyQt5 import QtCore, QtWidgets

filename = "/home/dev/Development/Python/Data-Validation-Tool-Final/Resources/Results/2019-03-18 14-07-06/query1/MATCHED.json"
type = "MATCHED"


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, data, parent=None):
        super(Ui_MainWindow, self).__init__(parent=parent)
        self.setupUi(self, data)
        self.show()

    def setupUi(self, MainWindow, data):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(947, 564)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 931, 501))
        self.tableView.setObjectName("tableView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 947, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        table = QtWidgets.QTableWidget()
        d: dict = data[0]
        table.setColumnCount(len(d.keys()))
        table.setRowCount(len(data))
        test = list(d.keys())

        table.setHorizontalHeaderLabels([k for k in d.keys()])
        table.resizeColumnsToContents()
        layoutTestTable = QtWidgets.QHBoxLayout()
        self.tableView.setLayout(layoutTestTable)
        layoutTestTable.addWidget(table)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


def getTableDataFromJson(filePath, type):
    json_file = open(filename, "r")
    data = json.load(json_file)
    returnData = []
    for resultItem in data[type]:
        if resultItem["isAvailableInSrc"]:
            for values in resultItem["source"]:
                temp = {"datafrom": "Source", "datakey": resultItem["datakey"]}
                temp.update(values)
                returnData.append(temp)
        if resultItem["isAvailableInDest"]:
            for values in resultItem["destination"]:
                temp = {"datafrom": "Destination", "datakey": resultItem["datakey"]}
                temp.update(values)
                returnData.append(temp)
    json_file.close()
    return returnData


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    data = getTableDataFromJson(filename, type)
    ui = Ui_MainWindow(data)
    sys.exit(app.exec_())
