from flask import Flask, session, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
from emails import *
import hashlib
import sqlite3
import random
import time


COURSES = sorted([
	'Foundations of Literature',
	'Acting',
	'American Literature',
	'Creative Nonfiction',
	'Asian American Literature',
	'Writing to Make Change',
	'Poetry',
	'Writers Workshop',
	'AP English – American Literary History',
	'AP English – Defining American Voices',
	'AP English – Contemporaries & Classics',
	'AP English – American Places & Perspectives',
	'AP English – Great Books',
	'AP English – Society & Self',
	'Freshman Composition',
	'Existentionalism',
	'Science Fiction',
	'Shakespearean Literature',
	'Writing in the World',
	'Women\'s Voices in Literature',
	'Leadership and Decision Making'
])

TEACHERS = {
	'Maura Dwyer': 'dwyer',
	'Eric Ferencz': 'eferencz2',
	'Katherine Fletcher': 'msfletcher',
	'Hugh Francis': 'hfrancis',
	'Kerry Garfinkel': 'kgarfin',
	'Eric Grossman': 'mr.grossman',
	'Dermot Hannon': 'hannon',
	'Mark Henderson': 'mhenderson',
	'Minkyu Kim': 'mkim24',
	'Katherine Kincaid': 'kkincaid',
	'David Mandler': 'dmandler',
	'Kim Manning': 'kmanning',
	'Rosa Mazzurco': 'ms.mazzurco',
	'Emily Moore': 'emoore',
	'Emilio Nieves': 'enieves',
	'Sophie Oberfield': 'oberfield',
	'Alicia Pohan': 'apohan',
	'Julie Sheinman': 'jsheinman',
	'Ellis Staley': 'estaley',
	'Lauren Stuzin': 'lstuzin',
	'Annie Thoms': 'athoms',
	'Megan Weller': 'mweller',
	'Alice Yang': 'ayang',
	'Sarah Lifson': 'slifson',
}

for teach in TEACHERS:
	TEACHERS[teach] = 'gthompson30'

app = Flask(__name__)
app.secret_key = 'bigchunguslol'

def get_database():
	db = sqlite3.connect('app/data.db', check_same_thread=False)
	c = db.cursor()

	return c, db

def get_user_from_session():
	c, db = get_database()

	if session['usertype'] == 'editor':
		c.execute(f"SELECT rowid, * FROM editors WHERE email=\"{session['username']}\";")
	elif session['usertype'] == 'mentee':
		c.execute(f"SELECT rowid, * FROM mentees WHERE email=\"{session['username']}\";")
	else:
		print("ERROR IS NEITHER EDITOR NOR MENTEE?")
		return

	resp = c.fetchone()

	if resp:
		return resp
	else:
		return None

def get_user(username, usertype):
	c, db = get_database()
	c.execute(f"SELECT * FROM {usertype}s WHERE email=\"{username}\"")
	resp = c.fetchone()

	if resp:
		return resp
	else:
		return None

def get_readable_time(timestamp):
	return datetime.utcfromtimestamp(timestamp).strftime('%a, %b %-d %Y at %-I:%M %p')

def sha_convert(text):
	return hashlib.sha256(text.encode('utf-8')).hexdigest()

# def hash_with_toppings(pwd, salt_length=8):
# 	salt = ''

# 	for i in range(salt_length):
# 		salt += chr(random.randint(97, 122))

# 	pepper = chr(random.randint(97, 122)) # pepper length 1

# 	pwd_with_toppings = pwd + salt + pepper
# 	hashed_pwd_with_toppings = sha_convert(pwd_with_toppings)

# 	return [hashed_pwd_with_toppings, salt]

# def is_valid_password(test_password, correct_password, salt):
# 	for pepper_ascii in range(97, 123):
# 		peppered = sha_convert(test_password + salt + chr(pepper_ascii))

# 		if peppered == correct_password:
# 			return True

# 	return False

@app.route('/')
def index():
	loggedin = False
	if session:
		loggedin = True
	return render_template('static_pages/landing.html', loggedin=loggedin)

@app.route('/about')
def about():
	c, db = get_database()

	c.execute(f"SELECT rowid, * FROM editors;")
	all_editors = c.fetchall()
	all_editors = sorted(all_editors, key=lambda editor: editor[6])[::-1]

	return render_template('static_pages/about.html', editors=all_editors, usertype=session['usertype'])

