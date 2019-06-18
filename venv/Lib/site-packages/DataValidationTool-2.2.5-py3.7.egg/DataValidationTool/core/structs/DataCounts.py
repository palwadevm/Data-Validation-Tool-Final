class DataProgressCounts:
    __instance = None
    __TotalCounts = 0
    __CurrentProgress = 0

    @staticmethod
    def resetCounts():
        DataProgressCounts.__instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DataProgressCounts.__instance == None:
            DataProgressCounts()
        return DataProgressCounts.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DataProgressCounts.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DataProgressCounts.__instance = self

    def getTotalCount(self):
        return self.__TotalCounts

    def getCurrentProgress(self):
        return self.__CurrentProgress

    def setTotalCount(self, count):
        self.__TotalCounts += count

    def setCurrentCount(self, count):
        self.__CurrentProgress += count
