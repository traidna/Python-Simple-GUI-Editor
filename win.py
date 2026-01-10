#### updated dnd.py using ai generated code for interface

import tkinter as tk
from tkinter import IntVar
from tkinter import messagebox
import tkinter.font as tkFont

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

## pass in a widget and return a string of widget type parsed
def parse_widget_type(w):
	wstr=str(type(w))
	wstr=wstr.split(".")[1]
	wstr=wstr.split("'")[0]
	return wstr
	
    
# default text in cmd_entry if appropriate type of widget 
def change_widget():
	wig=wvar.get()
	if (wig in wigcmd):
		cmd_entry.config(state="normal")
	else:
		cmd_entry.config(state="disable")


## create name of commnand function
def update_cmdfnc(event):
	wig=wvar.get()
	if (wig in wigcmd and name_entry.get() !="" ):
		cmd_entry.delete(0,"end")
		nstr=name_entry.get()
		cmd_entry.insert(0,"on_" + nstr + "_clicked")


def updateWidget():
	global ew
	global edit_index
	wnlist[edit_index]=name_entry.get()
	cmdlst[edit_index]=cmd_entry.get()
	ew.config(text=caption_entry.get())
	ew.place(x=x_entry.get(), y=y_entry.get(), width=width_entry.get(), height=height_entry.get())
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
		ew=w
		clr_widget_fields()
		name_entry.insert(0,wnlist[index])
		cmd_entry.insert(0,cmdlst[index])
		caption_entry.insert(0,w.cget("text"))
		x_entry.insert(0,w.winfo_x())
		y_entry.insert(0,w.winfo_y())
		width_entry.insert(0,w.winfo_width())
		height_entry.insert(0,w.winfo_height())
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
	