@app.route('/credits', methods=['GET'])
def view_hours():
	c, db = get_database()

	current_user = get_user_from_session()
	if not current_user:
		flash('You are not logged in! Please log in to access this page.', 'warning')
		return redirect('/')

	c.execute(f"SELECT * FROM requests WHERE editor=\"{session['username']}\" AND request_status=3;")
	num_credits = len(c.fetchall())

	c.execute(f"SELECT rowid, * FROM editors;")
	all_editors = c.fetchall()
	all_editors = sorted(all_editors, key=lambda editor: editor[6])[::-1]

	return render_template('editor/hours.html', hours=current_user[6], latest=current_user[6], editors=all_editors, credits=num_credits)

# LOGIN METHODS

@app.route('/editor_login', methods=['GET'])
@app.route('/mentee_login', methods=['GET'])
def login_get():
	return render_template('login.html', usertype=f"{request.path[1:7].title()}")

@app.route('/editor_login', methods=['POST'])
@app.route('/mentee_login', methods=['POST'])
def login_post():
	usertype = request.form.get('usertype')
	email = request.form.get('email')
	entered_password = request.form.get('password')

	db = sqlite3.connect('app/data.db', check_same_thread=False)
	c = db.cursor()
	c.execute(f"SELECT password FROM {request.path[1:7]}s WHERE email='{email}'")
	correct_password = c.fetchone()[0]

	if entered_password and check_password_hash(correct_password, entered_password):
		session["username"] = email
		session["usertype"] = usertype
		return redirect('/dashboard')
	else:
		flash('Account does not exist or password is invalid', 'danger')
		return redirect(request.path)

# SIGNUP METHODS

@app.route('/editor_signup', methods=['GET'])
@app.route('/mentee_signup', methods=['GET'])
def signup_get():
	return render_template('signup.html', usertype=request.path[1:7])

@app.route('/mentee_signup', methods=['POST'])
@app.route('/editor_signup', methods=['POST'])
def signup_post():
	usertype = request.path[1:7]
	email = request.form.get('email').lower().replace('@stuy.edu', '')
	password = request.form.get('password')
	fname = request.form.get('fname')
	lname = request.form.get('lname')
	grade = request.form.get('grade')
	pronouns = request.form.get('pronouns')
	hashed_password = generate_password_hash(password, method='sha256')

	c, db = get_database()

	c.execute(f"SELECT * FROM {usertype}s WHERE email='{email}'")
	if len(c.fetchall()) > 0:
		flash('User with that email already exists!', 'danger')
		return redirect(request.path)

	if usertype == 'editor':
		whitelist = [i.strip() for i in open('app/whitelist.csv', 'r').read().split(',')]
		if not(email in whitelist):
			flash('You\'re not on the whitelist! Please contact the writing center admins to be whitelisted.', 'danger')
			return redirect(request.path)

	if usertype == 'editor':
		c.execute(f"INSERT INTO editors VALUES ( '{email}', '{hashed_password}', '{fname}', '{lname}', {grade}, 0, 0, 0, 0, '', '{pronouns}', 0 )")
	elif usertype == 'mentee':
		c.execute(f"INSERT INTO mentees VALUES ( '{email}', '{hashed_password}', '{fname}', '{lname}', {grade}, '', '{pronouns}', 0  )")

	db.commit()

	flash('Check your @stuy.edu email for an email with the subject "Confirm your Writing Center Account", to confirm your account.', 'success')
	e = Emailer()
	e.send(email, [email, fname, usertype], type='signup')

	return redirect(f'/{usertype}_login')

# LOGOUT METHOD

@app.route('/logout', methods=["GET"])
def logout():
	session.pop("username", None)
	return redirect("/")

@app.route('/confirm', methods=["GET"])
def confirm():
	email = request.args['email']
	usertype = request.args['usertype']

	c, db = get_database()
	c.execute(f"UPDATE {usertype}s SET verified=1 WHERE email='{email}'")
	db.commit()

	flash('Successfully verified email! You can log in below.', 'success')

	return redirect(f'/{usertype.lower()}_login')

@app.route('/admin', methods=["GET"])
def admin_login():
	return render_template('admin/login.html')

@app.route('/admin', methods=["POST"])
def admin():
	password = request.form.get('password')
	hashed = sha256(password.encode()).hexdigest()
	editors = User.query.filter_by(usertype='editor')
	editors = editors.all()
	whitelist = ', '.join(open('whitelist.csv').read().split(','))
	print(editors)

	if hashed == os.getenv('ADMIN_PWD'):
		return render_template('admin/dashboard.html', editors=editors, whitelist=whitelist)
	else:
		flash('Invalid password!', 'warning')
		return redirect('/admin')

