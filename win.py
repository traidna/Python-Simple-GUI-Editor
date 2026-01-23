#!/opt/homebrew/opt/python@3.13/bin/python3
## above for my mac
###!/usr/bin/python3
### linux raspterry pi #!/usr/bin/python3

import tkinter as tk
from tkinter import IntVar, StringVar
from tkinter import messagebox
from tkinter import colorchooser
import tkinter.font as tkFont
from tkinter import filedialog as fd
import platform
import sys
import os
import sqlite3 as sq


def on_drag_start(event):
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y

def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x, y=y)
    print("pos of widget "+str(widget.winfo_x()) + "," + str(widget.winfo_y()))

def update_mode(inmode):
	global mode
	mode=inmode
	modelabel.config(text=f'Mode: {mode}')
	

## create the database - only needs to happen once or if a reset on the db
def makedb():
	
	if os.path.isfile("pywin.db"):
		##messagebox.showinfo("","Database exists")
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
		fgcolor TEXT,
		bgcolor TEXT)
		""")
	conn.commit()
	conn.close()	
	messagebox.showinfo("info","Database pywin.db has been created")


# Create the target window
def createWindow():
    global win
    global mode
    global m
    text=wtentry.get()
    win=tk.Toplevel()
    win.title(text)
    
    # Bind the close event to the on_closing function
    win.protocol("WM_DELETE_WINDOW", on_closing)
    
    gstr=f'{wwentry.get()}x{whentry.get()}+{xpentry.get()}+{ypentry.get()}'
    print(gstr)
    win.geometry(gstr)
    wbutton.config(state="disabled")
    lwbutton.config(state="disabled")
    button.config(state="active")
    write_button.config(state="active")
    edit_button.config(state="active")
    editwin_button.config(state="active")
    resetwin_button.config(state="active")
    
    m.append(win)
    update_mode("add")
    
    #mode="add"
    print("master list = "+str(m))


## clear all the widgets for the window on the entry screen
def clrwinparms():
	wtentry.delete(0,'end')
	wnentry.delete(0,'end')
	wwentry.delete(0,'end')
	whentry.delete(0,'end')
	xpentry.delete(0,'end')
	ypentry.delete(0,'end')


## clear all the widgets on the entry screen
def clr_widget_fields():
	name_entry.delete(0,"end")
	caption_entry.delete(0,"end")
	x_entry.delete(0,"end")
	y_entry.delete(0,"end")
	height_entry.delete(0,"end")
	width_entry.delete(0,"end")
	cmd_entry.delete(0,"end")
	from_entry.delete(0,"end")
	to_entry.delete(0,"end")
	bgc_frame.config(bg=dfltbg)
	fgc_frame.config(bg=dfltfg)


## pass in a widget and return a string of widget type parsed
def parse_widget_type(w):
	wstr=str(type(w))
	wstr=wstr.split(".")[1]
	wstr=wstr.split("'")[0]
	return wstr

    
# default text in cmd_entry if appropriate type of widget 
def change_widget():
	wig=wvar.get()
	#wigcmd is a list of widgets that can have a command=
	if (wig in wigcmd):
		cmd_entry.config(state="normal")
		#cmdtext.config(state="normal")
	else:
		cmd_entry.delete(0,'end')
		#cmdtext.delete(1.0, 'end')
		cmd_entry.config(state="disable")
		#cmdtext.config(state="disable")
	if (wig in wigtxt):
		caption_entry.config(state="normal")
	else:
		caption_entry.delete(0,'end')
		caption_entry.config(state="disable")
				
	if(wig=="Spinbox" or wig=="Scale"):
		#from_label.place(x=10, y=450)
		#from_entry.place(x=60, y=450, width=50)
		#to_label.place(x=130, y=450)
		#to_entry.place(x=175, y=450, width=50)
		to_entry.config(state='normal')
		from_entry.config(state='normal')
		from_entry.delete(0,'end')
		from_entry.insert(0,"0")
		to_entry.delete(0,'end')
		to_entry.insert(0,"100")
	else:
		##from_label.place_forget()
		##from_entry.place_forget()
		##to_label.place_forget()
		##to_entry.place_forget()
		from_entry.config(state="disable")
		to_entry.config(state="disable")



## create name of commnand function
def update_cmdfnc(event):
	wig=wvar.get()
	if (wig in wigcmd and name_entry.get() !="" and mode=="add"):
		cmd_entry.delete(0,"end")
		nstr=name_entry.get().replace(" ","_")
		nstr='on_'+nstr+'_clicked'
		if wig=='Scale':
			nstr = nstr + '(event)'
		else:
			nstr=nstr + ')'
			
		cmd_entry.insert(0,nstr)


#Save the updated widget after selecting edit
def updateWidget():
	global ew
	global edit_index
	wtype = parse_widget_type(ew)
	wnlist[edit_index]=name_entry.get()
	cmdlst[edit_index]=cmd_entry.get()
	
	## udpate fg an bg colors
	if wtype in wigcol:
		ew.config(fg=fgc_frame['bg'])
		if (wtype!="Frame"):
			ew.config(bg=bgc_frame['bg'])
		
	## update text fields
	if wtype in wigtxt:
		ew.config(text=caption_entry.get())
	
	if wtype in wigtofrom:
		ew.config(from_=from_entry.get())
		ew.config(to=to_entry.get())
	
	ew.place(x=x_entry.get(), y=y_entry.get(), width=width_entry.get(), height=height_entry.get())
	wstr=parse_widget_type(ew)+"               "
	wstr=wstr[0:15]+wnlist[edit_index]
	wigbox.delete(edit_index)
	wigbox.insert(edit_index,wstr)
	clr_widget_fields()
	button.config(state="active")
	update_button.config(state="disable")
	#global mode
	#mode="add"
	update_mode("add")
	
	print(wnlist)
	
	
# update form with widget info for widget to change, load fields for selected widget
def edit_widget():
	print("Edit Widget")
	selected_index=wigbox.curselection()
	if (wigbox.size()==0):
		messagebox.showinfo("No Widgets", "There are no widgets in the list")
	elif (not selected_index):
		messagebox.showinfo("None Selected", "No widget selected")
	else:
		global ew
		global edit_index
		index=selected_index[0]
		edit_index=index
		w=wlist[index]
		wtype=parse_widget_type(w)
		print(f"index = {index}  type={wtype} fx={w.winfo_x()}  wx{w.winfo_rootx()}")
		ew=w
		clr_widget_fields()
		name_entry.insert(0,wnlist[index])
		cmd_entry.insert(0,cmdlst[index])
		
		mastervar.set(masterlist[index])
		wvar.set(wtype)
		
		if wtype in wigtxt:
			caption_entry.insert(0,w.cget("text"))
		if (masterlist[index]!="root"):
			mstridx=masteridx[index]
			x_entry.insert(0,str(w.winfo_x()-m[mstridx].cget("borderwidth")))
			y_entry.insert(0,str(w.winfo_y()-m[mstridx].cget("borderwidth")))
		else:
			x_entry.insert(0,w.winfo_x())
			y_entry.insert(0,w.winfo_y())
			
		if (wtype in wigcol):
			bgc_frame.config(bg=w['bg'])
			if (wtype!="Frame"):
				fgc_frame.config(bg=w['fg'])

		width_entry.insert(0,w.winfo_width())
		height_entry.insert(0,w.winfo_height())
		
		if (wtype=="Spinbox" or wtype=="Scale"):
			from_entry.insert(0,w.cget("from"))
			to_entry.insert(0,w.cget("to"))
		
		button.config(state="disable")
		update_button.config(state="active")
		
		name_entry.focus_force()
		update_mode("update")


# clear all widget fields and put in "add" mode 
# this will reject changes in update mode
def clear_widget():
	clr_widget_fields()
	update_button.config(state="disable")
	button.config(state="active")
	name_entry.focus_force()
	update_mode("add")


## bind function for not allowing the user window to be closed	
def on_closing():
	pass
    
    
# Create Widget on working window
def createWidget():
	#add or update mode
    global mode  
    if (mode!="add"):
       messagebox.showinfo("","Not in Add mode")
       return    
    if(name_entry.get()=="" or x_entry.get()=="" or y_entry.get()==""):
        messagebox.showinfo("Information","Missing widget information")
        return
       
    global widgetct
    global m
    widgetct=widgetct+1
    caption=caption_entry.get()
    cmd=cmd_entry.get()

    fgcol=fgc_frame['bg']
    bgcol=bgc_frame['bg']
   
    mindex=master_options.index(mastervar.get())
    print(f"master options = {master_options} master_index = {mindex} m[mindex]={m[mindex]}")

    #Label
    if (wvar.get() == "Label"):
        w=tk.Label(m[mindex], text = caption, bg=bgcol, fg=fgcol)
        w.place(x=x_entry.get(), y=y_entry.get(), width=width_entry.get(), height=height_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
        print(f"x={w.winfo_x()}")            
    # Button
    elif (wvar.get() == "Button"):
        w=tk.Button(m[mindex], text=caption, bg=bgcol, fg=fgcol)
        w.place(x=x_entry.get(), y=y_entry.get(), height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        w.config(bg=bgcolor)
        wlist.append(w)
    # Entry Box
    elif (wvar.get() == "Entry"):
        w=tk.Entry(m[mindex], bg=bgol, fg=fgcol)
        w.insert(0,caption)
        w.place(x=x_entry.get(), y=y_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
    # Text Box
    elif (wvar.get() == "Text"):
        w=tk.Text(m[mindex], bg=bgcol, fg=fgcol)
        w.insert("1.0",caption)
        w.place(x=x_entry.get(), y=y_entry.get(),height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
    # Checkbutton Box
    elif (wvar.get() == "Checkbutton"):
        w=tk.Checkbutton(m[mindex],text=caption, bg=bgcol, fg=fgcol)
        w.place(x=x_entry.get(), y=y_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
    #spinbox    
    elif (wvar.get() == "Spinbox"):
        w=tk.Spinbox(m[mindex],text=caption, from_ = from_entry.get(), to=to_entry.get())
        w.place(x=x_entry.get(), y=y_entry.get(), height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)   
    #scale
    elif (wvar.get() == "Scale"):
        w=tk.Scale(m[mindex], bg=bgcol, fg=fgcol, from_ = from_entry.get(), to=to_entry.get(), orient = tk.HORIZONTAL)
        w.place(x=x_entry.get(), y=y_entry.get(), height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)     
    # ListBox
    elif (wvar.get() == "Listbox"):
        w=tk.Listbox(m[mindex], bg=bgcol, fg=fgcol)
        w.place(x=x_entry.get(), y=y_entry.get(),height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
    # LabelFrame
    elif (wvar.get() == "LabelFrame"):
        w=tk.LabelFrame(m[mindex], text=caption, bg=bgcol, fg=fgcol, borderwidth=2)
        w.place(x=x_entry.get(), y=y_entry.get(),height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
        m.append(w)
        master_options.append(name_entry.get().replace(" ","_"))
        opt=name_entry.get().replace(" ","_")
        master_om['menu'].add_command(label=opt, command=tk._setit(mastervar, opt))
    # Frame
    elif (wvar.get() == "Frame"):
        w=tk.Frame(m[mindex], bg=bgcol, borderwidth=2, relief=tk.GROOVE)
        w.place(x=x_entry.get(), y=y_entry.get(),height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
        m.append(w)
        master_options.append(name_entry.get().replace(" ","_"))
        opt=name_entry.get().replace(" ","_")
        master_om['menu'].add_command(label=opt, command=tk._setit(mastervar, opt))

    name_entry.focus_force()
    cmdlst.append(cmd)
    #proclist.append(cmdcode)
    masterlist.append(mastervar.get())
    masteridx.append(mindex)
    wnlist.append(name_entry.get().replace(" ","_"))
    wname=name_entry.get()
    clr_widget_fields()
    mystr=parse_widget_type(w)
    mystr=mystr+"                    "
    mystr=mystr[0:15]
    lbstr=mystr + wname
    wigbox.insert("end",lbstr)

    
## save the window info to the database
def save_to_db():
	global winid
	if int(winid)>0:
		oid=winid
	conn=sq.connect('pywin.db')
	c = conn.cursor()
	###
	### check adding new one or updating old
	### 
	if int(winid)<1:
		sql="""INSERT INTO windows(winname, title, height, width, x, y)
		VALUES(?,?,?,?,?,?)"""
		sqldata=(wnentry.get(),win.title(),
			win.winfo_height(),win.winfo_width(),
			win.winfo_x(),win.winfo_y())
		c.execute(sql, sqldata)
		conn.commit()
		oid=c.lastrowid
	else:
		sql=f"""
		UPDATE windows 
		SET winname=?, title=?, height=?, width=?, x=?, y=? WHERE oid={winid}
		"""
		sqldata=(wnentry.get(),win.title(),
			win.winfo_height(),win.winfo_width(),
			win.winfo_x(),win.winfo_y())
		print(sql)
		print(sqldata)
		c.execute(sql, sqldata)
		conn.commit()
		
	## if existing window delete all the widgets
	if int(winid)>0:
		print("*** deleting fronm widgets "+str(winid))
		sql=f'DELETE FROM widgets WHERE winid={winid}'
		print('SQL='+sql)
		c.execute(sql)
		conn.commit()


	## save the widgets
	for i,w in enumerate(wlist):
		fromnum="-1"
		tonum="-1"
		wtype = parse_widget_type(w)
		
		if wtype in wigtofrom:
			fromnum=str(w.cget("from"))
			tonum=str(w.cget("to"))
		
		wtext=""
		if wtype in wigtxt:
			wtext=w.cget("text")
		
		fgc="" ## if frame no fg property so set default
		bgc=""
		
		if wtype in wigcol:
			if wtype!="Frame":
				 fgc=str(w.cget("fg"))
			bgc=str(w.cget("bg"))
		
		x=w.winfo_x()
		y=w.winfo_y()
		
		# adjust x, y by size or boader (hard coded to 2) if not on root	
		mstr=masterlist[masteridx[i]]
		if mstr!="root":
			x=x-1
			y=y-2
		
		print(f'name={wnlist[i]}   width={w.winfo_width()}')
		
		sql="""INSERT INTO widgets(winid, wtype, wname, master, wtext,
				width, height, x, y, from_num, to_num, trigger, fgcolor, bgcolor)
			VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
		sqldata=(oid,
				parse_widget_type(w),
				wnlist[i],
				mstr,
				wtext,
				w.winfo_width(),
				w.winfo_height(),
				x,
				y,
				fromnum,
				tonum,
				cmdlst[i],
				fgc,
				bgc
				)
				
		c.execute(sql, sqldata)
		conn.commit()
		
	conn.close()


