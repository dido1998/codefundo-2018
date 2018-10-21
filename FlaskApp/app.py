from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import twitterinterface.geocoding as gd
import twitterinterface.cluster as cl

from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

app = Flask(__name__)
mysql = MySQL()
 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'amit'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



@app.route("/")


def main():
    return render_template('index.html')

@app.route('/checkStatus')
def showSignUp():
    return render_template('status.html')

@app.route("/Authenticate")
def Authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return "Logged in successfully"


@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        _name = request.form['orangeForm-name']
        _email = request.form['orangeForm-email']
        _password = request.form['orangeForm-pass']
        ##add adress code here and store in variable _address
        print(_name)
        print(_email)
        print(_password)
        if _name and _email and _password:
            print("Reached")
            conn = mysql.connect()
            cursor = conn.cursor()

            _hashed_password = generate_password_hash(_password)

            print(_hashed_password)
            #cursor.callproc('sp_createUser',(_name,_email,_password))
            #data = cursor.fetchall()
            lat,lng=gd.geocode(_address)
            insertngo(_name,_email,_password,lat,lng)

            if len(data) is 0:
                print('finally')
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                print('error')
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
        print ('lol')
    finally:
        cursor.close() 
        conn.close()
#aniket
def create():
	cursor.execute('create table user (id auto increment,lat numeric,lon numeric,resuceid varchar(20))')
	cursor.execute('create table ngo (id int auto increment,email varchar(20),name varchar(20),password varchar(20),lat numeric,lon numeric)')
    cursor.execute('create table ngocurr(id int, rescuelat number,rescuelon number,rescueid int)')

def insertngo(name,email,password,lat,lng):
	cursor.execute('insert into ngo(email,name,password,lat,lon) values('+(email+','+name+','+password+','+lat+','+lon)+')')

def insertuser(idstr,lat,lon):
	cursor.execute('insert into user(lat,lon) values('+lat+','+lon+')')

def insertngocurr(ids,rescuelat,rescuelon):
    cursor.execute('insert into ngocurr(id,lat,lon) values('+ids+','+lat+','+lon+')')

def insertrescuengo(idstr,resuceid):
	cursor.execute('insert into user (rescueid) values ('+rescueid+') where id='+idstr)

def delentryuser(idstr):
	cursor.execute('delete from user where id='+idstr)
    cursor.execute('delete from ngocurr where rescueid='+idstr)
    #####
    """
    make ngo go after next relevent user
    """

    #######
def deleteentryngo(idstr):
	cursor.execute('delete from ngo where id='+idstr)

def updatelocngo(idstr,newlat,newlong):
    cursor.execute('update ngo set lat='+newlat+' where id='+idstr)
    cursor.execute('update ngo set lon='+newlong+' where id='+idstr)
    cursor.execute('select * from ngocurr where id='+idstr)
    people=cursor.fetchall()
    for p in people:
        dist=haversine(p[2],p[1],newlong,newlat)
        if dist<1:
            delentryuser(p[0])
def checkusertable():
    cursor.execute('select * from user')
    data=cursor.fetcall()
    if(len(data)>0):
        cursor.execute('select * from ngo')
        datango=cursor.fetchall()
        cl.precluster(data,datango)
#aniket

if __name__ == "__main__":
    app.run()
#https://maps.googleapis.com/maps/api/geocode/json?' +
#                  'latlng=' + latitude + ',' + longitude + '&key=' + 
#                  'AIzaSyA2Fn0J57CMn5od7EHQQWlOoEAGxKK8kqo'