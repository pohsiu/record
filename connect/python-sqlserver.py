import pyodbc
#use python pyodbc module to connect sql server
#module pyodbc installed by 'pip install pyodbc'

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=adminID\SQLEXPRESS;DATABASE=db;UID=root;PWD=root')
cursor = cnxn.cursor()
cursor.execute('select TOP 10 Asin FROM tablename')
rows = cursor.fetchall()
for row in rows:
  print row.Asin
