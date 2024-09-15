from flask import Blueprint, flash, redirect, render_template, request, session
from db import get_database, get_user
from datetime import datetime
from lists import *
from emails import *
import time

bp = Blueprint('requests', __name__, url_prefix='/requests')

@bp.route('/create_piece', methods=['GET'])
def create_piece_get():
	if session['usertype'] == 'mentee':
		return render_template('mentee/make_request.html', current_user=get_user(session['username'], session['usertype']), teachers=teachers, courses=courses)
	return redirect('/')

@bp.route('/create_piece', methods=['POST'])
def create_piece_post():
	teacher = request.form.get('teacher')
	course = request.form.get('course')
	period = int(request.form.get('period'))
	description = request.form.get('help').replace('"', '""')
	assignment_link = request.form.get('assignment_sheet')
	essay_link = request.form.get('google_doc')
	in_person = int(bool(request.form.get('in_person')))

	year, month, day = map(int, request.form.get('due_date').split('-'))
	due_time = request.form.get('due_time')
	if not due_time: due_time = '12:00'
	hour, minute = map(int, due_time.split(':'))

	due_time = datetime(year, month, day, hour, minute)
	due_time = int(time.mktime(due_time.timetuple()))
	cur_time = int(time.time())

	c, db = get_database()
	c.execute("SELECT rowid, * FROM requests;")

	current_user = get_user(session['username'], session['usertype'])
	c.execute(f'''
		INSERT INTO requests (requester, time_created, time_due, in_person, course, teacher, period, request_description, assignment_link, essay_link)
    VALUES ('{current_user[1]}', {cur_time}, {due_time}, {in_person},	'{course}', '{teacher}', {period}, '{description}',	'{assignment_link}', '{essay_link}')''')
	db.commit()

	flash(f'Request creation successful!', 'success')
	return redirect('/dashboard')

@bp.route('/delete_entry', methods=['GET'])
def delete_entry():
	c, db = get_database()
	request_id = request.args['id']

	c.execute(f"DELETE FROM requests WHERE request_id = {request_id}")
	db.commit()

	flash(f'Successfully deleted request #{request_id}', 'success')
	db.close()
	return redirect('/dashboard')

@bp.route('/select_entry', methods=['GET'])
def select_entry():
	c, db = get_database()
	request_id = request.args['id']

	c.execute(f"UPDATE requests SET request_status = 1, editor = \"{session['username']}\" WHERE request_id = {request_id}")
	db.commit()

	c.execute(f"SELECT rowid, * FROM requests WHERE request_id = {request_id}")
	resp = c.fetchone()
	requester = get_user(resp[3], 'mentee')
	editor = get_user(session['username'], session['usertype'])

	e = Emailer()
	e.send(requester[1], [f"{requester[3]} {requester[4]}", f"{editor[3]} {editor[4]}", editor[1]], 'matched')

	flash(f'Successfully selected request #{request_id}', 'success')
	db.close()
	return redirect('/dashboard')

@bp.route('/unselect_entry', methods=['GET'])
def unselect_entry():
	c, db = get_database()
	request_id = request.args['id']

	c.execute(f"UPDATE requests SET request_status = 0, editor = '' WHERE request_id = {request_id}")
	db.commit()

	flash(f'Successfully unselected request #{request_id}', 'success')
	db.close()
	return redirect('/dashboard')

@bp.route('/complete_entry', methods=['GET'])
def complete_entry_get():
	return render_template('editor/complete_entry.html')

@bp.route('/complete_entry', methods=['POST'])
def complete_entry_post():
	c, db = get_database()
	request_id = request.form.get('id')
	hours = int(request.form.get('hours'))
	tags = request.form.get('tags')
	edit_desc = request.form.get('help')
	time_completed = int(time.time())

	c.execute(f"""UPDATE requests 
    SET request_status = 2, time_completed = {time_completed}, edit_description = "{edit_desc}", hours = {hours}, tags = "{tags}"
		WHERE request_id = {request_id}""")
	db.commit()

	c.execute(f"SELECT rowid, * FROM requests WHERE request_id = {request_id}")
	resp = c.fetchone()
	requester = get_user(resp[3], 'mentee')
	editor = get_user(session['username'], session['usertype'])
	c.execute(f"UPDATE editors SET hours={editor[7] + hours} WHERE email='{session['username']}'")
	db.commit()
	e = Emailer()
	e.send(requester[1], [f"{requester[3]} {requester[4]}", f"{editor[3]} {editor[4]}", request_id], 'completed')

	db.close()
	return redirect('/dashboard')