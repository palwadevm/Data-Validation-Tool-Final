from queue import Queue

from DataValidationTool.core.configurations.configurations import configurations
from DataValidationTool.core.structs.DataNode import DataNode

iWaitTime = 0


class DataSyncQueue:
    # Single Instance
    __queueInstance = None
    __queueData = None

    # Data Queue Single Object initialization
    @staticmethod
    def getQueueInstance():
        if DataSyncQueue.__queueInstance is None:
            DataSyncQueue()
        print("Setting Queue...")
        return DataSyncQueue.__queueInstance

    # Object Initialization
    def __init__(self):
        DataSyncQueue.__queueInstance = self
        if DataSyncQueue.__queueData is None:
            print("Setting Queue")
            global iWaitTime
            configs = configurations.getInstance()
            print('--------------------------------------------------------------------------------------------------')
            print('Setting up data queue with Size : ' + str(configs.getPropertyValue('queue', 'ququeSize')))
            print('--------------------------------------------------------------------------------------------------')
            DataSyncQueue.__queueData = Queue(maxsize=int(configs.getPropertyValue('queue', 'ququeSize'), 10))
            iWaitTime = int(configs.getPropertyValue('queue', 'queueWaitTime'), 10)

    def getQueue(self):
        return DataSyncQueue.__queueData

    def addNodeToQueue(self, dataNode: DataNode):
        DataSyncQueue.__queueData.put(dataNode)

    def size(self):
        return DataSyncQueue.__queueData.qsize()

    def isQueueFull(self):
        return DataSyncQueue.__queueData.full()

    def getFirstNode(self):
        global iWaitTime
        # print("Waiting for the data from queue")
        return DataSyncQueue.__queueData.get(True, iWaitTime)  # Wait for 10 sec if queue is empty

# Pattern Of the Trade Id
# All The Null