@app.route('/dashboard', methods=["GET"])
def dashboard():
	if not("username" in session):
		flash('You have not verified your email! Check your email for an email verification link.', 'danger')
		return redirect('/')

	current_user = get_user_from_session()
	c, db = get_database()

	if not current_user:
		flash('You are not logged in! Please log in to access this page.', 'warning')
		return redirect('/')

	if session['usertype'] == 'editor':
		c.execute(f"SELECT rowid, * FROM requests WHERE request_status >= 2 AND editor = \"{current_user[1]}\"")
		finished = c.fetchall()

		c.execute(f"SELECT rowid, * FROM requests WHERE request_status = 1 AND editor = \"{current_user[1]}\"")
		current = c.fetchall()

		c.execute("SELECT rowid, * FROM requests WHERE request_status = 0")
		unselected = c.fetchall()

		no_finished = (len(finished) == 0)
		no_current = (len(current) == 0)
		no_unselected = (len(unselected) == 0)

		total_hours = sum([r[16] for r in finished if r[2] == 3])
		c.execute(f"UPDATE editors SET hours={total_hours} WHERE email=\"{session['username']}\"")
		db.commit()

		return render_template('editor/dashboard.html',
							   fname=current_user[3],
							   lname=current_user[4],
							   unselected=unselected,
							   current=current,
							   finished=finished,
							   no_unselected=no_unselected,
							   no_current=no_current,
							   no_finished=no_finished,
							   num_unfulfilled=len(unselected),
							   get_readable_time=get_readable_time,
							   get_user=get_user,
							   total_hours=total_hours)
	else:
		current_user = get_user_from_session()
		c.execute(f"SELECT rowid, * FROM requests WHERE requester=\"{current_user[1]}\"")
		num_active = 0
		requests = c.fetchall()
		requests = [r for r in requests if r[3] == current_user[1]]

		for r in requests:
			if r[2] < 3:
				num_active += 1

		print(f"SELECT * FROM requests WHERE requester=\"{current_user[1]}\"")

		return render_template('mentee/dashboard.html',
							   fname=current_user[3],
							   lname=current_user[4],
							   requests=requests,
							   num_active=num_active,
							   get_readable_time=get_readable_time,
							   get_user=get_user)

@app.route('/create_piece', methods=['GET'])
def create_piece_get():
	if session['usertype'] == 'mentee':
		return render_template('mentee/make_request.html', current_user=get_user_from_session(), teachers=TEACHERS, courses=COURSES)

	return 'you cant be here'

@app.route('/create_piece', methods=['POST'])
def create_piece_post():
	fname = request.form.get('fname')
	lname = request.form.get('lname')
	grade = int(request.form.get('grade'))
	email = request.form.get('email')
	pronouns = request.form.get('pronouns')
	teacher = request.form.get('teacher')
	course = request.form.get('course')
	period = int(request.form.get('period'))
	help_ = request.form.get('help').replace('"', '""')
	assignment_sheet = request.form.get('assignment_sheet')
	google_doc = request.form.get('google_doc')
	in_person = request.form.get('in_person')
	due_date = request.form.get('due_date')
	due_time = request.form.get('due_time')

	if not in_person:
		in_person = 'off'

	if in_person == 'on':
		in_person = 1
	elif in_person == 'off':
		in_person = 0

	if not due_time:
		due_time = '12:00'

	year, month, day = map(int, due_date.split('-'))
	hour, minute = map(int, due_time.split(':'))
	due_time = datetime(year, month, day, hour, minute)
	due_time = int(time.mktime(due_time.timetuple()))
	cur_time = int(time.time())

	c, db = get_database()
	c.execute("SELECT rowid, * FROM requests;")
	max_request_id = 0

	for row in c.fetchall():
		max_request_id = max(max_request_id, row[1])

	current_user = get_user_from_session()
	c.execute(f'''
		INSERT INTO requests VALUES (
			"{max_request_id + 1}",
			0,
			"{current_user[1]}",
			"",
			{cur_time},
			-1,
			{due_time},
			{in_person},
			"{course}",
			"{teacher}",
			{period},
			"{help_}",
			"",
			"{assignment_sheet}",
			"{google_doc}",
			0,
			"",
			-1,
			-1,
			-1
		)
	''')

	db.commit()

	flash(f'Successfully created request #{max_request_id + 1}', 'success')

	return redirect('/dashboard')

@app.route('/delete_entry', methods=['GET'])
def delete_entry():
	c, db = get_database()
	request_id = request.args['id']

	c.execute(f"DELETE FROM requests WHERE request_id = {request_id}")
	db.commit()

	flash(f'Successfully deleted request #{request_id}', 'success')
	return redirect('/dashboard')