## write the application
def write_widget_code():
	ctr=0
	filedir=fd.asksaveasfilename(initialfile=f'{wnentry.get()}.py')
	## list of the command rtns
	rtnlist=[]
	## create a separate file for each widget that has a command
	with open(filedir,"w") as f:
		# write imports and window def
		f.write("import tkinter as tk\n")
		f.write("from tkinter import IntVar\n\n")
		
		# write out the command= files and imports 
		for index, c in enumerate(cmdlst):
			fn=f'{wnentry.get()}_{c}.py'
			if c!="":
				rtnlist.append(fn)
				
			## only write the code if one does not exist already
			if c!="" and not os.path.isfile(fn): 
				with open(fn,"w") as fnf:
					fnf.write(f'def {c}:\n')
					fnf.write(f'\tprint("In {fn}")\n')
					fnf.write("\n")
					fnf.close()

		## read files for signals and write them in 
		print("Routines to pull in\n" + str(rtnlist))
		for rtn in rtnlist:
			with open(rtn, 'r') as rf:
				content = rf.read()
				rf.close
				f.write('\n')
				f.write(content)
				f.write('\n')
				
		f.write("root=tk.Tk()\n")
		titlestr='root.title("' + wtentry.get() + '")'
		f.write(titlestr)
		f.write("\n")
		pstr='root.geometry("'+ wwentry.get() + 'x' + whentry.get() + '+' + xpentry.get() + '+' + ypentry.get()+'")'
		f.write(pstr)
		f.write("\n\n")
		
		
		# write out all the widgets
		for index,w in enumerate(wlist):
			print(f"index = {index}  cmd={cmdlst[index]} w={str(w)}")
			wstr=str(type(w)).split(".")[1]
			wstr=wstr.split("'")[0]
			mstr=masterlist[index]
			
			## special cases fro listbox, Text and Frame
			##if (wstr!="Listbox" and wstr!="Text" and wstr!="Frame"):
			if wstr in wigtxt:
				pstr = wnlist[ctr] + '=tk.' + wstr+'('+mstr+', text="' + w.cget('text') +'"' 
			else:
				 pstr = wnlist[ctr] + '=tk.' + wstr+'('+mstr
			
			if (wstr=="Frame" or wstr=="Labelframe"):
				pstr=pstr+', borderwidth=2, relief="groove"'
			
			if wstr in wigtofrom:
				pstr = pstr + ', from_=' + str(w.cget('from')) + ', to=' + str(w.cget('to'))
				if wstr=="Scale":
					pstr = pstr + ', orient= tk.HORIZONTAL'
				
			## write color info
			if wstr in wigcol:
				pstr = pstr + ', bg="' + w["bg"] + '"'
				if wstr!="Frame":
					pstr = pstr + ', fg="' + w["fg"] + '"'
				
			if (cmdlst[index]!=""):
				pstr=pstr+", command="+str(cmdlst[index].replace('event','').replace('()',""))
			pstr=pstr + ' )'
			print(pstr)
			p2str = wnlist[ctr] + ".place(x=" + str(w.winfo_x()) + ",y=" + str(w.winfo_y())+ ","
			p2str= p2str + "height="+str(w.winfo_height()) + ", width="+str(w.winfo_width()) + ")"
			print(p2str)
			ctr = ctr+1
			f.write(pstr)
			f.write("\n")
			f.write(p2str)
			f.write("\n\n")



		f.write("root.focus_force()\n")
		f.write("root.mainloop()")
		f.write("\n")
		f.close()
		
		## save window and wigets to database
		save_to_db()


