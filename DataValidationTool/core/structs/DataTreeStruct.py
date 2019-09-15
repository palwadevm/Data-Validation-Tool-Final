from DataValidationTool.core.structs import DataOperations
from DataValidationTool.core.structs.DataCounts import DataProgressCounts
from DataValidationTool.core.structs.DataNode import DataNode
from DataValidationTool.core.structs.DataOperations import RecordsCounter


# e = DataNode('Test',{'Data':'Record'},'source')
# print(e.getData)

class DataTreeStructure:
	__queueTreeInstance = None
	__root = None
	__DataProgress = DataProgressCounts.getInstance()

	# Data Queue Single Object initialization
	@staticmethod
	def treeInitialize():
		if DataTreeStructure.__queueTreeInstance is None:
			DataTreeStructure()
		return DataTreeStructure.__queueTreeInstance

	# Object Initialization
	def __init__(self):
		DataTreeStructure.__queueInstance = self

	def height(self):
		return DataOperations.getheight(DataTreeStructure.__root)

	def insert_dataNode(self, dataNode: DataNode):
		# print(dataNode.getSource() + ' Insert To Compare : ' + "\nKey - " + dataNode.getKey() + "\nData" + str(dataNode.getData()))
		DataTreeStructure.__root = DataOperations.insertDataNode(self.__root, dataNode)
		DataTreeStructure.__DataProgress.setCurrentCount(1)
		# print(DataTreeStructure.__DataProgress.getCurrentProgress())
		return DataTreeStructure.__root

	def printTree(self):
		DataOperations.printCurrentTree(DataTreeStructure.__root, 0)

	def getRecordsWithState(self, recordsState: set, folderName: str = ""):
		RecordsCounter.statusRecordsCount = 0

		fileName = folderName + str("_".join([state.name for state in recordsState])) + ".json"
        # while (not path.exists(fileName)):
        # 	fileName = folderName + str("_".join([state.name for state in recordsState]))+ ".json"
		reportJson = open(fileName, mode='a+', encoding='utf-8')
		reportJson.write("{\"" + "_".join(rec.name for rec in recordsState) + "\": [")
		DataOperations.bItemAdded = True
		recCount = DataOperations.getRecordsWithStatus(DataTreeStructure.__root, recordsState, reportJson)
		reportJson.write("]}")
		reportJson.close()
		return recCount

	# Computes the number of nodes in tree
	def size(self, node):
		if node is None:
			return 0
		else:
			return (self.size(node.left) + 1 + self.size(node.right))

	def resetTree(self):
		DataTreeStructure.__queueInstance = None
		DataTreeStructure.__root = None
		DataProgressCounts.resetCounts()
		pass