@app.route('/select_entry', methods=['GET'])
def select_entry():
	c, db = get_database()
	request_id = request.args['id']

	c.execute(f"UPDATE requests SET request_status = 1, editor = \"{session['username']}\" WHERE request_id = {request_id}")
	db.commit()

	c.execute(f"SELECT rowid, * FROM requests WHERE request_id = {request_id}")
	resp = c.fetchone()
	requester = get_user(resp[3], 'mentee')
	editor = get_user_from_session()

	e = Emailer()
	e.send(
		requester[0],
		[requester[2] + ' ' + requester[3], editor[3] + ' ' + editor[4], editor[1]],
		'matched'
	)

	flash(f'Successfully selected request #{request_id}', 'success')
	return redirect('/dashboard')

@app.route('/unselect_entry', methods=['GET'])
def unselect_entry():
	c, db = get_database()
	request_id = request.args['id']

	c.execute(f"UPDATE requests SET request_status = 0, editor = '' WHERE request_id = {request_id}")
	db.commit()

	flash(f'Successfully unselected request #{request_id}', 'success')
	return redirect('/dashboard')

@app.route('/complete_entry', methods=['GET'])
def complete_entry_get():
	return render_template('editor/complete_entry.html')

@app.route('/complete_entry', methods=['POST'])
def complete_entry_post():
	c, db = get_database()
	request_id = request.form.get('id')
	hours = request.form.get('hours')
	tags = request.form.get('tags')
	edit_desc = request.form.get('help')
	arista = ('arista' in request.form)
	time_completed = int(time.time())

	c.execute(f"""UPDATE requests
				  SET request_status = 2, time_completed = {time_completed}, edit_description = "{edit_desc}", hours = {hours}, tags = "{tags}"
				  WHERE request_id = {request_id}
	""")
	db.commit()

	c.execute(f"SELECT rowid, * FROM requests WHERE request_id = {request_id}")
	resp = c.fetchone()
	requester = get_user(resp[3], 'mentee')
	editor = get_user_from_session()

	e = Emailer()
	e.send(
		requester[0],
		[requester[2] + ' ' + requester[3], editor[3] + ' ' + editor[4], request_id],
		'completed'
	)

	return redirect('/dashboard')

@app.route('/feedback', methods=['GET'])
def feedback_get():
	c, db = get_database()
	request_id = request.args['id']

	c.execute(f"SELECT rowid, * FROM requests WHERE request_id = {request_id}")
	edit_request = c.fetchone()
	tags = edit_request[17].split(',')
	hours = edit_request[16]
	edit_desc = edit_request[13]

	c.execute(f"SELECT rowid, * FROM editors WHERE email = \"{edit_request[4]}\"")
	editor = c.fetchone()
	editor_name = editor[3] + ' ' + editor[4]

	return render_template('mentee/feedback.html',
							editor=editor_name,
							tags=tags,
							hours=hours,
							edit_desc=edit_desc,
							editor_name=editor_name,
							request_id=request_id)

@app.route('/finish', methods=['POST'])
def finish_post():
	c, db = get_database()
	request_id = request.form.get('id')

	current_user = get_user_from_session()
	fname, lname = current_user[3], current_user[4]

	communicative = request.form.get('communicative')
	helpful = request.form.get('helpful')
	timely = request.form.get('timely')
	comments = request.form.get('comments')

	c.execute(f"""UPDATE requests
				  SET communicativeness={communicative}, helpfulness={helpful}, timeliness={timely}, request_status=3
				  WHERE request_id={request_id}
	""")
	db.commit()

	c.execute(f"SELECT rowid, * FROM requests WHERE request_id={request_id}")
	r = c.fetchone()
	editor = get_user(r[4], 'editor')

	e = Emailer()
	e.send(
		'gthompson30',
		[r[10], current_user[3] + ' ' + current_user[4],  r[9], r[11], editor[2] + ' ' + editor[3], get_readable_time(r[6]), r[17], comments],
		type='finish'
	)

	flash('Successfully completed request.', 'success')
	return redirect('/dashboard')

@app.route('/log_in_person', methods=['GET'])
def log_in_person_hours_get():
	current_user = get_user_from_session()
	if not current_user:
		flash('You are not logged in! Please log in to access this page.', 'warning')
		return redirect('/')

	return render_template('editor/in_person_hours.html', teachers=TEACHERS, courses=COURSES)

@app.route('/log_in_person', methods=['POST'])
def log_in_person_hours_post():
	c, db = get_database()
	hours = float(request.form.get("hours"))
	flash(f'{hours} hours have been added to your account!', 'success')

	current_user = get_user_from_session()
	c.execute(f"UPDATE editors SET hours = {current_user[6] + hours} WHERE email = \"{current_user[1]}\"")
	db.commit()

	return redirect('/dashboard')

if __name__ == '__main__':
	app.run(debug=True)