## load all the widgets for the selected window from the database
def loadwidgets(wid):
	## load from database
	conn=sq.connect('pywin.db')
	c=conn.cursor()
	c.execute(f'SELECT *,oid FROM widgets WHERE winid={wid}')
	widgets=c.fetchall()
	conn.commit()
	conn.close()
	
	## loop through all the widgets for this window
	for w in widgets:
		print(str(w)+'\n')
		clr_widget_fields()
		# load all the fileds
		name_entry.insert(0,w[2])
		caption_entry.insert(0,w[4])
		width_entry.insert(0,w[5])
		height_entry.insert(0,w[6])	
		x_entry.insert(0,w[7])
		y_entry.insert(0,w[8])
		from_entry.insert(0,w[9])
		to_entry.insert(0,w[10])
		cmd_entry.insert(0,w[11])
		fgc_frame.config(bg=w[12])
		bgc_frame.config(bg=w[13])
		# set the widget type radiobutton
		wvar.set(w[1])
		# set the master dropdown value
		mastervar.set(w[3])
		#create the widget
		createWidget()


## pick the window for those listed from the database
def pickwin():
	global lb
	global winid
	sel=lb.curselection()[0]
	winid=lb.get(sel).split()[0]
	widLabel.config(text=f'WID: {str(winid)}')
	conn=sq.connect('pywin.db')
	c=conn.cursor()
	oid=int(winid)
	c.execute(f'SELECT *,oid FROM windows WHERE oid={oid}')
	windb=c.fetchall()
	conn.commit()
	conn.close
	clrwinparms()
	windata=windb[0]
	wtentry.insert(0,windata[1])
	wnentry.insert(0,windata[0])
	wwentry.insert(0,windata[2])
	whentry.insert(0,windata[3])
	xpentry.insert(0,windata[4])
	ypentry.insert(0,windata[5])
	createWindow()
	loadwidgets(winid)
	root2.destroy()


