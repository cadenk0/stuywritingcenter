'''

MEANING OF TABLE ITEMS:

editors:
    email [primary key]:
    	a unique string, the email prefix of the editor
    password:
    	a string, the password of the editor (unencrypted at the moment)
    fname:
    	a string, the first name of the editor
    lname:
    	a string, the last name of the editor
    grade:
    	an integer, the grade of the editor
    hours:
    	a number, the number of hours the editor has
    communicative_avg:
    	a number, the avg "communicative" score the editor has acquired
    helpful_avg:
    	a number, the avg "helpfulness" score the editor has acquired
    timely_avg:
    	a number, the avg "timeliness" score the editor has acquired
    selected:
    	a string, a comma-separated list of request ids the editor selected as editing
    pronouns:
    	a string, the editor's pronouns
    verified:
    	an integer, 0 or 1 indicating whether the editor has verified their account

mentees:
	email [primary key]:
		a unique string, the email prefix of the mentee
	password:
		a string, the password of the mentee (unencrypted at the moment)
	fname:
		a string, the first name of the mentee
	lname:
		a string, the last name of the mentee
	grade:
		an integer, the grade of the mentee
	requests:
		a string, a comma-separated list of request ids the mentee has created
	pronouns:
		a string, the mentee's pronouns
	verified:
		an integer, 0 or 1 indicating whether the mentee has verified their account

requests:
	request_id [primary key]:
		a unique integer, which can be used to identify the request
	request_status:
		an integer (either 0, 1, 2 or 3) indicating the status of the request
			0: the request has been created but has not been selected by an editor
			1: the request has been selected by the editor but has not been marked as "complete"
			2: the request has been marked as "complete" by the editor but not been approved by the mentee
			3: the editor's edit has been approved by the mentee
	requester:
		a string, the email prefix of the mentee who created the request
	editor:
		a string, the email prefix of the editor who has selected the request
	time_created:
		an integer, the unix timestamp of when the request was created
	time_due:
		an integer, the unix timestamp of when the request is due
    in_person:
    	an integer, 0 or 1 depending on whether the mentee would like to meet in-person
	course:
		a string, the name of the course the request is for
	teacher:
		a string, the name of the teacher whose class the request is for
	period:
		an integer, the period of the class the request is for
	assignment_link:
		a string, the url of the assignment page
	essay_link:
		a string, the url of the mentee's draft
	request_description:
		a string, a description of what the mentee wants the editor to do
    edit_description:
    	a string, a description of what the editor helped with
	hours:
		a number, the amount of hours the editor spent on the request
	tags:
		a string, a comma-separated list of a "tags" on the request
    communicativeness:
    	an integer 1-10, the avg "communicative" score the editor has acquired
    helpfulness:
    	an integer 1-10, the avg "helpfulness" score the editor has acquired
    timeliness:
    	an integer 1-10, the avg "timeliness" score the editor has acquired
'''

import sqlite3

db_fname = 'app/data.db'
db = sqlite3.connect(db_fname, check_same_thread=False)
c = db.cursor()

c.executescript("""

	DROP TABLE IF EXISTS editors;
	DROP TABLE IF EXISTS mentees;
	DROP TABLE IF EXISTS requests;

	""")

c.executescript("""

	CREATE TABLE editors (
		email text primary key,
		password text,
		fname text,
		lname text,
		grade integer,
		hours real,
		communicative_avg real,
		helpful_avg real,
		timely_avg real,
		selected text,
		pronouns text,
		verified integer
	);

	CREATE TABLE mentees (
		email text primary key,
		password text,
		fname text,
		lname text,
		grade integer,
		requests text,
		pronouns text,
		verified integer
	);

	CREATE TABLE requests (
		request_id integer primary key,
		request_status integer,
		requester text,
		editor text,
		time_created integer,
		time_completed integer,
		time_due integer,
		in_person integer,
		course text,
		teacher text,
		period integer,
		request_description text,
		edit_description text,
		assignment_link text,
		essay_link text,
		hours real,
		tags text,
		communicativeness integer,
		helpfulness integer,
		timeliness integer
	);

	""")

db.commit()