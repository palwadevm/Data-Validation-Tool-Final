import datetime
import time

from DataValidationTool.core import Validations
from DataValidationTool.core.configurations import configurations
from DataValidationTool.core import DataSyncQueue

def commandValidationData():
    start = time.time()

    resourcesPath = "G:/Work/Python/GithubRepository/Pycharm/Data-Validation-Tool-Final/Resources/backend/Oracle2SQLServer/"
    resultFolder = "G:/Work/Python/GithubRepository/Pycharm/Data-Validation-Tool-Final/Resources/Results/" + str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")) + "/"
    #######################################################################################################################
    print("Data Validation Tool Command Line Execution")
    # get Instance of the Configuations Class
    config = configurations.getInstance()
    # Add Execution Type as Command Line
    config.addValueToSection("execution", "type", "commandline")
    config.addValueToSection("execution", "resultsFolder", resultFolder)
    # Setup Information for tool
    config.readBaseConfigurations(resourcesPath + "core.ini")
    # Connections
    config.readBaseConfigurations(resourcesPath + "connections.ini")
    # Queries
    config.readBaseConfigurations(resourcesPath + "queries.ini")
    # Initialize the Queue
    dataQueue = DataSyncQueue.getQueueInstance()
    # Execute Validations
    Validations.validateBackend()

    # End Time
    end = time.time()
    print("Execution Time : " + str(end - start))


if __name__ == "__main__":
    commandValidationData()