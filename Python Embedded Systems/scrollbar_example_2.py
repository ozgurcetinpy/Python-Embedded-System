from tkinter import *

root = Tk()
root.title('PythonGuides')
root.config(bg='#5F734C')

frame = Frame(root,bg='#A8B9BF')

text_box = Text(root,height=13,width=32,font=(12)  )
text_box.grid(row=0, column=0)
text_box.config(bg='#D9D8D7')

sb = Scrollbar(root,orient=VERTICAL)

sb.grid(row=0, column=1, sticky=NS)

text_box.config(yscrollcommand=sb.set)
sb.config(command=text_box.yview)

for i in range(100):
    my_label = Label(text_box,text="LED " + str(i))
    text_box.insert(END,my_label)


root.mainloop()