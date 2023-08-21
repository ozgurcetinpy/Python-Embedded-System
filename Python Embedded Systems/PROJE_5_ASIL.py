import functools
from os import name
import threading
from tkinter import constants
try:
    from tkinter import *
    import socket
    from tkinter import messagebox
    import time
except ImportError: 
    from tkinter import *
    import socket
    from tkinter import messagebox

# DEFINE WINDOW
root = Tk()
root.title("Proje_5")
root.geometry("700x700+700+30")
root.iconbitmap("Proje5\Form1.ico")
frame_1=Frame(root)


# DEFINE VARIABLES
HEADER = 64
FORMAT = "utf-8"
# read_data = 256
# string_separators = " | "
connected = False
liste_isim = []
liste_harf = []
liste_tipi = []
liste_min = []
liste_max = []
my_infos = []
my_threads = {}
button_thread_statu = False
constant_button_thread_statu = False
key = 1


# DEFINE COLORS
grey = "#BABABA"
white = "#fffeff"
root_color = "#072645"
root.config(bg=root_color)
scrollbar_color = "#81c7a5"


# DEFINE CANVAS AND SCROLLBAR
canvas=Canvas(frame_1,width=680, height=620)
frame_2=Frame(canvas)
myscrollbar=Scrollbar(frame_1,orient="vertical",command=canvas.yview) 
canvas.create_window((0,0),window=frame_2,anchor='nw')


# DEFINE FUNCTIONS
def Connect():                # Bağlantıyı gerçekleştiriyor
    global connected
    global server
    if not connected:
        try:
            server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    # socket oluşturma işlemi       
            server.settimeout(2)                                   # Bağlanamama durumunda 2 saniye sonra zaman aşımına uğrar.
            server.connect(("192.168.25.70",61))             #  ip adresi e port numarası atıyoruz.
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


def CSV_ROW_Count():    # Satır Sayısı Sayma
    with open("Proje_5.csv","r") as file:           # CSV dosyasındaki satır sayısını int olarak geriye döndürüyor.
        var1 = len(list(file.readlines()))         #  15
        return var1

# Dosya Okuma İşlevi
def ReadCSV():               
    global liste_isim,liste_harf,liste_tipi,liste_min,liste_max
    with open("Proje_5.csv","r") as file:
        content = file.readlines()
        for i in range(0,CSV_ROW_Count()):       # CSV dosyasındaki satırların 1. indislerini list olarak geri döndürüyor.
            string_bolunmus = content[i].split(",")
            liste_isim.append(string_bolunmus[0])    
            liste_harf.append(string_bolunmus[1]) #  ==>  ['1', '2', '3', '4', '5', '6', '7', '8', 'a', 'b', 'c', 'd', 'e']
            liste_tipi.append(string_bolunmus[2])
            liste_min.append(string_bolunmus[3])
            liste_max.append(string_bolunmus[4])
        
ReadCSV()   # Oluşan listeleri hafızada tutabilmesi için fonksiyonu bir kere çalıştırıyoruz. 

# Her buton için Read Once Buton Komutu 
def ReadOnce(button_number):
    global connected,liste_harf
    global my_infos
    if connected:
        server.sendall(liste_harf[button_number].encode())   # değişkeni servera gönderiyoruz.                 
        data_from_server = server.recv(HEADER)   # serverdan (arduinodan) aldığımız datayı değişkene atadık.
        var = str(data_from_server)
        var2 = var.split("|")[1]
        string = f"{liste_tipi[button_number]}: {button_number+1}, Cevap: {var2}"
        my_infos[button_number].config(text=string)
        if int(var2) <= int(liste_max[button_number]) and int(var2) >= int(liste_min[button_number]):
            my_infos[button_number].config(bg="green")
        else:
            my_infos[button_number].config(bg="red")
    else:
        messagebox.showinfo("Error","Connection Error\nLütfen Bağlantıyı gerçekleştiriniz. ")    

    
