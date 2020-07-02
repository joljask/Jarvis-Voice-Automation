# importing whole module
from tkinter import *
from tkinter.ttk import *
import time as t

import threading
# importing strftime function to
# retrieve system's time
from time import strftime

# creating tkinter window
root = Tk()
root.title('Clock')


# This function is used to
# display time on the label
def time():
    string = strftime('%H:%M:%S %p')
    lbl.config(text=string)
    lbl.after(1000, time)


# Styling the label widget so that clock
# will look more attractive
lbl = Label(root, font=('calibri', 40, 'bold'),
            background='purple',
            foreground='white')

# Placing clock at the centre
# of the tkinter window
lbl.pack(anchor='center')
time()

def count():
    for i in  range(1,1000):

        print(i)
        t.sleep(1)

t1 = threading.Thread(target=count)
t1.start()
btn = Button(root, text = "count", command = count).pack()
mainloop()
