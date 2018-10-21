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
            insertngo()

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
	cursor.execute('create table user (id autoincrement,lat numeric,lon numeric,resuceid varchar(20))')
	cursor.execute('create table ngo (id int autoincrement,email varchar(20),name varchar(20),password varchar(20),lat numeric,lon numeric)')
    cursor.execute('create table ngocurr(id int, rescuelat number,rescuelon number)')

def insertngo(idstr,lat,lon):
	cursor.execute('insert into ngo(idstr,lat,lon) values('+(idstr+','+lat+','+lon)+')')
def insertuser(idstr,lat,lon):
	cursor.execute('insert into user(idstr,lat,lon) values('+(idstr+','+lat+','+lon)+')')

def insertrescueuser(idstr,rescuelon,resucelat):
	cursor.execute('insert into ngo(rescuelat,rescuelon) values('+resucelat+','+rescuelon+') where idstr='+idstr)


def insertrescuengo(idstr,resuceid):
	cursor.execute('insert into user (rescueid) values ('+rescueid+') where idstr='+idstr)
def delentryuser(idstr):
	cursor.execute('delete from user where idstr='+idstr)
def deleteentryngo(idstr):
	cursor.execute('delete from ngo where idstr='+idstr)
#aniket

if __name__ == "__main__":
    app.run()
