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
		email TEXT PRIMARY KEY,
		password TEXT,
		fname TEXT,
		lname TEXT,
		grade INTEGER,
		pronouns TEXT,
		hours FLOAT DEFAULT 0,
		communicative_avg FLOAT DEFAULT 0,
		helpful_avg FLOAT DEFAULT 0,
		timely_avg FLOAT DEFAULT 0,
		selected TEXT DEFAULT '',
		verified BIT DEFAULT 0
	);

	CREATE TABLE mentees (
		email TEXT PRIMARY KEY,
		password TEXT,
		fname TEXT,
		lname TEXT,
		grade INTEGER,
		pronouns TEXT,
		requests TEXT DEFAULT '',
		verified BIT DEFAULT 0
	);

	CREATE TABLE requests (
		request_id INTEGER PRIMARY KEY AUTOINCREMENT,
		request_status INTEGER DEFAULT 0,
		requester TEXT,
		editor TEXT DEFAULT '',
		time_created INTEGER,
		time_completed INTEGER DEFAULT -1,
		time_due INTEGER,
		in_person BIT,
		course TEXT,
		teacher TEXT,
		period INTEGER,
		request_description TEXT,
		edit_description TEXT DEFAULT '',
		assignment_link TEXT,
		essay_link TEXT,
		hours FLOAT DEFAULT 0,
		tags TEXT DEFAULT '',
		communicativeness INTEGER DEFAULT -1,
		helpfulness INTEGER DEFAULT -1,
		timeliness INTEGER DEFAULT -1
	);
	""")

db.commit()