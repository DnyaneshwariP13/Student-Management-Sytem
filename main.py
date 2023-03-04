
from threading import activeCount
from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import re
import MySQLdb.cursors
from flask_socketio import SocketIO,emit

from staff import staff
from admin import admin
from student import student


app=Flask(__name__)
socketio = SocketIO(app)

app.register_blueprint(staff,url_prefix="/staff")
app.register_blueprint(admin,url_prefix="/admin")
app.register_blueprint(student,url_prefix="/student")


app.secret_key='omkar'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Dnyanu'
app.config['MYSQL_PASSWORD'] = 'Doraemon'
app.config['MYSQL_DB'] = 'student'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


mysql = MySQL(app)  
username2=""
id=0
accoount=""
@app.route('/login/',methods=['GET','POST'])
def login():
    msg=""
    global username2
    global id,account
    if request.method=='POST' and 'username' in request.form and 'password' in request.form and 'type' in request.form:
        username=request.form['username']
        password=request.form['password']
        accounttype=request.form["type"]
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT *FROM ACCOUNTS WHERE username=%s AND PASSWORD=%s AND accountType=%s',(username,password,accounttype))
        account=cursor.fetchone()

        if account:
            session['loggedin']=True
            session['id']=account['id']
            session['username']=account['username']

            username2=account['username']
            id=account['id'] 
            
            if accounttype=="1":
                return render_template('admin_dash.html')
            if accounttype=="2":
                return render_template('staff_dash.html')
            if accounttype=="3":
                return render_template('student_dash.html')
            
            return 'Logged in Successfully!'

        else:
            msg='Incorrect username or password!'

    
    
    return render_template("index.html",msg=msg)
    #return ids

@app.route('/logout/')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    
    if request.method=='POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
        accounttype=request.form['type']

        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account=cursor.fetchone()

        if account:
            msg='Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg='Invalid Email address'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s,%s)', (username, password, email,accounttype))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method=='POST':
        msg="Please fill out the form!"

    return render_template('register.html',msg=msg)


@app.route( '/' )
def hello():
    message = "test message"
    print(message)
    socketio.emit('message', message)
    return render_template( './session.html' )

def messageRecived():
  print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json, callback=messageRecived )
 

if __name__=="__main__":
    app.run(debug=True)
    socketio = SocketIO(app,debug=True)