# Create the target window
def createWindow(text):
    global win
    win=tk.Tk()
    win.title(text)
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

		
# Create Widget on working window
def createWidget():
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
    
    #Label
    if (wvar.get() == "Label"):
        w=tk.Label(win, text = caption)
        w.place(x=x_entry.get(), y=y_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)            
    # Button
    elif (wvar.get() == "Button"):
        w=tk.Button(win, text=caption)
        w.place(x=x_entry.get(), y=y_entry.get(), height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
    # Entry Box
    elif (wvar.get() == "Entry"):
        w=tk.Entry(win)
        w.insert(0,caption)
        w.place(x=x_entry.get(), y=y_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
    # Entry Box
    elif (wvar.get() == "Text"):
        w=tk.Text(win)
        w.insert("1.0",caption)
        w.place(x=x_entry.get(), y=y_entry.get(),height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
    # Checkbutton Box
    elif (wvar.get() == "Checkbutton"):
        w=tk.Checkbutton(win,text=caption)
        w.place(x=x_entry.get(), y=y_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)
    #spinbox    
    elif (wvar.get() == "Spinbox"):
        w=tk.Spinbox(win,text=caption)
        w.place(x=x_entry.get(), y=y_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)    
    # ListBox
    elif (wvar.get() == "Listbox"):
        w=tk.Listbox(win)
        w.place(x=x_entry.get(), y=y_entry.get(),height=height_entry.get(), width=width_entry.get())
        w.bind("<ButtonPress-1>", on_drag_start)
        w.bind("<B1-Motion>", on_drag_motion)
        wlist.append(w)

    #if(cmd!=""):
     #   print(cmd)
    name_entry.focus_force()
    cmdlst.append(cmd)
    print(cmdlst)
    print(cmd)
    print(wlist)
    wnlist.append(name_entry.get())
    wname=name_entry.get()
    print(wnlist)
    clr_widget_fields()
    mystr=parse_widget_type(w)
    #mystr=str(type(w))
    #mystr=mystr.split(".")[1]
    #mystr=mystr.split("'")[0]
    mystr=mystr+"                    "
    mystr=mystr[0:15]
    lbstr=mystr + wname
    wigbox.insert("end",lbstr)
    

def write_widget_code():
	ctr=0
	with open("widgets.py","w") as f:
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
		
		for c in cmdlst:
			if (c!=""):
				cstr="def " + c + "():\n"
				cstr2='\tprint("in ' + c + '")\n'
				f.write(cstr)
				f.write(cstr2)
				f.write("\n")
		
		# write out all the widgets
		for index,w in enumerate(wlist):
			print(f"index = {index}  cmd={cmdlst[index]} w={str(w)}")
			wstr=str(type(w)).split(".")[1]
			wstr=wstr.split("'")[0]
			if (wstr!="Listbox" and wstr!="Text"):
				pstr = wnlist[ctr] + '=tk.' + wstr+'(root, text="' + w.cget('text') +'"' 
			else:
				 pstr = wnlist[ctr] + '=tk.' + wstr+'(root'
			
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
		messagebox.showinfo("Information", "File Widgets has been written")



root = tk.Tk()
root.geometry("925x650+300+10")
root.title("Python Drag and Drop GUI Designer")
widgets = [
    "Button", "Label", "Entry", "Text", "Frame", 
    "Checkbutton", "Radiobutton", "Listbox", "Scrollbar", 
    "Canvas", "Menu", "MenuButton", "Scale", "Spinbox", 
    "Message", "PhotoImage", "Toplevel", "PanedWindow", 
    "LabelFrame", "Notebook"
]

wigcmd = [
	"Button", "Checkbutton", "Radiobutton", "Spinbox", "Scale", "Menu"
]

wvar = tk.StringVar(value=widgets[0])

for i, widget in enumerate(widgets):
    rb = tk.Radiobutton(root, text=widget, variable=wvar, value=widget, command=change_widget)
    rb.place(x=(i % 5) * 110 + 10, y=(i // 5) * 30 + 10)


#widget properties
name_label = tk.Label(root, text="Name")
name_label.place(x=10, y=200)
name_entry = tk.Entry(root)
name_entry.place(x=60, y=200)

name_entry.bind("<FocusOut>", update_cmdfnc)
 

cmd_label = tk.Label(root, text="Command Fnc")
cmd_label.place(x=300, y=200)
cmd_entry = tk.Entry(root)
cmd_entry.place(x=400, y=200)

caption_label = tk.Label(root, text="Text")
caption_label.place(x=10, y=230)
caption_entry = tk.Entry(root)
caption_entry.place(x=60, y=230)

x_label = tk.Label(root, text="Xpos")
x_label.place(x=10, y=260)
x_entry = tk.Entry(root)
x_entry.place(x=60, y=260)

y_label = tk.Label(root, text="Ypos")
y_label.place(x=10, y=290)
y_entry = tk.Entry(root)
y_entry.place(x=60, y=290)

width_label = tk.Label(root, text="Width")
width_label.place(x=10, y=320)
width_entry = tk.Entry(root)
width_entry.place(x=60, y=320)

height_label = tk.Label(root, text="Height")
height_label.place(x=10, y=350)
height_entry = tk.Entry(root)
height_entry.place(x=60, y=350)

button=tk.Button(root,text="Make Widget", command=createWidget)
button.place(x=60,y=380)
button.config(state="disabled")
root.bind('<Return>', lambda event:createWidget())

update_button=tk.Button(root,text="Update Widget", command=updateWidget)
update_button.place(x=220,y=380)
update_button.config(state="disabled")

clear_button=tk.Button(root, text="Clear Widget", command=clear_widget)
clear_button.place(x=380,y=380)



## New window properties
wbutton=tk.Button(root,text="Make Window", command= lambda: createWindow(wtentry.get()))
wbutton.place(x=10,y=500)

l=tk.Label(root, text="Window Title")
l.place(x=10,y=545)
wtentry=tk.Entry(root, width=30)
wtentry.place(x=120,y=545)
wtentry.insert(0,"Title")

l=tk.Label(root, text="Window Width")
l.place(x=10,y=575)
wwentry=tk.Entry(root, width=4)
wwentry.place(x=120,y=575)
wwentry.insert(0,"300")

l=tk.Label(root, text="Window Height")
l.place(x=10,y=600)
whentry=tk.Entry(root, width=4)
whentry.place(x=120,y=600)
whentry.insert(0,"200")

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

# Create a monospace font
monospace_font = tkFont.Font(family="Menlo", size=10)
wigbox=tk.Listbox(root, font=monospace_font)
wigbox.place(x=610,y=10,width=300,height=360)

write_button = tk.Button(root, text="Write Code", command=write_widget_code)
write_button.place(x=610, y=600)
write_button.config(state="disabled")

edit_button=tk.Button(root, text="Edit", command=edit_widget)
edit_button.place(x=850,y=380)
edit_button.config(state="disabled")



quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.place(x=850, y=600)

# tracks number of widgets
widgetct=-1

# holds list of the widgets
wlist=[]
# holds list of the variable names for the widgets
wnlist=[]
# holds the name of the command function or NULL if not needed
cmdlst=[]
# entry mode "add" or "update"
global mode
mode = "add"

root.focus_force()
root.mainloop()
