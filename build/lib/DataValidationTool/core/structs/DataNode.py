from collections import defaultdict

from DataValidationTool.core.structs.eMatchStatus import Match_Status


class DataNode:
    'Common base class for all employees'
    nodesCount = 0

    def __init__(self, key, dataRecords: dict, dataSource: str):
        self.key = key
        self.dataRecords = defaultdict(list)
        self.dataRecords[dataSource].append(dataRecords)
        if dataSource.lower() == "source":
            self.isAvailableInSrc = True
        else:
            self.isAvailableInSrc = False

        if dataSource.lower() == "destination":
            self.isAvailableInDest = True
        else:
            self.isAvailableInDest = False

        self.matchStatus = Match_Status.MISSING_DATA
        self.left = None
        self.right = None
        self.height = 1
        self.failedColumns = ["datakey"]

    def getData(self):
        return self.dataRecords

    def getKey(self):
        return self.key

    def getSource(self):
        if self.isAvailableInSrc:
            return 'source'
        elif self.isAvailableInDest:
            return 'destination'
        else:
            return 'invalid'

    def getMatchStatus(self):
        return self.matchStatus

    def getleft(self):
        return self.left

    def getright(self):
        return self.right

    def getheight(self):
        return self.height

    # Set Node to left noe
    def setleft(self, node):
        self.left = node
        return

    # Set node to Right end
    def setright(self, node):
        self.right = node
        return

    # set height
    def setheight(self, height):
        self.height = height
        return

    # add data to existng list
    def add_data(self, data):
        self.failedColumns = []
        for dataSource in data:
            for dataDicts in data[dataSource]:
                self.dataRecords[dataSource].append(dataDicts)
        return

    def updateDataSource(self, sourceName: str):
        if sourceName.lower() == 'source':
            self.isAvailableInSrc = True
        elif sourceName.lower() == 'destination':
            self.isAvailableInDest = True

    def updateMatchStatus(self):

        if self.dataRecords.__len__() == 1:
            self.matchStatus = Match_Status.MISSING_DATA
        elif self.dataRecords.__len__() > 1:
            self.matchStatus = Match_Status.MATCHED
            keySet = set().union(*(data.keys() for data in self.dataRecords["source"])).union(set().union(*(data.keys() for data in self.dataRecords["destination"])))
            # TODO -- Duplicate Records management Pending
            for key in keySet:
                try:
                    val1 = self.dataRecords["source"][0].get(key)
                    # self.dataRecords[0].get(key)
                    val2 = self.dataRecords["destination"][0].get(key)
                    # self.dataRecords[1].get(key)
                    if val1 != val2:
                        print("****************************************************************************************************************")
                        print("mismatch on data for key - " + self.key)
                        print(key + " : " + val1 + " | " + val2)
                        self.matchStatus = Match_Status.FIELDS_MISMATCH
                        self.failedColumns.append(key)
                        print("****************************************************************************************************************")
                except ValueError:
                    self.matchStatus = Match_Status.FIELDS_MISMATCH

    # def getTypeCastedValue(self, val):
    #     if type(val) == int:
    #         return int(val)
    #     elif type(val) == float:
    #         return float("{0:.2f}".format(val))
    #     elif type(val) == datetime.datetime:
    #         return datetime.datetime.strftime(val, '%Y-%m-%d %I:%M %p')
    #     elif type(val) == str:
    #         return str(val)
    #     else:
    #         return val
