import sqlite3 as sq
import os
from tkinter import messagebox


def makedb():

	### check if exists and warn?
	
	if os.path.isfile("pywin.db"):
		messagebox.showinfo("","Database exists")
		return
	
		
	#os.system("rm win.db")

	conn=sq.connect('pywin.db')
	cur = conn.cursor()

	cur.execute("""CREATE TABLE windows(
		id INTEGER PRIMARY_KEY,
		winname TEXT,
		title TEXT,
		width TEXT,
		height TEXT,
		x TEXT,
		y TEXT)
		""")
	conn.commit()
	
	cur.execute("""CREATE TABLE widgets(
		id INTEGER PRIMARY_KEY,
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
	