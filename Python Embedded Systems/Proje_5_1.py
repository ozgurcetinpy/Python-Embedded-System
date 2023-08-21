import socket
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# DEFINE WINDOW
root = Tk()
root.title("Proje_5")
root.resizable(1,1)
root.geometry("600x600")

# DEFINE VARIABLES
HEADER = 64
FORMAT = "utf-8"
read_data = 256
string_separators = " | "
connected = False

# DEFINE COLORS
grey = "#1a202c"
white = "#fffeff"
root_color = "#000000"
root.config(bg=root_color)
scrollbar_color = "#81c7a5"



# DEFINE FUNCTIONS
def Connect():
    global connected
    global server
    if not connected:
        try:
            server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)           
            server.settimeout(2)
            server.connect(("192.168.25.70", 61))
            server.settimeout(None)
            connection_text.config(text="Bağlandı")
            connection_button.config(text="DURDUR")
            connected = True
        except Exception as err:
            messagebox.showinfo("Error","Connection Error {}".format(err))
            connected = False
            connection_button.config(text="Bağlan")
    else:
        try:
            socket.shutdown(socket.SHUT_RDWR)
            socket.close()
            connection_button.config(text="Bağlan")
            connection_text.config(text="Bağlantı kesildi")
            connected = False
        except Exception as err:
            messagebox.showinfo("Error","Connection Error : {}".format(err))
            connected = False
            connection_button.config(text="DURDUR")

def ReadCSV():
    global liste
    with open("Proje_5.csv","r") as file:
        content = file.readlines()
        i = 0
        liste = []
        while True:
            if i == 15:
                break
            else:
                var = content[i].split(",")[1]
                i +=1
                liste.append(var)
        return liste

def Count():
    with open("Proje_5.csv","r") as file:
        var1 = len(list(file.readlines()))
        return var1

def LedOnOff(x):
    print(x)
    # global connected,my_text
    # if connected:
    #     for i in range(Count()):
    #         var1 = ReadCSV()[i-0]
    #         server.sendall(var1.encode())
    #         data_from_server = server.recv(HEADER)
    #         var = str(data_from_server)
    #         var2 = var.split("|")[1]
    #         string = f"Konum: {var1}, Durum: {var2}"
    #         my_text.config(text=string)
liste = []           

def MakeLabel():
    for i in range(Count()):
        my_label = ttk.Label(scrollable_frame,text="LED" + str(i+1),font=("Times New Roman",12),foreground="#5e4a4a",width=15)
        my_label.grid(row=i,column=0,padx=(5,5),pady=15)

def MakeButton():
    global liste
    for i in range(Count()):
        liste.append(ttk.Button(scrollable_frame,text="OKU/DUR " + str(i) ,width=15,command = lambda: LedOnOff(i+1)))
        # my_button.grid(row=i,column=1,padx=(10,10),pady=15)

def GridLoop():
    print(liste)
    for i in range(len(liste)):
        liste[i].grid(row=i,column=1,padx=(10,10),pady=15)


def MakeConstantButton():
    for i in range(Count()):
        my_constant_button = ttk.Button(scrollable_frame,text="Sürekli Oku "  + str(i),width=15)
        my_constant_button.grid(row=i,column=2,padx=(10,85),pady=15)

def MakeSituationText():
    global my_text
    for i in range(Count()):
        my_text = ttk.Label(scrollable_frame,text="--",justify=CENTER,width=20)
        my_text.grid(row=i,column=3,padx=5,pady=15)






# DEFINE SCROLLBAR
connection_frame = Frame(root)
container = ttk.Frame(root)
canvas = Canvas(container,bg=root_color)
my_scrollbar = ttk.Scrollbar(container,orient="vertical",command=canvas.yview)

connection_frame.grid(row=0,column=0)
container.grid(row=1,column=0)
canvas.pack(side="left", fill="both",expand=True,ipadx=100,ipady=145)
scrollable_frame = ttk.Frame(canvas)
my_scrollbar.pack(side="right", fill="y")


scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=my_scrollbar.set)


# CONNECTION BUTTON AND TEXT
connection_button = Button(connection_frame,text="Bağlan",width=30,height=2,bg=grey,fg=white,command=Connect)
connection_button.grid(row=0,column=0,padx=1,pady=1,sticky="WE")
connection_text = Label(connection_frame,text="Bağlantı Yok",bg=grey,fg=white)
connection_text.grid(row=0,column=1,sticky="NS",padx=1,pady=1)

MakeLabel()
MakeButton()
GridLoop()
MakeConstantButton()
MakeSituationText()



# DEFINE LOOP WINDOW
root.mainloop()