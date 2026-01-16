#!/usr/bin/python3
#### updated dnd.py using ai generated code for interface
## updated on mac with github desktop

import tkinter as tk
from tkinter import IntVar, StringVar
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter import filedialog as fd
import platform
import sys
import sqlite3 as sq
from windb import makedb



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
    
    
def clr_widget_fields():
	# clear all the entry boxes
	name_entry.delete(0,"end")
	caption_entry.delete(0,"end")
	x_entry.delete(0,"end")
	y_entry.delete(0,"end")
	height_entry.delete(0,"end")
	width_entry.delete(0,"end")
	cmd_entry.delete(0,"end")
	cmdtext.delete("1.0", tk.END)
	from_entry.delete(0,"end")
	to_entry.delete(0,"end")

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
		cmdtext.config(state="normal")
	else:
		cmd_entry.delete(0,'end')
		cmdtext.delete(1.0, 'end')
		cmd_entry.config(state="disable")
		cmdtext.config(state="disable")
	if (wig in wigtxt):
		caption_entry.config(state="normal")
	else:
		caption_entry.delete(0,'end')
		caption_entry.config(state="disable")
		
		
	if(wig=="Spinbox"):
		from_label.place(x=10, y=450)
		from_entry.place(x=60, y=450, width=50)
		to_label.place(x=130, y=450)
		to_entry.place(x=175, y=450, width=50)

	else:
		from_label.place_forget()
		from_entry.place_forget()
		to_label.place_forget()
		to_entry.place_forget()


## create name of commnand function
def update_cmdfnc(event):
	wig=wvar.get()
	if (wig in wigcmd and name_entry.get() !="" and mode=="add"):
		cmd_entry.delete(0,"end")
		nstr=name_entry.get()
		cmd_entry.insert(0,"on_" + nstr.replace(" ","_") + "_clicked")
		cmdtext.insert(1.0,f'def on_{nstr.replace(" ","_")}_clicked():\n\tprint("test")\n')
		
#Save the updated widget
def updateWidget():
	global ew
	global edit_index
	wnlist[edit_index]=name_entry.get()
	cmdlst[edit_index]=cmd_entry.get()
	ew.config(text=caption_entry.get())
	ew.place(x=x_entry.get(), y=y_entry.get(), width=width_entry.get(), height=height_entry.get())
	#ew.place(x=x_entry.get(), y=y_entry.get())
	wstr=parse_widget_type(ew)+"               "
	wstr=wstr[0:15]+wnlist[edit_index]
	wigbox.delete(edit_index)
	wigbox.insert(edit_index,wstr)
	clr_widget_fields()
	button.config(state="active")
	update_button.config(state="disable")
	global mode
	mode="add"
	print(wnlist)
	
# update form with widget info for widget to change
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
		cmdtext.insert(1.0,proclist[index])
		caption_entry.insert(0,w.cget("text"))
		if (masterlist[index]!="root"):
			mstridx=masteridx[index]
			x_entry.insert(0,str(w.winfo_x()-m[mstridx].cget("borderwidth")))
			y_entry.insert(0,str(w.winfo_y()-m[mstridx].cget("borderwidth")))
		else:
			x_entry.insert(0,w.winfo_x())
			y_entry.insert(0,w.winfo_y())
			
		width_entry.insert(0,w.winfo_width())
		height_entry.insert(0,w.winfo_height())
		if (wtype=="Spinbox"):
			from_entry.insert(0,w.cget("from"))
			to_entry.insert(0,w.cget("to"))
		button.config(state="disable")
		update_button.config(state="active")
		name_entry.focus_force()
		global mode
		mode="update"
		print(str(type(w)))


# clear all widget fields and put in "add" mode 
# this will reject changes in update mode
def clear_widget():
	clr_widget_fields()
	update_button.config(state="disable")
	button.config(state="active")
	name_entry.focus_force()
	global mode
	mode="add"

## bind function for not allowing the user window to be closed	
def on_closing():
	pass

