from enum import Enum


# Create Enum to Specify Tool Supported Databases
class ConnectionType(Enum):
	select = "Select Database Type"
	Oracle = "Oracle"
	SQLServer = "SQLServer"
	MySQL = "MySQL"
	File = "File"
	MongoDB = "MongoDB"
	HadoopHive = "HadoopHive"


def getConnectionType(connectionType):
	connectionType = connectionType.upper()
	if str(connectionType) == "HADOOPHIVE":
		return ConnectionType.HadoopHive
	elif str(connectionType) == "ORACLE":
		return ConnectionType.Oracle
	elif str(connectionType) == "SQLSERVER":
		return ConnectionType.SQLServer
	elif str(connectionType) == "MYSQL":
		return ConnectionType.MySQL
	elif str(connectionType) == "FILE":
		return ConnectionType.File
	elif str(connectionType) == "MONGODB":
		return ConnectionType.MongoDB
	else:
		return ConnectionType.select
