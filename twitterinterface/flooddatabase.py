import MySQLdb

def createdatabase():
	conn=MySQLdb.connect(host='localhost',user='root',passwd='')
	cursor = conn.cursor()
	#cursor.execute('Create database Library')
	cursor.execute('use Library')
	cursor.execute('create table floodvictims (idstr varchar(200) primary key,text varchar(200),coords varchar(100))')

def insertintotable(tweet):
	conn=MySQLdb.connect(host='localhost',user='root',passwd='')
	cursor = conn.cursor()
	cursor.execute('use Library')
	#cursor.execute('delete * from floodvictims')
	try:
		cursor.execute('insert into floodvictims values (%s,%s,%s)',(tweet['id_str'],tweet['text'],tweet['coordinates']))
	except:
		pass

if __name__=='__main__':
	createdatabase()