## load all the window stored in the database
def getwin():
	global root2
	
	#add warning that current window will be deleted
	if isinstance(win, tk.Toplevel):
		win.destroy()
		
	root2=tk.Toplevel()
	root2.title("Load Window Application")
	root2.geometry("220x400+75+310")
	
	global selindex
	l=tk.Label(root2, text="Window List")
	l.place(x=10,y=10,height=23, width=81)
	global lb
	monospace_font = tkFont.Font(family="Monospace", size=10)
	lb=tk.Listbox(root2, font=monospace_font)
	lb.place(x=10,y=30,height=300, width=200)

	btn2=tk.Button(root2, text="Select", command=pickwin)
	btn2.place(x=10,y=340,height=33, width=100)

	## load data for from windows table
	conn=sq.connect('pywin.db')
	c=conn.cursor()
	c.execute('SELECT *,oid FROM windows')
	wins=c.fetchall()
	conn.commit()
	conn.close
	
	for w in wins:
		lbstr=str(w[6])+"     "
		lbstr = lbstr[0:4]+str(w[1])
		lb.insert('end',lbstr)

	root2.focus_force()

def choose_bg_color():
	global bgcolor
	bgcolor = colorchooser.askcolor(title="Choose Color", color=bgcolor)
	bgcolor = bgcolor[1]
	bgc_frame.config(bg=bgcolor)


