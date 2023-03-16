from flask import Flask, render_template, request, redirect, url_for, session, flash, Response, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import logging

app = Flask(__name__)

FLASK_APP = app;
FLASK_DEBUG = 1;

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'PBDVPBDEGROUP5PROJECT'
app.config['MYSQL_DB'] = 'tutorhive'


database = MySQL(app)

@app.route('/')

@app.route('/sign_in', methods =['GET', 'POST'])
def sign_in():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = database.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM account WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
			return render_template('sign_in.html', msg = msg)
	return render_template('sign_in.html', msg = msg)

@app.route('/sign_out')
def sign_out():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('sign_in'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = database.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM account WHERE username = % s AND password = % s AND email = % s', (username, password, email, ))
		account = cursor.fetchone()
		if account:
			msg = 'This account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO account VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			database.connection.commit()
			msg = 'You have successfully registered !'
			return render_template('register.html', msg = msg)
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
		return render_template('register.html', msg = msg)
	return render_template('register.html', msg = msg)
@app.route('/profile')
def profile():
    return render_template('profile.html')
@app.route('/studentinfo', methods =['GET', 'POST'])
def studentinfo():
	return render_template('studentinfo.html')
@app.route('/email')
def email():
	msg = 'Email sent'
	return render_template('email.html', msg = msg)
@app.route('/jobs')
def jobs():
	return render_template('jobs.html')
@app.route('/tutorOpportunity')
def tutorOpportunity():
	cursor = database.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM tutor_jobs')
	info = cursor.fetchall()
	return render_template('tutorOpportunity.html', info=info)
@app.route('/taOpportunity')
def taOpportunity():
	cursor = database.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM ta_jobs')
	info = cursor.fetchall()
	return render_template('taOpportunity.html', info=info)
@app.route('/recieved')
def recieved():
	return render_template('recieved.html')