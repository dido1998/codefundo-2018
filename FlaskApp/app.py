from flask import Flask, render_template, json, request, redirect, url_for, flash, session, escape
from flaskext.mysql import MySQL
import json
import urllib.request
from twitterinterface import tweetextract,geocoding
app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'amit'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
mysql.init_app(app)

conn = mysql.connect()
cursor= conn.cursor()


@app.route("/")
def index():
    tweetextract.gettweetbytag()
    return render_template('index.html')

@app.route('/checkStatus')
def showSignUp():
    return render_template('status.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('loginpage.html', session_user_name=username_session)
    return redirect(url_for('index'))
    #return render_template('loginpage.html')

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

@app.route('/Login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username_form  = request.form['login-email']
        password_form  = request.form['login-pass']
        print(username_form)
        print("Reached")
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(1) FROM ngo WHERE email = %s;",[username_form]) # CHECKS IF USERNAME EXSIST
        if cursor.fetchone()[0]:
            print('got value')
            cursor.execute("SELECT pass,name FROM ngo WHERE email = %s;", [username_form]) # FETCH THE HASHED PASSWORD
            for row in cursor.fetchall():
                print(row)
                if password_form == row[0]:
                    #print(password_form,row[0])
                    session['username'] = row[1]
                    #print(username)
                    return redirect(url_for('profile'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
    return render_template('index.html', error=error)


@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        _name = request.form['orangeForm-name']
        _email = request.form['orangeForm-email']
        _password = request.form['orangeForm-pass']
        _address = request.form['orangeForm-adr']
        # response=urllib.request.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address='+_address+'&key=AIzaSyA2Fn0J57CMn5od7EHQQWlOoEAGxKK8kqo')
        # html=response.read()
        # html=html.decode("utf-8") 
        # res=json.loads(html)
        # lat, lon = res['results'][0]['geometry']['location']['lat'],res['results'][0]['geometry']['location']['lng']
        #print(lat, lon)
        lat,lon=geocoding.geocode(_address)
        #lat, lon =22.22,21.32
        # print('aniket')
        #print (type(lon))
        print(_name)
        print(_email)
        print(_password)    
        if _name and _email and _password:
            # print("Reached")
            # conn = mysql.connect()
            # cursor = conn.cursor()
            cursor.execute("INSERT INTO ngo (email,name,pass,lat,lon) VALUES(%s,%s,%s,%s,%s)",(_email,_name,_password,str(lat),str(lon)))
            print('coolllllll')
            data = cursor.fetchall()
            print ('str(data[0])')
            if len(data) is 0:
                print('finally')
                conn.commit()
                return "You have Signed Up Successfully"
            else:
                print(json.dumps({'error':str(data[0])}))

                return str(data[0])
        else:
            return "Enter the required Fields"
            #return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        print (str(e))
        return "Please Enter the fields correctly"
        #return json.dumps({'error':str(e)})
        
    finally:
        cursor.close() 
        conn.close()

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


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


if __name__ == "__main__":

    app.run()