def choose_fg_color():
	global fgcolor
	fgcolor = colorchooser.askcolor(title="Choose Color", color=fgcolor)
	fgcolor = fgcolor[1]
	fgc_frame.config(bg=fgcolor)


## quit the app destry the open windows
def quitapp():
	
	print(str(type(win)))
	if isinstance(win,tk.Toplevel):
		win.destroy()
	root.destroy()
	
	
	
### update the existing window - title, size and position	
def edit_window():
	win.title(wtentry.get())
	win.geometry(f'{wwentry.get()}x{whentry.get()}+{xpentry.get()}+{ypentry.get()}')


def reset_window():
	global wlist, wnlist, masterlist, masteridx
	widgetct=-1
	mastct=1
	global win, m
	#holds list of tkinter widgets that are masters
	m=[]
	# holds list of the widgets
	wlist=[]
	# holds list of the variable names for the widgets
	wnlist=[]
	# holds the name of the command function or NULL if not needed
	cmdlst=[]
	# holds the name of the master for this widget
	masterlist=[]
	masteridx=[]
	wigbox.delete(0,tk.END)
	win.destroy()
	wbutton.config(state="active")
	lwbutton.config(state="active")
	button.config(state="active")
	write_button.config(state="disable")
	edit_button.config(state="disable")
	editwin_button.config(state="disable")
	resetwin_button.config(state="active")
	wtentry.delete(0,'end')
	wnentry.delete(0,'end')
	whentry.delete(0,'end')
	wwentry.delete(0,'end')
	xpentry.delete(0,'end')
	ypentry.delete(0,'end')
	clr_widget_fields()
	update_mode("window")
	global winid
	winid=-1
	win=""
	widLabel.config(text=f'WID: {str(winid)}')


