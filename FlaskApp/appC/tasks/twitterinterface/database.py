from flaskext.mysql import MySQL
from appC.tasks.twitterinterface import cluster as cl

mysql = MySQL()
conn=None
cursor=None
def init(app):
	global cursor,conn,mysql
	print("initialized!!!!")
	mysql.init_app(app)
	conn = mysql.connect()
	cursor= conn.cursor()
	print(cursor)

def commit():
	global conn
	conn.commit()
def create():
    cursor.execute('create table user (id auto increment,lat numeric,lon numeric,resuceid varchar(20))')
    cursor.execute('create table ngo (id int auto increment,email varchar(20),name varchar(20),password varchar(20),lat numeric,lon numeric)')
    cursor.execute('create table ngocurr(id int, rescuelat number,rescuelon number,rescueid int)')

def insertngo(name,email,password,lat,lng):
    global cursor
    cursor.execute("INSERT INTO ngo (email,name,pass,lat,lon) VALUES(%s,%s,%s,%s,%s)",(_email,_name,_password,str(lat),str(lon)))

def insertuser(idstr,lat,lon):
    cursor.execute("INSERT INTO user (lat,lon) VALUES(%s,%s)",(str(lat),str(lon)))
    

def insertngocurr(ids,rescuelat,rescuelon,rescueid):
    global cursor
    cursor.execute("SELECT COUNT(1) FROM ngo_saver WHERE rescue_id = {};".format(rescueid))
    if cursor.fetchone()[0]:
        return
    cursor.execute("INSERT INTO ngo_saver (id, rescue_lat, rescue_lon, rescue_id) VALUES(%s,%s,%s,%s)",(str(ids),str(rescuelat),str(rescuelon),str(rescueid)))
    
def insertrescuengo(idstr,resuceid):
    global cursor
    print(type(resuceid))
    print(type(idstr))
    cursor.execute("UPDATE user set rescue_id = {} where id = {}".format(int(resuceid),int(idstr)))

def delentryuser(idstr):
    global cursor
    cursor.execute('delete from user where id='+idstr)
    cursor.execute('delete from ngo_saver where rescueid='+idstr)
    #####
    """
    make ngo go after next relevent user
    """

    #######
def deleteentryngo(idstr):
    global cursor
    cursor.execute('delete from ngo where id='+idstr)

def updatelocngo(idstr,newlat,newlong):
    global cursor
    cursor.execute('update ngo set lat=%s where id=%d'+(newlat,idstr))
    cursor.execute('update ngo set lon=%s where id=%d'+(newlong,idstr))
    cursor.execute('select * from ngo_save where id='+idstr)
    people=cursor.fetchall()
    for p in people:
        dist=haversine(double(p[2]),double(p[1]),newlong,newlat)
        if dist<1:
            delentryuser(p[0])
def checkusertable():
    global cursor
    cursor.execute('select * from user')
    data=cursor.fetchall()
    if(len(data)>0):
        newdata=[]
        for i,d in enumerate(data):
            newdata.append(list(data[i]))
            print(type(newdata[i]))
            newdata[i][1]=float(d[1])
            newdata[i][2]=float(d[2])
        cursor.execute('select * from ngo')
        datango=cursor.fetchall()
        newdatango=[]
        for i,d in enumerate(datango):
            newdatango.append(list(datango[i]))
            newdatango[i][4]=float(d[4])
            newdatango[i][5]=float(d[5])
        cl.precluster(newdata,newdatango)
#aniket
