import socket
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# DEFINE WINDOW
root = Tk()
root.title("Proje_5")
root.resizable(1,1)
root.geometry("600x600")



# DEFINE COLORS
grey = "#1a202c"
white = "#fffeff"
root_color = "#000000"
root.config(bg=root_color)
scrollbar_color = "#81c7a5"


# DEFINE FUNCTIONS
def Count():
    with open("Proje_5.csv","r") as file:
        var1 = len(list(file.readlines()))
        return var1

def MakeLabel():
    for i in range(Count()):
        my_label = ttk.Label(scrollable_frame,text="LED" + str(i+1),width=35)
        my_label.grid(row=i,column=0,padx=10,pady=15)
        
def MakeButton():
    for i in range(Count()):
        my_button = ttk.Button(scrollable_frame,text="OKU/DUR",width=20)
        my_button.grid(row=i,column=1,padx=10,pady=15,sticky="we")

def MakeSituationText():
    for i in range(Count()):
        my_text = ttk.Label(scrollable_frame,text="Hello World",width=30)
        my_text.grid(row=i,column=2,padx=10,pady=15)



# DEFINE SCROLLBAR
connection_frame = Frame(root)
container = ttk.Frame(root)
canvas = Canvas(container,bg=root_color)
my_scrollbar = ttk.Scrollbar(container,orient="vertical",command=canvas.yview)
frame_1 = ttk.Frame(container)
frame_2 = ttk.Frame(container)
frame_3 = ttk.Frame(container)
frame_1.grid(row=0,column=0)

connection_frame.grid(row=0,column=0)
container.grid(row=1,column=0)
canvas.grid(row=0,column=0,ipadx=100,ipady=145)
scrollable_frame = ttk.Frame(canvas)
my_scrollbar.grid(row=0,column=1,sticky="ns")


scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=my_scrollbar.set)


# CONNECTION BUTTON AND TEXT
connection_button = Button(connection_frame,text="Bağlan",width=30,height=2,bg=grey,fg=white)
connection_button.grid(row=0,column=0,padx=1,pady=1,sticky="WE")
connection_text = Label(connection_frame,text="Bağlantı Yok",bg=grey,fg=white)
connection_text.grid(row=0,column=1,sticky="NS",padx=1,pady=1)

MakeLabel()
MakeButton()
MakeSituationText()

# DEFINE LOOP WINDOW
root.mainloop()