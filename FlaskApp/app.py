from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash


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
            insertngo(name,email,password)

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
    cursor.execute('create table ngocurr(id int, rescuelat number,rescuelon number)')

def insertngo(name,email,password,lat,lng):
	cursor.execute('insert into ngo(email,name,password,lat,lon) values('+(email+','+name+','+password+','+lat+','+lon)+')')
def insertuser(idstr,lat,lon):
	cursor.execute('insert into user(lat,lon) values('+lat+','+lon+')')
def insertngocurr(ids,rescuelat,rescuelon):
    cursor.execute('insert into user(id,lat,lon) values('+ids+','+lat+','+lon+')')


def insertrescuengo(idstr,resuceid):
	cursor.execute('insert into user (rescueid) values ('+rescueid+') where idstr='+idstr)
def delentryuser(idstr):
	cursor.execute('delete from user where id='+idstr)
def deleteentryngo(idstr):
	cursor.execute('delete from ngo where id='+idstr)
#aniket

if __name__ == "__main__":
    app.run()
#https://maps.googleapis.com/maps/api/geocode/json?' +
#                  'latlng=' + latitude + ',' + longitude + '&key=' + 
#                  'AIzaSyA2Fn0J57CMn5od7EHQQWlOoEAGxKK8kqo'