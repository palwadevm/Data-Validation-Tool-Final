# #!/usr/bin/pythodatabasen
#
# # import cx_Oracle
# #
# # conn = cx_Oracle.connect('palwadevm/VP$yne55@orcl.cd0ta02os5b7.ap-south-1.rds.amazonaws.com:1521/ORCL')
# # curs = conn.cursor()
# # curs.arraysize = 50
# # curs.execute("Select * From UserDetails")
# # for row in curs:
# # 	print(row)
# #
# # curs.close()
# # conn.close()
# import platform
#
# print(platform.system())
# #
import os

file_extension = os.path.splitext('G:\Work\Python\GithubRepository\Pycharm\Data-Validation-Tool-Final\trash\oracleConnector.py')[1]
print(file_extension)
#
# connstr = "Driver={Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)};DBQ=C:\\Users\\Vaijnath\\Desktop\\folders\\Barclays\\Informtion.xlsx;"
# conn = pyodbc.connect(connstr, autocommit=True)
#
# cursor = conn.cursor()
# query = "Select * From [Details$]"
# cursor.execute(query)
# for line in cursor:
#     print(line)
