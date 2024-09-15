from flask import Flask, session, render_template, request, flash, redirect
from lists import courses, teachers
from emails import *
from db import *
import sqlite3
from datetime import datetime

app = Flask(__name__)
import auth
app.register_blueprint(auth.bp)
import requests
app.register_blueprint(requests.bp)
app.secret_key = 'bigchunguslol'

# Utility

def get_readable_time(timestamp):
	print(timestamp)
	return datetime.utcfromtimestamp(timestamp).strftime('%m-%d-%Y at %H:%M:%S')

# Main Pages

@app.route('/')
def index():
	return render_template('static_pages/landing.html', loggedin=bool(session))

@app.route('/about')
def about():
	c, db = get_database()
	c.execute(f"SELECT rowid, * FROM editors;")
	all_editors = sorted(c.fetchall(), key=lambda editor: editor[6])[::-1]
	db.close()
	return render_template('static_pages/about.html', editors=all_editors, usertype=session['usertype'])

@app.route('/credits', methods=['GET'])
def view_hours():
	c, db = get_database()
	current_user = get_user(session['username'], session['usertype'])
	c.execute(f"SELECT rowid, * FROM editors WHERE email=\"{current_user[1]}\"")
	if not current_user:
		flash('You are not logged in! Please log in to access this page.', 'warning')
		db.close()
		return redirect('/')

	c.execute(f"SELECT * FROM requests WHERE editor=\"{session['username']}\" AND request_status=3;")
	num_credits = len(c.fetchall())

	c.execute(f"SELECT rowid, * FROM editors;")
	all_editors = sorted(c.fetchall(), key=lambda editor: editor[6])[::-1]
	
	db.close()
	return render_template('editor/hours.html', hours=current_user[7], editors=all_editors, credits=num_credits)

# @app.route('/admin', methods=["POST"])
# def admin():
# 	password = request.form.get('password')
# 	hashed = sha256(password.encode()).hexdigest()
# 	editors = User.query.filter_by(usertype='editor')
# 	editors = editors.all()
# 	whitelist = ', '.join(open('whitelist.csv').read().split(','))
# 	print(editors)
# 	if hashed == os.getenv('ADMIN_PWD'):
# 		return render_template('admin/dashboard.html', editors=editors, whitelist=whitelist)
# 	else:
# 		flash('Invalid password!', 'warning')
# 		return redirect('/admin')

@app.route('/dashboard', methods=["GET"])
def dashboard():
	if not("username" in session):
		flash('You have not verified your email! Check your email for an email verification link.', 'danger')
		return redirect('/')

	current_user = get_user(session['username'], session['usertype'])
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
		total_hours = current_user[7]

		db.close()
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
		c.execute(f"SELECT rowid, * FROM requests WHERE requester=\"{current_user[1]}\"")
		requests = c.fetchall()
		num_active = sum((r[2] < 3) for r in requests)

		db.close()
		return render_template('mentee/dashboard.html',
							   fname=current_user[3],
							   lname=current_user[4],
							   requests=requests,
							   num_active=num_active,
							   get_readable_time=get_readable_time,
							   get_user=get_user)

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
	editor_name = f"{editor[3]} {editor[4]}"

	db.close()
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
	request_id = int(request.form.get('id'))
	print(request_id)

	current_user = get_user(session['username'], session['usertype'])
	fname, lname = current_user[3], current_user[4]

	communicative = request.form.get('communicative')
	helpful = request.form.get('helpful')
	timely = request.form.get('timely')
	comments = request.form.get('comments')

	c.execute(f"""UPDATE requests
				  SET communicativeness={communicative}, helpfulness={helpful}, timeliness={timely}, request_status=3
				  WHERE request_id={request_id}""")
	db.commit()

	c.execute(f"SELECT rowid, * FROM requests WHERE request_id={request_id}")
	r = c.fetchone()
	editor = get_user(r[4], 'editor')

	e = Emailer()
	e.send('jlei60', [r[10], f"{current_user[3]} {current_user[4]}", r[9], r[11], f"{editor[3]} {editor[3]}", get_readable_time(r[6]), r[17], comments], 'finish')

	flash('Successfully completed request.', 'success')
	db.close()
	return redirect('/dashboard')

@app.route('/log_in_person', methods=['GET'])
def log_in_person_hours_get():
	current_user = get_user(session['username'], session['usertype'])
	if not current_user:
		flash('You are not logged in! Please log in to access this page.', 'warning')
		return redirect('/')
	return render_template('editor/in_person_hours.html', teachers=teachers, courses=courses)

@app.route('/log_in_person', methods=['POST'])
def log_in_person_hours_post():
	c, db = get_database()
	hours = float(request.form.get("hours"))
	flash(f'{hours} hours have been added to your account!', 'success')
	current_user = get_user(session['username'], session['usertype'])
	c.execute(f"UPDATE editors SET hours={current_user[7] + hours} WHERE email=\"{current_user[1]}\"")
	db.commit()
	db.close()
	return redirect('/dashboard')

if __name__ == '__main__':
	app.run(debug=True)