def ThreadLoop(button_number):  
    global my_threads,my_infos
    while True:
        time.sleep(0.5)
        while my_threads[button_number]["status"]:
            server.sendall(liste_harf[button_number].encode())      # değişkeni servera gönderiyoruz.              
            data_from_server = server.recv(HEADER)         # serverdan (arduinodan) aldığımız datayı değişkene atadık.
            var = str(data_from_server)
            var2 = var.split("|")[1]
            string = f"{liste_tipi[button_number]}: {button_number+1}, Cevap: {var2}"
            if int(var2) <= int(liste_max[button_number]) and int(var2) >= int(liste_min[button_number]):
                my_infos[button_number].config(bg="green")
            else:
                my_infos[button_number].config(bg="red")
            my_infos[button_number].config(text=string)
            time.sleep(1)
            
                

# Her buton için Read Constant butonu
def ReadConstant(button_number):
    global my_threads
    if connected:
        if button_number not in my_threads:
            my_threads[button_number] = {"thread":threading.Thread(target=ThreadLoop,args=(button_number,)),"status":True}
            # gelen cevabın iterable bir değişken olması için fonskiyona verdiğimiz argümanı tuple cinsinden belirledik.
            my_threads[button_number]["thread"].start()
            # Oluşan dict'in key = thread bilgisen ulaşıp o threadi başlattık.
            # print(my_threads)
        else:
            my_threads[button_number]["status"] = not my_threads[button_number]["status"]
            # False ise True, True ise False yap
    else:
        messagebox.showinfo("Error","Connection Error\nLütfen Bağlantıyı gerçekleştiriniz. ")


# Make Label
for i in range(CSV_ROW_Count()):
    my_label = Label(frame_2,text=liste_isim[i],justify="center",foreground="white",background="#b5ada7",width=10,height=3)
    my_label.grid(row=i,column=0,padx=(30,40),pady=25)

# Make Button
for i in range(CSV_ROW_Count()):
    my_button = Button(frame_2,text="Read Once",width=10,height=2,command=functools.partial(ReadOnce,i),borderwidth=6)
    my_button.config(foreground="white",background="#7d6f6e")
    my_button.grid(row=i,column=1,padx=55,pady=25)

# Make Constant Button
for i in range(CSV_ROW_Count()):
    my_constant_button = Button(frame_2,text="Read Constant",width=10,height=2,command=functools.partial(ReadConstant,i),borderwidth=6)
    my_constant_button.config(foreground="white",background="#7d6f6e")
    my_constant_button.grid(row=i,column=2,padx=10,pady=25)

# Make Info Text
for i in range(CSV_ROW_Count()):
    my_info = Label(frame_2,text="-----",foreground="white",background="#471310",width=15,height=1)
    my_info.grid(row=i,column=3,padx=(60,90),pady=25)
    my_infos.append(my_info)
# print(len(my_infos))


# DEFINE CONNECTION FRAME 
connection_frame = Frame(frame_2).grid(row=0,column=0)   # Bağlantı Butonunu ve Bilgi veren içeriğin bulunduğu kısım

connection_button = Button(connection_frame,text="Connect",width=35,height=5,command=Connect,borderwidth=6)
connection_button.config(background="#7d6f6e")
connection_text = Label(connection_frame,text="No Connection",width=20,height=2)
connection_text.config(background=grey)
connection_button.grid(row=0,column=0,pady=5)
connection_text.grid(row=1,column=0,pady=5)

# CANVAS CONFIGURATIONS
frame_2.update()
frame_2.config(background="#10477d")
canvas.configure(yscrollcommand=myscrollbar.set, scrollregion="0 0 0 %s" % frame_2.winfo_height())
canvas.grid(row=0,column=0)
myscrollbar.grid(row=0,column=1,sticky='ns')
frame_1.grid()

# DEFINE LOOP
root.mainloop()