###########################################
######
###### start of main code
######
###########################################
global winid
winid=-1
global bgcolor, fgcolor
global dfltbg, dfltfg

ost=platform.system()
## main window definition  Darwin is Macos
root = tk.Tk()
if ost=="Darwin":
	root.geometry("620x670+600+5")
else:
	root.geometry("620x670+400+5")
root.title("Python/Tkinter GUI Designer")


## frame at top fo screen for the widget types
wgf = tk.LabelFrame(root,text="Widget Types",  width=600, height=120, borderwidth=3)
wgf.place(x=4,y=1)

widgets = [
    "Button", "Label", "Entry", "Text", "Checkbutton", 
    "Radiobutton", "Spinbox", "Listbox", "Scrollbar", "MenuButton",
    "Scale", "PhotoImage", "Canvas", "Frame", "LabelFrame"
]

# list of widget types that can have a command assignment
wigcmd = [
	"Button", "Checkbutton", "Radiobutton", "Spinbox", "Scale", "Menu"
]
#list of widget types that can have text assignment
wigtxt = [
	"Button", "Label","Checkbutton", "Radiobutton", "LabelFrame"
] 

#list of widgets that can use color
wigcol =[
	"Button", "Label","Checkbutton", "Radiobutton", "LabelFrame",
	"Frame", "Listbox", "Canvas", "Scrollbar", "Text", "Scale"
]
# list of widgets that use to and from_
wigtofrom = [ "Spinbox", "Scale"]

