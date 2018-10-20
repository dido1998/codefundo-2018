import pyodbc
server = 'tcp:codeflood.database.windows.net'
database = 'codeflooddb'
username = 'dido1998@codeflood'
password = 'Manutd789'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("create table test(id number)")
