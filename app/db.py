from flask import Flask, session, render_template, request, flash, redirect
import sqlite3

def get_database():
	db = sqlite3.connect('app/data.db')
	c = db.cursor()
	return c, db

def get_user(username, usertype):
	c, db = get_database()
	c.execute(f"SELECT rowid, * FROM {usertype}s WHERE email=\"{username}\"")
	resp = c.fetchone()
	print(resp)
	db.close()
	return resp if resp else None