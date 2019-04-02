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
    print(pfixTabs + ' - Key : ' + str(root.getKey()) + ' | ' + str(root.getMatchStatus()) + ' | Data : ' + str(root.getData()))
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
                    data = data + ("" if data == "" else ",") + f"\"{keys}\" : [{value}]"

            fileObj.write((",\n" if bItemAdded is False else "") + "{\"datakey\" : \"" + root.getKey() + "\", "
                          + "\"isAvailableInSrc\": " + str(root.isAvailableInSrc).lower() + ", "
                          + "\"isAvailableInDest\": " + str(root.isAvailableInDest).lower() + ", "
                          + str(data).replace("'", '"') + ", "
                          + "\"failedColumns\":\"" + str("|".join(root.failedColumns)) + "\""
                          + "}")
            RecordsCounter.statusRecordsCount = RecordsCounter.statusRecordsCount + 1
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
