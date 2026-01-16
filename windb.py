import sqlite3 as sq
import os
from tkinter import messagebox


## create the database - only needs to happen once or if a reset on the db
def makedb():
	
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
		winid TEXT,
		wtype TEXT,
		wname TEXT,
		master TEXT,
		wtext TEXT,
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
	
## just a utility function to output what is in the database
## print window data then widgets for that window	
def checkdb():
	conn=sq.connect('pywin.db')
	cur = conn.cursor()

	cur.execute("SELECT *,oid FROM windows")
	q=cur.fetchall()
	conn.commit()
	
	print("\nin checkdb\n\n")
	for r in q:
		## print window info
		print(f"{r} oid={r[6]}\n")
		oid=r[6]
		cur.execute(f"SELECT *,oid FROM widgets WHERE winid={oid}")
		w=cur.fetchall()
		for ww in w:
			## print wdigets for this window
			print(ww)
		print("\n\n")
		
	conn.close()

checkdb()