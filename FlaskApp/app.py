from flask import Flask, render_template, json, request, redirect, url_for, flash, session, escape
from flaskext.mysql import MySQL
import json
import urllib.request
from os import environ
from celery import Celery
from appC.tasks import test 
from appC.tasks.twitterinterface import database,geocoding
app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'amit'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Configs
REDIS_HOST = "0.0.0.0"
REDIS_PORT = 6379
BROKER_URL = environ.get('REDIS_URL', "redis://{host}:{port}/0".format(
    host=REDIS_HOST, port=str(REDIS_PORT)))
CELERY_RESULT_BACKEND = BROKER_URL


def make_celery(app):
    # create context tasks in celery
    celery = Celery(
        app.import_name,
        broker=BROKER_URL
    )
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

celery = make_celery(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
mysql.init_app(app)
conn = mysql.connect()
cursor= conn.cursor()

database.init(app)
database.checkusertable()

@app.route("/")
def index():
    task = test.print_hello.delay()
    #task.wait()
    return render_template('index.html')

@app.route('/checkStatus')
def showSignUp():
    return render_template('status.html' )

@app.route('/receiver', methods = ['POST'])
def worker():
    data = request.form['keyword']
    print(data)
    result = data.split(',')
    #print(result)
    if int(result[2])==1:
        print("reached")
        database.insertuser(result[0],result[1])
    ngolat,ngolon=database.getngolatlon(result[0],result[1])
    print("valure")
    print(ngolat)
    print(ngolon)
    # print(result)
    # showSignUp()
    # return redirect(url_for('checkStatus'))
    return result[0]+','+result[1]+','+ngolat+','+ngolon#render_template('status.html',geocode_ngo=geocode_ngo,geocode_user=geocode_user)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    print(session['email'])
    if 'email' in session:
        lat,lon,lat2,lon2=database.getlatlongofuserandngo(session['email'])
        print('----------')
        if lat==None:
            address_user="You're free currently"
            distance="0.0"
            geocode_user=0.0,0.0
            geocode_ngo=0.0,0.0
            username_session = escape(session['username']).capitalize()
            return render_template('loginpage.html', session_user_name=username_session,geocode_ngo=geocode_ngo,geocode_user=geocode_user,dist=distance,address_user=address_user  )
        else:
            distance=database.haversine(lon2,lat2,lon,lat)        
            events={}
            events['lat1']=lat
            events['lon1']=lon
            events['lat2']=lat2
            events['lon2']=lon2
            geocode_user=events['lat1'],events['lon1']
            geocode_ngo=events['lat2'],events['lon2']
            address_user=geocoding.reversegeocode(lat,lon)
            username_session = escape(session['username']).capitalize()
            return render_template('loginpage.html', session_user_name=username_session,geocode_ngo=geocode_ngo,geocode_user=geocode_user,dist=distance,address_user=address_user  )

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
    # if 'username' in session:
    #     return redirect(url_for('profile'))
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
                #print('checking session:'+row)
                if password_form == row[0]:
                    #print(password_form,row[0])
                    session['username'] = row[1]
                    session['email']=username_form
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
        database.checkusertable()
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




if __name__ == "__main__":

    app.run()

