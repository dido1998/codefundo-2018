from flaskext.mysql import MySQL


mysql = MySQL()
conn=None
cursor=None
def init(app):
	mysql.init_app(app)
	conn = mysql.connect()
	cursor= conn.cursor()


def create():
    cursor.execute('create table user (id auto increment,lat numeric,lon numeric,resuceid varchar(20))')
    cursor.execute('create table ngo (id int auto increment,email varchar(20),name varchar(20),password varchar(20),lat numeric,lon numeric)')
    cursor.execute('create table ngocurr(id int, rescuelat number,rescuelon number,rescueid int)')

def insertngo(name,email,password,lat,lng):
    cursor.execute("INSERT INTO ngo (email,name,pass,lat,lon) VALUES(%s,%s,%s,%s,%s)",(_email,_name,_password,str(lat),str(lon)))

def insertuser(idstr,lat,lon):
    cursor.execute("INSERT INTO user (lat,lon) VALUES(%s,%s)",(str(lat),str(lon)))
    

def insertngocurr(ids,rescuelat,rescuelon,rescueid):
    cursor.execute("INSERT INTO ngo_saver (id, rescue_lat, rescue_lon, rescue_id) VALUES(%s,%s,%s,%s)",(str(ids),str(rescuelat),str(rescuelon),str(rescue_id)))
    
def insertrescuengo(idstr,resuceid):
    cursor.execute("UPDATE user set rescue_id = %d where id = %d",(rescueid,idstr))

def delentryuser(idstr):
    cursor.execute('delete from user where id='+idstr)
    cursor.execute('delete from ngo_saver where rescueid='+idstr)
    #####
    """
    make ngo go after next relevent user
    """

    #######
def deleteentryngo(idstr):
    cursor.execute('delete from ngo where id='+idstr)

def updatelocngo(idstr,newlat,newlong):
    cursor.execute('update ngo set lat=%s where id=%d'+(newlat,idstr))
    cursor.execute('update ngo set lon=%s where id=%d'+(newlong,idstr))
    cursor.execute('select * from ngo_save where id='+idstr)
    people=cursor.fetchall()
    for p in people:
        dist=haversine(double(p[2]),double(p[1]),newlong,newlat)
        if dist<1:
            delentryuser(p[0])
def checkusertable():
    cursor.execute('select * from user')
    data=cursor.fetcall()
    if(len(data)>0):
        for d in data:
            d[1]=double(d[1])
            d[2]=double(d[2])
        cursor.execute('select * from ngo')
        datango=cursor.fetchall()
        for d in datango:
            d[4]=double(d[4])
            d[5]=double(d[5])
        cl.precluster(data,datango)
#aniket
