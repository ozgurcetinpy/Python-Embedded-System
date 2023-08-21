from tkinter import *

top = Tk()
top.geometry("100x100+10+10")
ALL = N+S+E+W
padding = 2
width = 3

frame = Frame(top)
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.pack(expand=1, fill=BOTH, padx=1, pady=1)

canvas = Canvas(frame)
canvas.grid(row=0, column=0, sticky=NW+SE)

def add_checkbox(x,y):
    check = IntVar()
    Checkbutton(canvas,variable=check).grid(row=x,column=y,padx=padding,pady=padding)

def add_label(x,y,text):
    Label(canvas, text=text).grid(row=x, column=y, padx=padding, pady=padding)  

add_checkbox(0,0)
add_label(0,0,"x")
add_label(1,0,"y") 
add_label(2,0,"z") 
add_label(3,0,"1") 
add_label(4,0,"2") 
add_label(5,0,"3") 
add_label(6,0,"4") 
add_label(7,0,"5") 
add_label(8,0,"6")
add_label(9,0,"6")
add_label(10,0,"6")
add_label(11,0,"6")
add_label(12,0,"6")
add_label(13,0,"6")
add_label(14,0,"6")
add_label(15,0,"6")
add_label(16,0,"6")



Button(frame, text="Submit").grid(row=3, column=0, columnspan=width, sticky=ALL)

yscrollbar = Scrollbar(frame, orient=VERTICAL)
yscrollbar.grid(row=0, column=1, sticky=NE+SE)

canvas.configure(yscrollcommand=yscrollbar.set,     scrollregion=canvas.bbox("all"))
canvas.create_window((4,4), window=frame, anchor="nw")
yscrollbar.configure(command=canvas.yview)

frame.pack()
top.mainloop()