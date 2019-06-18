from DataValidationTool.core.structs.DataNode import DataNode

bItemAdded = True


class RecordsCounter:
	statusRecordsCount = 0


def printCurrentTree(root: DataNode, tabSpace: int):
	pfixTabs = ''
	for iTabsCounter in range(tabSpace):
		pfixTabs = pfixTabs + '\t'
	if root is None:
		# print(pfixTabs + ' - EMPTY')
		return
	print(pfixTabs + ' - Key : ' + str(root.getKey()) + ' | ' + str(root.getMatchStatus()) + ' | Data : ' + str(
		root.getData()))
	printCurrentTree(root.getleft(), tabSpace + 1)
	printCurrentTree(root.getright(), tabSpace + 1)


def getRecordsWithStatus(root: DataNode, recordsState: set, fileObj):
	global bItemAdded
	if root is None:
		# print(pfixTabs + ' - EMPTY')
		return
	if root.getMatchStatus() in recordsState:
		try:
			# Write Object To Report File
			data = ""
			for keys, values in root.getData().items():
				for value in values:
					data = data + ("" if data == "" else ",") + "\"{keys}\" : [{value}]"
			fileObj.write((",\n" if bItemAdded is False else "") + "{\"datakey\" : \"" + root.getKey() + "\", "
						  + "\"isAvailableInSrc\": " + str(root.isAvailableInSrc).lower() + ", "
						  + "\"isAvailableInDest\": " + str(root.isAvailableInDest).lower() + ", "
						  + str(data).replace("'", '"') + ", "
						  + "\"failedColumns\":\"" + str("|".join(root.failedColumns)) + "\""
						  + "}")
			RecordsCounter.statusRecordsCount = RecordsCounter.statusRecordsCount + 1
            # if Match_Status.MISSING_DATA != root.getMatchStatus():
            # 	deleteDataNode(root, root.getKey())
			# if Match_Status.MATCHED != root.getMatchStatus():
			#     print('Key : ' + str(root.getKey()) + ' | Available in Source1 : ' + str(
			#         root.isAvailableInSrc) + ' | Available in Source 2 : ' + str(root.isAvailableInDest) + ' | ' + str(
			#         root.getMatchStatus()) + ' | Data : ' + str(root.getData()))
			addTab = 1
			if bItemAdded:
				bItemAdded = False
		except Exception as e:
			print("Exception " + e)
	getRecordsWithStatus(root.getleft(), recordsState, fileObj)
	getRecordsWithStatus(root.getright(), recordsState, fileObj)
	return RecordsCounter.statusRecordsCount


def getheight(node: DataNode):
	if node is None:
		return 0
	return node.getheight()


def max(key1, key2):
	if key1 > key2:
		return key1
	return key2


def rotateLeft(node: DataNode):
	ret = node.getleft()
	node.setleft(ret.getright())
	ret.setright(node)
	h1 = max(getheight(node.getright()), getheight(node.getleft())) + 1
	node.setheight(h1)
	h2 = max(getheight(ret.getright()), getheight(ret.getleft())) + 1
	ret.setheight(h2)
	return ret


def rotateRight(node):
	ret = node.getright()
	node.setright(ret.getleft())
	ret.setleft(node)
	h1 = max(getheight(node.getright()), getheight(node.getleft())) + 1
	node.setheight(h1)
	h2 = max(getheight(ret.getright()), getheight(ret.getleft())) + 1
	ret.setheight(h2)
	return ret


def rlrotation(node):
	node.setleft(rotateRight(node.getleft()))
	return rotateLeft(node)


def lrrotation(node):
	node.setright(rotateLeft(node.getright()))
	return rotateRight(node)


def insertDataNode(rootNode: DataNode, dataNode: DataNode):
	if rootNode is None:
		return dataNode
	# if data key is less or equal and from same source add it to left site
	if (str(dataNode.getKey()) < str(rootNode.getKey())):
		rootNode.setleft(insertDataNode(rootNode.getleft(), dataNode))
		if getheight(rootNode.getleft()) - getheight(rootNode.getright()) == 2:  # an unbalance detected
			if dataNode.getKey() <= rootNode.getleft().getKey():  # new node is the left child of the left child
				rootNode = rotateLeft(rootNode)
			else:
				rootNode = rlrotation(rootNode)  # new node is the right child of the left child
	elif str(dataNode.getKey()) > str(rootNode.getKey()):
		rootNode.setright(insertDataNode(rootNode.getright(), dataNode))
		if getheight(rootNode.getright()) - getheight(rootNode.getleft()) == 2:
			if dataNode.getKey() < rootNode.getright().getKey():
				rootNode = lrrotation(rootNode)
			else:
				rootNode = rotateRight(rootNode)
	elif str(dataNode.getKey()) == str(rootNode.getKey()):
		rootNode.updateDataSource(dataNode.getSource())
		rootNode.add_data(dataNode.getData())
		rootNode.updateMatchStatus()
	rootNode.setheight(max(getheight(rootNode.getright()), getheight(rootNode.getleft())) + 1)
	return rootNode


# Recursive function to delete a node with
# given key from subtree with given root.
# It returns root of the modified subtree.

def deleteDataNode(rootNode: DataNode, key):
	# Step 1 - Perform standard BST delete
	if not rootNode:
		return rootNode

	elif key < rootNode.getKey():
		rootNode.left = deleteDataNode(rootNode.left, key)

	elif key > rootNode.getKey():
		rootNode.right = deleteDataNode(rootNode.right, key)

	else:
		if rootNode.left is None:
			temp = rootNode.right
			rootNode = None
			return temp

		elif rootNode.right is None:
			temp = rootNode.left
			rootNode = None
			return temp

		temp = getMinValueNode(rootNode.right)
		rootNode = temp
		rootNode.right = deleteDataNode(rootNode.right,
										temp.val)

	# If the tree has only one node,
	# simply return it
	if rootNode is None:
		return rootNode

	# Step 2 - Update the height of the
	# ancestor node
	rootNode.height = 1 + max(getheight(rootNode.left),
							  getheight(rootNode.right))

	# Step 3 - Get the balance factor
	balance = getBalance(rootNode)

	# Step 4 - If the node is unbalanced,
	# then try out the 4 cases
	# Case 1 - Left Left
	if balance > 1 and getBalance(rootNode.left) >= 0:
		return rotateRight(rootNode)

	# Case 2 - Right Right
	if balance < -1 and getBalance(rootNode.right) <= 0:
		return rotateLeft(rootNode)

	# Case 3 - Left Right
	if balance > 1 and getBalance(rootNode.left) < 0:
		rootNode.left = rotateLeft(rootNode.left)
		return rotateRight(rootNode)

	# Case 4 - Right Left
	if balance < -1 and getBalance(rootNode.right) > 0:
		rootNode.right = rotateRight(rootNode.right)
		return rotateLeft(rootNode)

	return rootNode


def getMinValueNode(root: DataNode):
	if root is None or root.left is None:
		return root

	return getMinValueNode(root.left)


def getBalance(root: DataNode):
	if not root:
		return 0

	return getheight(root.left) - getheight(root.right)
