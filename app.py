from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
FLASK_APP = app;
FLASK_DEBUG = 1;


app.secret_key = 'your secret key'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'PBDVPBDEGROUP5PROJECT'
app.config['MYSQL_DB'] = 'Applicants'


database = MySQL(app)

@app.route('/')
@app.route('/sign_in', methods =['GET', 'POST'])
def sign_in():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = database.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
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
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s AND email = % s', (username, password, email, ))
		account = cursor.fetchone()
		if account:
			msg = 'This account already exists !'
		if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		if not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		if not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			database.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)
@app.route('/profile')
def profile():
    return render_template('profile.html')
@app.route('/quiz')
def quiz():
	return render_template('quiz.html')
@app.route('/opportunities')
def opportunities():
	return render_template('opportunities.html')
def opportunitiesTA():
	return render_template('opportunitiesTA.html')
@app.route('/personality_quiz')
def personality_quiz():
	return render_template('personality_quiz.html')
@app.route('/knowledge_quiz')
def knowledge_quiz():
	return render_template('knowledge_quiz.html')
@app.route('/results')
def results():
	return render_template('results.html')
@app.route('/end', methods =['GET', 'POST'])
def end():
	msg = ''
	if request.method == 'POST' and 'result' in request.form:
		result = request.form['result']
		cursor = database.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM personality_results WHERE P_RESULTS_SCORE = % s', (result, ))
		personality_results = cursor.fetchone()
		if personality_results:
			msg = 'This result already exists !'
		else:
			cursor.execute('INSERT INTO personality_results VALUES (NULL, % s)', (result, ))
			database.connection.commit()
			msg = 'We have captured your result !'
			return render_template('highPResults.html', msg = result)
	elif request.method == 'POST':
		msg = 'Error!'
	return render_template('end.html')
@app.route('/endQuiz')
def endQuiz():
	msg = ''
	if request.method == 'POST' and 'result' in request.form:
		result = request.form['result']
		cursor = database.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM knowledge_results WHERE K_RESULTS_SCORE = % s', (result, ))
		knowledge_results = cursor.fetchone()
		if knowledge_results:
			msg = 'This result already exists !'
		else:
			cursor.execute('INSERT INTO knowledge_results VALUES (NULL, % s)', (result, ))
			database.connection.commit()
			msg = 'We have captured your result !'
			return render_template('highKResults.html', msg = result)
	elif request.method == 'POST':
		msg = 'Error!'
	return render_template('endQuiz.html')
@app.route('/highPResults')
def highPResults():
	return render_template('highPResults.html')
@app.route('/highKResults')
def highKResults():
	return render_template('highKResults.html')
@app.route('/studentinfo', methods =['GET', 'POST'])
def studentinfo():
	msg = ''
	if request.method == 'POST' and 'name' in request.form and 'surname' in request.form and 'snumber' in request.form and 'phone' in request.form and 'email' in request.form and 'gender' in request.form and 'birthday' in request.form and 'ID' in request.form and 'race' in request.form:
		STUDENT_NAME = request.form['name']
		STUDENT_SURNAME = request.form['surname']
		STUDENT_NUMBER = request.form['snumber']
		PHONE_NUMBER = request.form['phone']
		EMAIL = request.form['email']
		GENDER = request.form['gender']
		BIRTH_DATE = request.form['birthday']
		ID = request.form['ID']
		RACE = request.form['race']
		cursor = database.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM student_info WHERE STUDENT_NAME = % s AND STUDENT_SURNAME = % s STUDENT_NUMBER = % s AND PHONE_NUMBER = % s EMAIL = % s AND GENDER = % s BIRTH_DATE = % s AND ID = % s RACE = % s', (name, surname, snumber, phone, email, gender, birthday, ID, race, ))
		student_info = cursor.fetchone()
		if student_info:
			msg = 'This account already exists !'
		else:
			cursor.execute('INSERT INTO student_info VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (name, surname, snumber, phone, email, gender, birthday, ID, race, ))
			database.connection.commit()
			msg = 'We have successfully captured your details !'
	return render_template('studentinfo.html', msg = msg)
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
	if request.method == 'POST':
		PROOF = request.files['Prooffile']
		RECORD = request.files['Recordfile']
		ID_UPLOAD = request.files['IDfile']
		CV = request.files['CVfile']
		OPTIONAL = request.files['Otherfile']
		PROOF.save(secure_filename(PROOF.filename))
		RECORD.save(secure_filename(RECORD.filename))
		ID_UPLOAD.save(secure_filename(ID_UPLOAD.filename))
		CV.save(secure_filename(CV.filename))
		OPTIONAL.save(secure_filename(OPTIONAL.filename))
		msg = 'File uploaded successfully'
	else:
		msg = 'Error!'
		return render_template('studentinfo.html', msg = msg)
	return render_template('studentinfo.html', msg = msg)
@app.route('/notification')
def notification():
	msg = 'Hello, this is a notification message!'
	return render_template('notification.html', msg=msg)
@app.route('/email')
def email():
	return render_template('email.html')
@app.route('/confirm')
def confirm():
	return render_template('confirm.html')