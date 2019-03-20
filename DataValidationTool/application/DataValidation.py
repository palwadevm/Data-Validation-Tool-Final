import sys
import tempfile

from PyQt5 import QtWidgets

# from application.guiWindows.MainWindow import DataValidationWindow
from DataValidationTool.application.guiWindows.DataValidationWindow import DataValidationWindow
from DataValidationTool.core.configurations import configurations

if __name__ == "__main__":
    # Create Instance Of Configurations
    config = configurations.getInstance()
    config.addValueToSection("execution", "type", "application")
    config.addValueToSection("execution", "resultsFolder", tempfile.gettempdir() + "/DVT/Results/")
    config.addValueToSection("execution", "maxresultrows", "1000")
    config.readBaseConfigurations()
    app = QtWidgets.QApplication(sys.argv)
    ui = DataValidationWindow()
    sys.exit(app.exec_())