## StringVar for which widget type radio button
wvar = tk.StringVar(value=widgets[0])

for i, widget in enumerate(widgets):
	rb = tk.Radiobutton(root, text=widget, variable=wvar, value=widget, command=change_widget)
	rb.place(x=(i % 5) * 110 + 10, y=(i // 5) * 25 + 20)

## frame for middle of screen widget info
wif=tk.LabelFrame(root,text="Widget Info", width=600, height=400, borderwidth=3)
wif.place(x=4,y=120)

#widget properties
name_label = tk.Label(root, text="Name")
name_label.place(x=10, y=300)
name_entry = tk.Entry(root)
name_entry.place(x=60, y=300)
name_entry.bind("<FocusOut>", update_cmdfnc)
 
cmd_label = tk.Label(root, text="Command:")
cmd_label.place(x=240, y=300)
cmd_entry = tk.Entry(root)
cmd_entry.place(x=315, y=300)

master_options = ["root"]
mastervar = StringVar(value="root")
master_label=tk.Label(root, text="Master")
master_label.place(x=10, y=330)
master_om = tk.OptionMenu(root, mastervar, "root")
master_om.place(x=60,y=330, width=100, height=25)

caption_label = tk.Label(root, text="Text")
caption_label.place(x=10, y=360)
caption_entry = tk.Entry(root)
caption_entry.place(x=60, y=360, width=100)

x_label = tk.Label(root, text="Xpos")
x_label.place(x=10, y=390)
x_entry = tk.Entry(root)
x_entry.place(x=60, y=390, width=50)

y_label = tk.Label(root, text="Ypos")
y_label.place(x=130, y=390)
y_entry = tk.Entry(root)
y_entry.place(x=175, y=390, width=50)

bgc_btn = tk.Button(root, text="BG col", command=choose_bg_color)
bgc_btn.place(x=235, y=390, width=75, height=25)
bgc_frame=tk.Frame(root, borderwidth=2, relief="groove")
bgc_frame.place(x=315,y=392, height=22, width=25)
bgcolor = bgc_btn['bg']
dfltbg = bgcolor

width_label = tk.Label(root, text="Width")
width_label.place(x=10, y=420)
width_entry = tk.Entry(root)
width_entry.place(x=60, y=420, width=50)

height_label = tk.Label(root, text="Height")
height_label.place(x=130, y=420)
height_entry = tk.Entry(root)
height_entry.place(x=175, y=420, width=50)


fgc_btn = tk.Button(root, text="FG col", command=choose_fg_color)
fgc_btn.place(x=235, y=420, width=75, height=25)
fgc_frame=tk.Frame(root, borderwidth=2, relief="groove")
fgc_frame.place(x=315,y=422, height=22, width=25)
fgcolor = fgc_btn['fg']
dfltfg=fgcolor
fgc_frame['bg']=dfltfg


from_label = tk.Label(root, text="From")
from_label.place(x=10, y=450)
#from_label.place_forget()
from_entry = tk.Entry(root)
from_entry.place(x=60, y=450, width=50)
#from_entry.place_forget()

to_label = tk.Label(root, text="To")
to_label.place(x=130, y=450)
#to_label.place_forget()
to_entry = tk.Entry(root)
to_entry.place(x=175, y=450, width=50)
#to_entry.place_forget()

button=tk.Button(root,text="Make Widget", command=createWidget)
button.place(x=10,y=480)
button.config(state="disabled")
#root.bind('<Return>', lambda event:createWidget())

update_button=tk.Button(root,text="Update Widget", command=updateWidget)
update_button.place(x=165,y=480)
update_button.config(state="disabled")

clear_button=tk.Button(root, text="Clear Widget", command=clear_widget)
clear_button.place(x=325,y=480)

wf = tk.LabelFrame(root,text="Window",  width=600, height=140, borderwidth=3)
wf.place(x=4,y=520)


##
## New window properties
##
l=tk.Label(root, text="Window Title")
l.place(x=10,y=545)
wtentry=tk.Entry(root, width=12)
wtentry.place(x=120,y=545)
wtentry.insert(0,"Title")

l=tk.Label(root, text="App Name")
l.place(x=250,y=545)
wnentry=tk.Entry(root,width=10)
wnentry.place(x=330,y=545)
wnentry.insert(0,"myapp")

l=tk.Label(root, text="Window Width")
l.place(x=10,y=575)
wwentry=tk.Entry(root, width=4)
wwentry.place(x=120,y=575)
wwentry.insert(0,"350")

l=tk.Label(root, text="Window Height")
l.place(x=10,y=600)
whentry=tk.Entry(root, width=4)
whentry.place(x=120,y=600)
whentry.insert(0,"300")

l=tk.Label(root, text="X Position")
l.place(x=250,y=575)
xpentry=tk.Entry(root, width=4)
xpentry.place(x=330,y=575)
xpentry.insert(0,"10")

l=tk.Label(root, text="Y Position")
l.place(x=250,y=600)
ypentry=tk.Entry(root, width=4)
ypentry.place(x=330,y=600)
ypentry.insert(0,"10")

# Create a monospace font need to check for system type "Menlo" for mac
if (ost=="Darwin"):
	monospace_font = tkFont.Font(family="Menlo", size=10)
elif (ost=="Windows"):
	monospace_font = tkFont.Font(family="Consolas", size=10)
else:
	monospace_font = tkFont.Font(family="Monospace", size=10)

wigbox=tk.Listbox(root, font=monospace_font)
wigbox.place(x=60,y=140,width=350,height=150)

edit_button=tk.Button(root, text="Edit", command=edit_widget)
edit_button.place(x=415,y=140, width=125)
edit_button.config(state="disabled")


widLabel=tk.Label(root, text="WID :")
widLabel.place(x=10, y=625)

#fnLabel=tk.Label(root,text="File name: ")
#fnLabel.place(x=120, y=625)

modelabel=tk.Label(root, text="Mode:")
modelabel.place(x=120, y=625)


wbutton=tk.Button(root,text="MakeWin", command=createWindow)
wbutton.place(x=430,y=540,width=75, height=30)

lwbutton=tk.Button(root, text="LoadWin", command = getwin)
lwbutton.place(x=520,y=540, width=75, height=30)

editwin_button = tk.Button(root, text="Update",command=edit_window)
editwin_button.place(x=430, y=575, width=75, height=30)
editwin_button.config(state="disabled")

resetwin_button = tk.Button(root, text="Reset",command=reset_window)
resetwin_button.place(x=520, y=575, width=75, height=30)
resetwin_button.config(state="disabled")

write_button = tk.Button(root, text="Save", command=write_widget_code)
write_button.place(x=430, y=610, width=75, height =30)
write_button.config(state="disabled")

quit_button = tk.Button(root, text="Quit", command=quitapp)
quit_button.place(x=520, y=610, width=75, height=30)

# tracks number of widgets
widgetct=-1
mastct=1

global m, wlist, wnlist, cmdlst, masterlist, masteridx

#holds list of tkinter widgets that are masters
m=[]
# holds list of the widgets
wlist=[]
# holds list of the variable names for the widgets
wnlist=[]
# holds the name of the command function or NULL if not needed
cmdlst=[]
# holds the name of the master for this widget
masterlist=[]
# index to the mastlist[] for this widget
masteridx=[]


# entry mode "add" or "update or "window", "old"-need to create window
# window - no window defined yet
# add - window - but new application
# update - editing widgets
# old - loaded existing app from the data base

#global mode
#mode = "window"
update_mode("window")

## win is the variable for the tkinter application window

win=""
## call make database, if database exists it will just return
makedb()

root.focus_force()
wtentry.focus_force()
root.mainloop()


