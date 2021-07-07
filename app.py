from flask import Flask, app, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = "45876a1068784ca50cd703bfdf6cf973"

#connecting to MYSQL
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "3672Dorcas."   #db password
app.config['MYSQL_DB'] = "logindb"  #db name

#initialize my SQL
mysql = MySQL(app)

#this is home route
@app.route('/')
def home():
    return render_template('index.html')

#this is login route
@app.route('/login', methods =['GET', 'POST'])
def login():
    message = 'Awaits input'   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']  # Create variables for easy access
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  # Check if account exists using MySQL
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()     # Fetch one record and return result
        if account:                     #if user exist in account
            session['loggedin'] = True  # Create session data, we can access this data in other routes
            session['username'] = username
            session['email'] = account['email']
            session['id'] = account['id']
            message = 'logged in successfully'
            return render_template('index.html', msg= message)
        else:                            # Account doesnt exist or username/password incorrect
            message = 'invalid username and password'
    return render_template('login.html', msg= message)  # Show the login form with message (if any)

#registration route
@app.route('/register', methods =['GET', 'POST'])
def register():
    message = 'Awaits input data...'    # Output message if something goes wrong
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']     # Create variables for easy access
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password ))
        account = cursor.fetchone()
        if account:
            message = 'this account already exists'
        elif not username or not password or not email: # Form is empty... (no POST data)
            message = 'Please fill all fields'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            message = 'You have successfully registered ! you can Login now. '
    elif request.method == 'POST':
        message = 'Please fill out the form'
    return render_template('register.html', msg = message)  # Show registration form with message (if any)

#logout route  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)       # Remove session data, this will log the user out
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))