# Create the target window
def createWindow(text):
    global win
    global mode
    win=tk.Tk()
    win.title(text)
    
    # Bind the close event to the on_closing function
    win.protocol("WM_DELETE_WINDOW", on_closing)
    
    gstr=wwentry.get()+"x"+whentry.get()+"+"+xpentry.get()+"+"+ypentry.get()
    print(gstr)
    win.geometry(gstr)
    wbutton.config(state="disabled")
    button.config(state="active")
    write_button.config(state="active")
    edit_button.config(state="active")
    wtentry.config(state="disable")
    wwentry.config(state="disable")
    whentry.config(state="disable")
    xpentry.config(state="disable")
    ypentry.config(state="disable")
    m.append(win)
    mode="add"
    print("master list = "+str(m))
    
    
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
    widgetct=widgetct+1
    caption=caption_entry.get()
    cmd=cmd_entry.get()
    cmdcode=cmdtext.get(1.0, "end")
    mindex=master_options.index(mastervar.get())
    print(f"master options = {master_options} master_index = {mindex}")
    global m
    #Label
    if (wvar.get() == "Label"):
        w=tk.Label(m[mindex], text = caption)
        w.place(x=x_entry.get(), y=y_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
        print(f"x={w.winfo_x()}")            
    # Button
    elif (wvar.get() == "Button"):
        w=tk.Button(m[mindex], text=caption)
        w.place(x=x_entry.get(), y=y_entry.get(), height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
    # Entry Box
    elif (wvar.get() == "Entry"):
        w=tk.Entry(m[mindex])
        w.insert(0,caption)
        w.place(x=x_entry.get(), y=y_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
    # Entry Box
    elif (wvar.get() == "Text"):
        w=tk.Text(m[mindex])
        w.insert("1.0",caption)
        w.place(x=x_entry.get(), y=y_entry.get(),height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
    # Checkbutton Box
    elif (wvar.get() == "Checkbutton"):
        w=tk.Checkbutton(m[mindex],text=caption)
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
    # ListBox
    elif (wvar.get() == "Listbox"):
        w=tk.Listbox(m[mindex])
        w.place(x=x_entry.get(), y=y_entry.get(),height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
    elif (wvar.get() == "LabelFrame"):
        w=tk.LabelFrame(m[mindex], text=caption, borderwidth=2)
        w.place(x=x_entry.get(), y=y_entry.get(),height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
        m.append(w)
        master_options.append(name_entry.get().replace(" ","_"))
        opt=name_entry.get().replace(" ","_")
        master_om['menu'].add_command(label=opt, command=tk._setit(mastervar, opt))
    elif (wvar.get() == "Frame"):
        w=tk.Frame(m[mindex], borderwidth=2, relief=tk.GROOVE)
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
    proclist.append(cmdcode)
    masterlist.append(mastervar.get())
    masteridx.append(mindex)
    print(cmdlst)
    print(cmd)
    print(wlist)
    print(masterlist)
    wnlist.append(name_entry.get().replace(" ","_"))
    wname=name_entry.get()
    print(wnlist)
    clr_widget_fields()
    mystr=parse_widget_type(w)
    mystr=mystr+"                    "
    mystr=mystr[0:15]
    lbstr=mystr + wname
    wigbox.insert("end",lbstr)
    

def write_widget_code():
	ctr=0
	filedir=fd.asksaveasfilename()
	fnLabel.config(text=f"File Name = {filedir}")
	
	with open(filedir,"w") as f:
		# write imports and window def
		f.write("import tkinter as tk\n")
		f.write("from tkinter import IntVar\n\n")
		f.write("root=tk.Tk()\n")
		titlestr='root.title("' + wtentry.get() + '")'
		f.write(titlestr)
		f.write("\n")
		pstr='root.geometry("'+ wwentry.get() + 'x' + whentry.get() + '+' + xpentry.get() + '+' + ypentry.get()+'")'
		f.write(pstr)
		f.write("\n\n")
		
		for index, c in enumerate(cmdlst):
			if (c!="" and proclist[index]==""):
				cstr="def " + c + "():\n"
				cstr2='\tprint("in ' + c + '")\n'
				f.write(cstr)
				f.write(cstr2)
				f.write("\n")
			elif (c!="" and proclist[index]!=""):
				f.write(proclist[index])
				f.write("\n")
		
		# write out all the widgets
		for index,w in enumerate(wlist):
			print(f"index = {index}  cmd={cmdlst[index]} w={str(w)}")
			wstr=str(type(w)).split(".")[1]
			wstr=wstr.split("'")[0]
			mstr=masterlist[index]
				
			if (wstr!="Listbox" and wstr!="Text" and wstr!="Frame"):
				pstr = wnlist[ctr] + '=tk.' + wstr+'('+mstr+', text="' + w.cget('text') +'"' 
			else:
				 pstr = wnlist[ctr] + '=tk.' + wstr+'('+mstr
			if (wstr=="Frame"):
				pstr=pstr+', borderwidth=2, relief="groove"'
			if (cmdlst[index]!=""):
				pstr=pstr+", command="+str(cmdlst[index])
			pstr=pstr + ')'
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
		
		

		with open("/Users/thomasraidna/PythonCode/logfile.txt","w") as lf:
			lf.write("data dump for application\n")
			lf.write(f"Title  = {win.title()}\n")
			lf.write(f"X      = {win.winfo_x()}\n")
			lf.write(f"Y      = {win.winfo_y()}\n")
			lf.write(f"Width  = {win.winfo_width()}\n")
			lf.write(f"Height = {win.winfo_height()}\n")
			lf.write("done with window\nWidgets \n\n")
			for i, w in enumerate(wlist):
				lf.write(f"Index  = {str(i)}\n")
				lf.write(f"Type   = {parse_widget_type(w)}\n")
				lf.write(f"Name   = {wnlist[i]}\n")
				lf.write(f"Master = {masterlist[masteridx[i]]}\n")
				lf.write(f"Text   = {w.cget("text")}\n")
				lf.write(f"X      = {w.winfo_x()}\n")
				lf.write(f"Y      = {w.winfo_y()}\n")
				lf.write(f"Width  = {w.winfo_width()}\n")
				lf.write(f"Height = {w.winfo_height()}\n")
				lf.write(f"Procnm = {cmdlst[i]}\n")
				lf.write(f"Procedure=\n{proclist[i]}\n")
			lf.write("\nDone with Widgets\n")
			lf.close()
		
		conn=sq.connect('pywin.db')
		c = conn.cursor()
		
		sql="""INSERT INTO windows(winname, title, height, width, x, y)
			VALUES(?,?,?,?,?,?)"""
		sqldata=('NAME',win.title(),win.winfo_height(),win.winfo_width(),win.winfo_x(),win.winfo_y())
		
		c.execute(sql, sqldata)
		oid=c.lastrowid
		conn.commit()
		conn.close()
		messagebox.showinfo("Information", f"File {filedir} has been written\nlast index={oid} ")	


def quitapp():
	root.quit()
	

ost=platform.system()
## main window definition
root = tk.Tk()
if ost=="Darwin":
	root.geometry("620x670+600+5")
else:
	root.geometry("620x670+400+5")
root.title("Python Drag and Drop GUI Designer")



## frame at top fo screen for the widget types
wgf = tk.LabelFrame(root,text="Widget Types",  width=600, height=120, borderwidth=3)
wgf.place(x=4,y=1)


# widgets = [
    # "Button", "Label", "Entry", "Text", "Frame", 
    # "Checkbutton", "Radiobutton", "Listbox", "Scrollbar", 
    # "Canvas", "Menu", "MenuButton", "Scale", "Spinbox", 
    # "Message", "PhotoImage", "Toplevel", "PanedWindow", 
    # "LabelFrame", "Notebook"
#]

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
 
cmd_label = tk.Label(root, text="Command Function")
cmd_label.place(x=240, y=300)
cmd_entry = tk.Entry(root)
cmd_entry.place(x=380, y=300)

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

width_label = tk.Label(root, text="Width")
width_label.place(x=10, y=420)
width_entry = tk.Entry(root)
width_entry.place(x=60, y=420, width=50)

height_label = tk.Label(root, text="Height")
height_label.place(x=130, y=420)
height_entry = tk.Entry(root)
height_entry.place(x=175, y=420, width=50)

from_label = tk.Label(root, text="From")
from_label.place(x=10, y=450)
from_label.place_forget()
from_entry = tk.Entry(root)
from_entry.place(x=60, y=450, width=50)
from_entry.place_forget()

to_label = tk.Label(root, text="To")
to_label.place(x=130, y=450)
to_label.place_forget()
to_entry = tk.Entry(root)
to_entry.place(x=175, y=450, width=50)
to_entry.place_forget()

## code for command = fucntion here to make last when tabbing
cmdtext=tk.Text(root)
cmdtext.place(x=240,y=330,width=305,height=150)

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
wtentry=tk.Entry(root, width=30)
wtentry.place(x=120,y=545)
wtentry.insert(0,"Title")

l=tk.Label(root, text="Window Width")
l.place(x=10,y=575)
wwentry=tk.Entry(root, width=4)
wwentry.place(x=120,y=575)
wwentry.insert(0,"350")

l=tk.Label(root, text="Window Height")
l.place(x=10,y=600)
whentry=tk.Entry(root, width=4)
whentry.place(x=120,y=600)
whentry.insert(0,"600")

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
	pass
else:
	monospace_font = tkFont.Font(family="Monospace", size=10)

wigbox=tk.Listbox(root, font=monospace_font)
wigbox.place(x=60,y=140,width=350,height=150)

fnLabel=tk.Label(root,text="File name: ")
fnLabel.place(x=10, y=625)

wbutton=tk.Button(root,text="Make Window", command= lambda: createWindow(wtentry.get()))
wbutton.place(x=450,y=540,width=125, height=30)

write_button = tk.Button(root, text="Save", command=write_widget_code)
write_button.place(x=450, y=575, width=125, height =30)
write_button.config(state="disabled")

edit_button=tk.Button(root, text="Edit", command=edit_widget)
edit_button.place(x=415,y=140, width=125)
edit_button.config(state="disabled")

quit_button = tk.Button(root, text="Quit", command=quitapp)
quit_button.place(x=450, y=610, width=125, height=30)

# tracks number of widgets
widgetct=-1
mastct=1

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
#list of python code for command = widgets
proclist=[]
# entry mode "add" or "update or "window"-need to create window

global mode
mode = "window"

makedb()

root.focus_force()
wtentry.focus_force()
root.mainloop()
