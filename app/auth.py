from flask import Blueprint, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_database
from lists import whitelist
from emails import *
import sqlite3

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/editor_login', methods=['GET'])
@bp.route('/mentee_login', methods=['GET'])
def login_get():
  return render_template('login.html', usertype=f"{request.path[6:12].title()}")

@bp.route('/editor_login', methods=['POST'])
@bp.route('/mentee_login', methods=['POST'])
def login_post():
  usertype = request.form.get('usertype')
  email = request.form.get('email')
  entered_password = request.form.get('password')

  db = sqlite3.connect('app/data.db', check_same_thread=False)
  c = db.cursor()
  c.execute(f"SELECT password FROM {request.path[6:12]}s WHERE email='{email}'")
  correct_password = c.fetchone()[0]

  if entered_password and check_password_hash(correct_password, entered_password):
    session["username"] = email
    session["usertype"] = usertype
    return redirect('/dashboard')
  else:
    flash('Account does not exist or password is invalid', 'danger')
    return redirect(request.path)

@bp.route('/editor_signup', methods=['GET'])
@bp.route('/mentee_signup', methods=['GET'])
def signup_get():
  return render_template('signup.html', usertype=request.path[6:12])

@bp.route('/mentee_signup', methods=['POST'])
@bp.route('/editor_signup', methods=['POST'])
def signup_post():
  usertype = request.path[6:12]
  email = request.form.get('email').lower().replace('@nycstudents.net', '')
  password = request.form.get('password')
  fname = request.form.get('fname')
  lname = request.form.get('lname')
  grade = request.form.get('grade')
  pronouns = request.form.get('pronouns')
  password = generate_password_hash(password)

  c, db = get_database()

  c.execute(f"SELECT * FROM {usertype}s WHERE email='{email}'")
  if len(c.fetchall()) > 0:
    flash('User with that email already exists!', 'danger')
    db.close()
    return redirect(request.path)

  if usertype == 'editor':
    if not(email in whitelist):
      flash('You\'re not on the whitelist! Please contact the writing center admins to be whitelisted.', 'danger')
      db.close()
      return redirect(request.path)

  c.execute(f"""INSERT INTO {usertype}s (email, password, fname, lname, grade, pronouns) VALUES (
  '{email}', '{password}', '{fname}', '{lname}', '{grade}', '{pronouns}')""")
  db.commit()

  flash('Check your @nycstudents.net email to confirm your account.', 'success')
  e = Emailer()
  e.send(email, [email, fname, usertype], type='signup')
  db.close()
  return redirect(f'/auth/{usertype}_login')

# LOGOUT METHOD

@bp.route('/logout', methods=["GET"])
def logout():
  session.pop("username", None)
  return redirect("/")

@bp.route('/confirm', methods=["GET"])
def confirm():
  email = request.args['email']
  usertype = request.args['usertype']

  c, db = get_database()
  c.execute(f"UPDATE {usertype}s SET verified=1 WHERE email='{email}'")
  db.commit()

  flash('Successfully verified email! You can log in below.', 'success')
  db.close()
  return redirect(f'/auth/{usertype.lower()}_login')

@bp.route('/admin', methods=["GET"])
def admin_login():
  return render_template('admin/login.html')