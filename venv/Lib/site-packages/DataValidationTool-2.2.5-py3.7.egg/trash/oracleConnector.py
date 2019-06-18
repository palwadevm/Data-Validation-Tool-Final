#!/usr/bin/pythodatabasen

# import cx_Oracle
#
# conn = cx_Oracle.connect('palwadevm/VP$yne55@orcl.cd0ta02os5b7.ap-south-1.rds.amazonaws.com:1521/ORCL')
# curs = conn.cursor()
# curs.arraysize = 50
# curs.execute("Select * From UserDetails")
# for row in curs:
# 	print(row)
#
# curs.close()
# conn.close()
import platform

print(platform.system())
