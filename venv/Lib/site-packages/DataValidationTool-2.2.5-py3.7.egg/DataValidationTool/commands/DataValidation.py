import datetime
import time

from DataValidationTool.core import Validations
from DataValidationTool.core.configurations.configurations import configurations
from DataValidationTool.core.structs.DataQueue import DataSyncQueue


def commandValidationData(resourcesPath="", resultFolder=""):
    start = time.time()

    if resourcesPath == "":
        resourcesPath = "/home/dev/Development/Python/Data-Validation-Tool-Final-master/Resources/backend/SQLServer2MongoDB/"
    if resultFolder == "":
        resultFolder = "/home/dev/Development/Python/Data-Validation-Tool-Final-master/Resources/Results/"
    #######################################################################################################################
    print("Data Validation Tool Command Line Execution")
    # get Instance of the Configuations Class
    config = configurations.getInstance()
    # Setup Information for tool
    config.readBaseConfigurations(resourcesPath + "core.ini")
    # Connections
    config.readBaseConfigurations(resourcesPath + "connections.ini")
    # Queries
    config.readBaseConfigurations(resourcesPath + "queries.ini")

    # Add Execution Type as Command Line
    config.addValueToSection("execution", "type", "commandline")
    config.addValueToSection("execution", "resultsFolder", config.getPropertyValueOrDefaultValue("resultsFolder", "resultsFolder", resultFolder) + str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")) + "/")

    # Initialize the Queue
    dataQueue = DataSyncQueue.getQueueInstance()
    # Execute Validations
    Validations.validateBackend()

    # End Time
    end = time.time()
    print("Execution Time : " + str(end - start))


if __name__ == "__main__":
    commandValidationData()
