import pyodbc
#use python pyodbc module to connect sql server
#module pyodbc installed by 'pip install pyodbc'

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=P15684-R700-IDS\SQLEXPRESS;DATABASE=CrawlerDB;UID=james;PWD=james123!')
cursor = cnxn.cursor()
cursor.execute('select TOP 10 Asin FROM Amazon')
rows = cursor.fetchall()
for row in rows:
  print row.Asin
