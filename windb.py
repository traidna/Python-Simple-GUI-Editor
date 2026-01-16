import sqlite3 as sq
import os
from tkinter import messagebox


def makedb():

	### check if exists and warn?
	
	if os.path.isfile("pywin.db"):
		messagebox.showinfo("","Database exists")
		return
	
	conn=sq.connect('pywin.db')
	cur = conn.cursor()

	cur.execute("""CREATE TABLE windows(
		winname TEXT,
		title TEXT,
		width TEXT,
		height TEXT,
		x TEXT,
		y TEXT)
		""")
	conn.commit()
	
	cur.execute("""CREATE TABLE widgets(
		winname TEXT,
		title TEXT,
		width TEXT,
		height TEXT,
		x TEXT,
		y TEXT,
		from_num TEXT,
		to_num TEXT,
		trigger TEXT,
		code, TEXT)
		""")
	conn.commit()
	conn.close()	

	messagebox.showinfo("info","Database pywin.db has been created")
	
	
def checkdb():
	conn=sq.connect('pywin.db')
	cur = conn.cursor()

	cur.execute("SELECT *,oid FROM windows")
	q=cur.fetchall()
	conn.commit()
	conn.close()
	print("in checkdb")
	for r in q:
		print(str(r))
	
checkdb()
	