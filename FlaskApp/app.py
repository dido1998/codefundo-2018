from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import json
import urllib.request

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
        _address = request.form['orangeForm-adr']
        response=urllib.request.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address='+_address+'&key=AIzaSyA2Fn0J57CMn5od7EHQQWlOoEAGxKK8kqo')
        html=response.read()
        html=html.decode("utf-8") 
        res=json.loads(html)
        lat, lon = res['results'][0]['geometry']['location']['lat'],res['results'][0]['geometry']['location']['lng']
        print(lat, lon)
        #lat, lon =22.22,21.32
        print('aniket')
        print (type(lon))
        print(_name)
        print(_email)
        print(_password)    
        if _name and _email and _password:
            print("Reached")
            conn = mysql.connect()
            cursor = conn.cursor()

            #cursor.execute('insert into ngo(email,name,pass,lat,lon) values('+(_email+','+_name+','+_password+','+lat+','+lon)+')')
            cursor.execute("INSERT INTO ngo (email,name,pass,lat,lon) VALUES(%s,%s,%s,%d,%d)",(_email,_name,_password,lat,lon))
            print('coolllllll')
            #cursor.callproc('sp_createUser',(_name,_email,_password))
            data = cursor.fetchall()
            print ('str(data[0])')
            if len(data) is 0:
                print('finally')
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                print(json.dumps({'error':str(data[0])}))

                with open('data.json', 'w') as outfile:
                    json.dump(str(data[0]), outfile)
                #return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        print (str(e))
        return json.dumps({'error':str(e)})
        
    finally:
        cursor.close() 
        conn.close()

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
