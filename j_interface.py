from tkinter import *
import time
import sys
import random
import psutil
from PIL import ImageTk
from PIL import Image
from Jk_internet import Jk_internet

import requests
import datetime
import random
import sys
import os
import smtplib
import webbrowser
import urllib
import pyttsx3
import speech_recognition as sr
import pyaudio
from PyDictionary import PyDictionary
from tkinter import simpledialog


import threading as t
from temp_jarvis import print_weather
from temp_jarvis import weather_data
from database import write_csv
from database import append_csv
from database import read_csv




jku = Jk_internet()
jkr = Jk_internet()


root = Tk()
root.title("Jarvis The Desktop Assistant")

#Declarations
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


leftImage = "bg4.jpg"
rightImage = "chat1.png"
'''
INITIATE DATABASE
'''
def csv_open():

    import tkinter.ttk as ttk
    import csv

    root = Tk()
    root.title("CONVERSATION")
    width = 500
    height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)

    TableMargin = Frame(root, width=500)
    TableMargin.pack(side=TOP)

    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("date", "time", "conversation"), height=400,
                        selectmode="extended",
                        yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('date', text="date", anchor=W)
    tree.heading('time', text="time", anchor=W)
    tree.heading('conversation', text="conversation", anchor=W)

    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=120)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=1020)

    tree.pack()
    with open('conversation.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            dt = row['date']
            ti = row['time']
            con = row['conversation']

            tree.insert("", 0, values=(dt, ti, con))
    root.mainloop()

if os.path.isfile('conversation.csv'):
    print("pass")
    pass

else:
    write_csv()

'''
TOP OF VOICE ASSISTANT
--------------------------------------------------------------------------------------------------------------------
'''


def speak(audio):
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[len(voices) - 1].id)

    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 62)  # Slows down the speaking speed of the engine voice.

    print("  " + audio)
    engine.say(audio)
    engine.runAndWait()

def command_interface():

    query = simpledialog.askstring("COMMAND", "Enter your command")
    return query

def command():
    cmd = sr.Recognizer()
    with sr.Microphone() as source:
        cmd.adjust_for_ambient_noise(source)  # Adjusts the level to recieve voice even in case of noise in surroundings
        #speak('I am listening')
        print('Listening..')
        audio = cmd.listen(source)
        try:
            query = cmd.recognize_google(audio, language='en-in')
            print('User: ' + query + '\n')
            db = "user : " + query
            append_csv(db)
        except sr.UnknownValueError:
            speak('Sorry ! I did not get that. Could you please type it out ?')
            j_db = "jarvis : " + 'Sorry ! I did not get that. Could you please type it out ?'
            append_csv(j_db)
            #query = str(input('Command: '))
           # query = simpledialog.askstring("COMMAND","Enter your command")
            query = command_interface()
            jt_db = "jarvis : " + query
            append_csv(jt_db)
            print(query)
    return query


def greeting():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning')
        append_csv("jarvis : Good Morning")
    if currentH >= 12 and currentH < 17:
        speak('Good Afternoon')
        append_csv("jarvis : Good Afternoon")
    if currentH >= 17 and currentH != 0:
        speak('Good Evening')
        append_csv("jarvis : Good Evening")

    speak('jarvis here.')
    append_csv("jarvis : jarvis here")
    speak('What would you like me to do for you ?')
    append_csv("jarvis : What would you like me to do for you?")


def find(name, path):
    for root, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def playOnYoutube(query):
    query_string = urllib.parse.urlencode({"search_query": query})
    search_string = str("http://www.youtube.com/results?" + query_string)
    append_csv(search_string)
    speak("Here's what you asked for. Enjoy!")
    append_csv("jarvis : Here's what you asked for. Enjoy")
    webbrowser.open_new_tab(search_string)


def tellAJoke():
    res = requests.get(
        'https://icanhazdadjoke.com/',
        headers={"Accept": "application/json"}
    )
    if res.status_code == 200:
        speak("Okay. Here's one")
        append_csv("jarvis : Okay. Here's one")
        speak(str(res.json()['joke']))
        append_csv("jarvis : "+ str(res.json()['joke']))
    else:
        speak('Oops!I ran out of jokes')
        append_csv("jarvis : Oops!I ran out of jokes")
def temperature():
    city = "bangalore"
    query = 'q=' + city
    w_data = weather_data(query)
    print_weather(w_data, city)
    append_csv(print_weather(w_data, city))

def main_voice():

    time.sleep(5)
    while True:

        query = command()
        query = query.lower()

        if 'play music' in query or 'play a song' in query:
            speak("Here's your music. Enjoy !")
            append_csv("jarvis : Here's your music. Enjoy !")
            os.system('spotify')

        if 'find file' in query:
            speak('What is the name of the file that I should find ?')
            append_csv("jarvis : What is the name of the file that I should find ?")
            query = command()
            filename = query
            print(filename)
            append_csv("jarvis : File name :- "+ filename)
            speak('What would be the extension of the file ?')
            append_csv("jarvis : What would be the extension of the file ?")
            query = command()
            query = query.lower()
            extension = query
            print(extension)
            fullname = str(filename) + '.' + str(extension)
            print(fullname)
            append_csv("jarvis : Full name " + fullname)
            path = r'D:\\'
            location = find(fullname, path)
            speak('File is found at the below location')
            append_csv("jarvis : File is found at the below location")
            print(location)
            append_csv("jarvis : " + location)

        if 'search' in query:
            speak('What should I search for ?')
            append_csv("jarvis : What should I search for ?")
            query = command()
            lib = query
            url = "https://www.google.co.in/search?q=" + (str(lib)) + "&oq=" + (str(
                lib)) + "&gs_l=serp.12..0i71l8.0.0.0.6391.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.UiQhpfaBsuU"
            webbrowser.open_new(url)
            append_csv("jarvis : " + url)

        if 'play on youtube' in query:
            speak('What should I look up for ?')
            append_csv("jarvis : What should I look up for ?")
            query = command()
            playOnYoutube(query)

        if 'joke' in query:
            tellAJoke()
        if 'temperature' in query:
            temperature()
            #append_csv("jarvis" + str(temperature()))

        if 'open word' in query:
            os.system('libreoffice word')
            append_csv("jarvis : Successfully opened word")
            speak("successfully opened word")

        if 'send an email' in query:
            speak('whom would you like to send')
            append_csv("jarvis : whom would you like to send")
            query = command()
            sender = query
            append_csv("user : " + sender)
            speak('what would you like to send')
            append_csv("jarvis : what would you like to send")
            query = command()

            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)

            # start TLS for security
            s.starttls()

            # Authentication
            s.login("jarvisassistant.chetz@gmail.com", "jarvis@123")

            # message to be sent
            message = query
            append_csv("jarvis : " + message)

            # sending the mail
            s.sendmail("jarvisassistant.chetz@gmail.com", sender, message)
            speak("mail sent")
            append_csv("jarvis : mail sent")

            # terminating the session
            s.quit()
        if 'conversation' in query:
            #read_csv()

            #path = os.getcwd()
            #print(path)
            #f_path = path+"/conversation.csv"
            #print(f_path)
            #os.startfile(f_path)
            csv_open()

        if 'that would be all' in query or 'that is it' in query or 'go to sleep jarvis' in query:
            speak('Alright. Have a nice day')
            append_csv("jarvis : Alright. Have a nice day")
            sys.exit()

t1 = t.Thread(target=greeting)
t1.start()

t2 = t.Thread(target=main_voice)

t2.start()


'''
BOTTOM OF VOICE ASSISTANT
--------------------------------------------------------------------------------------------------------------------
'''
# frames  LEFT

leftFrame = Frame(root, width=1000, height=820, background="yellow")


# Background starbackground

backgroundhome = Canvas(leftFrame, width=1000, height=820)
bimage = ImageTk.PhotoImage(Image.open(leftImage))
backgroundhome.create_image(0, 0, anchor=NW, image=bimage)
backgroundhome.pack(fill=BOTH)

'''
buttons

'''

# weather
def weather(event):
    city = "bangalore"
    query = 'q=' + city
    w_data = weather_data(query)
    print_weather(w_data, city)

buttonBG = backgroundhome.create_rectangle(700-10, 235, 800-10, 275, fill= "#94d5d6", outline="grey60")
buttonTXT = backgroundhome.create_text(750-10, 257, text="WEATHER", font = "bold")
backgroundhome.tag_bind(buttonBG, "<Button-1>", weather) # function call weather
backgroundhome.tag_bind(buttonTXT, "<Button-1>",weather)

'''
# ping
def ping(event):
    print("ping")
buttonBG = backgroundhome.create_rectangle(700-10, 235+400-50, 800-10, 275+400-50, fill= "#94d5d6", outline="grey60")
buttonTXT = backgroundhome.create_text(750-10, 257+400-50, text="PING", font = "bold")
backgroundhome.tag_bind(buttonBG, "<Button-1>", ping) # function call ping
backgroundhome.tag_bind(buttonTXT, "<Button-1>",ping)
'''
# calculator

def claculator(event):
    os.system('gnome-calculator')
buttonBG = backgroundhome.create_rectangle(700-10+200-20-5, 400,200+800-10-20+5, 440, fill= "#94d5d6", outline="grey60")
buttonTXT = backgroundhome.create_text(750-10+200-20, 22+400, text="CALCULATOR", font = "bold")
backgroundhome.tag_bind(buttonBG, "<Button-1>", claculator) # function call calculator
backgroundhome.tag_bind(buttonTXT, "<Button-1>",claculator)


'''
#photo
picLbl = PhotoImage(file = "C:\\Users\\jolly\\Desktop\\PROJECT LEGCY\\background\\label\\box.png")

#label
lblCpu = Label(leftFrame,image = picLbl)
lblCpu.pack()
'''
#
'''
picLbl = PhotoImage(file = "C:\\Users\\jolly\\Desktop\\PROJECT LEGCY\\background\\label\\box.png")
CpicLbl = Canvas(leftFrame,width = 287, height = 89,bg = "white")
CpicLbl.pack(side = LEFT)

lblCpu = Label(CpicLbl,text = "CPU",image = picLbl)
lblCpu.pack()

'''
dside = 30
lstart = 20

fn = "castellar"
fs = 13
b = "bold"

ytd = 15

# internet speed meter


def u_speed():
    up = str(jku.current_upload()) + "KB/s"
    backgroundhome.itemconfig(up_speed, text = up)
    backgroundhome.after(250,u_speed)

def r_speed():
    down = str(jkr.current_download()) + "KB/s"
    backgroundhome.itemconfig(rs, text = down)
    backgroundhome.after(200,r_speed)
right = 40
backgroundhome.create_line(lstart, 50, 380+right, 50, fill="white")  # upper line
backgroundhome.create_line(lstart, 50, 20, 50 + dside, fill="white")  # left side
backgroundhome.create_line(380+right, 50, 380+ right, 50 + dside, fill="white")  # right side
backgroundhome.create_line(lstart, 80, 380+ right, 80, fill="white")  # down side
backgroundhome.create_line(270, 50, 270, 50 + dside, fill="white")  # up
backgroundhome.create_line(346, 50, 346, 50 + dside, fill="white")  # mid line

backgroundhome.create_text(295, 35, text="UP", anchor=N, fill="white")  # up text
backgroundhome.create_text(370, 35, text="DOWN", anchor=N, fill="white")  # down text

#backgroundhome.create_text(295, 60, text="N/A", anchor=N, fill="white")  # up value
#backgroundhome.create_text(350, 60, text="N/A", anchor=N, fill="white")  # down value

ism = backgroundhome.create_text(25, 65, anchor=W, fill="WHITE", text="INTERNET SPEED METER",
                                 font=("castellar", 13, "bold"))
# internet upload update

up_speed = backgroundhome.create_text(324, 60, text="N/A", anchor=N, fill="white")  # up value
u_speed()

#internet download update
rs = backgroundhome.create_text(389, 60, text="N/A", anchor=N, fill="white")  # down value

# Network receiver monitor

r_speed()


# battery

def perbattery():
    battery = psutil.sensors_battery()
    # plugged = battery.power_plugged
    percent = str(battery.percent)
    percentage = percent.split('.')[0]
    backgroundhome.itemconfig(bvalue, text=percentage)
    backgroundhome.after(200, perbattery)
    # if plugged==False: plugged="Not Plugged In"


# else: plugged="Plugged In"
# print(percent+'% | '+plugged)


'''
picBatteryLbl = PhotoImage(file = "C:\\Users\\jolly\\Desktop\\PROJECT LEGCY\\background\\label\\png\\battery.png")
lblbattery = Label(leftFrame,text = "BATTERY", width = 250,height = 40, borderwidth = 2, highlightcolor = "green", image = picBatteryLbl)
cmb = backgroundhome.create_window(20,615, anchor =NW, window = lblbattery)
'''
'''
heartPic = PhotoImage(file = "C:\\Users\\jolly\\Desktop\\PROJECT LEGCY\\background\\New folder\\heart.gif")
lblHeart = Label(leftFrame,width = 250, height = 400,image = heartPic)
backgroundhome.create_window(100,100, anchor = CENTER,window = lblHeart)
'''
backgroundhome.create_text(lstart + 5, 615 + ytd, text="BATTERY", fill="white", font=(fn, fs, b),
                           anchor=W)  # battery text
backgroundhome.create_line(lstart, 615, lstart + 150 + 30, 615, fill="white")  # up line
backgroundhome.create_line(lstart, 615, lstart, 615 + dside, fill="white")  # left side
backgroundhome.create_line(lstart + 150 + 30, 615, lstart + 150 + 30, 615 + dside, fill="white")  # right side
backgroundhome.create_line(lstart, 615 + dside, lstart + 150 + 30, 615 + dside, fill="white")  # down side
xb = 120
backgroundhome.create_line(xb, 615, xb, 615 + dside, fill="white")  # percentage line
backgroundhome.create_text(185, 630, fill="white", font="bold", text="%")

bvalue = backgroundhome.create_text(155, 630, fill="white", font="bold")  # percentage value

perbattery()


# Time

# Time

def tick():
    current_time = time.strftime('%H:%M:%S')
    backgroundhome.itemconfig(lblClock, text=current_time)
    backgroundhome.after(200, tick)


# cpu and memory
'''
picLbl = PhotoImage(file = "C:\\Users\\jolly\\Desktop\\PROJECT LEGCY\\background\\label\\CM1.png")
cmc = backgroundhome.create_text(135,500,anchor = W,text = "CPU", fill = "white" )
lblCpu = Label(leftFrame, text = "CPU", width = 311, height = 95,image = picLbl)
cm = backgroundhome.create_window(20,700,anchor = NW, window = lblCpu )
'''

backgroundhome.create_text(lstart + 5, 700, text="CPU", fill="white", font=(fn, fs, b), anchor=W)  # text CPU
backgroundhome.create_text(lstart + 5, 730, text="MEMORY", fill="white", font=(fn, fs, b), anchor=W)  # text MEMORY
backgroundhome.create_line(lstart, 685, lstart + 150 + 30, 685, fill="white")  # up line
backgroundhome.create_line(lstart, 685, lstart, 685 + dside + dside, fill="white")  # left line
backgroundhome.create_line(lstart + 150 + 30, 685, lstart + 150 + 30, 685 + dside + dside, fill="white")  # right line
backgroundhome.create_line(lstart, 685 + dside + dside, lstart + 150 + 30, 685 + dside + dside,
                           fill="white")  # down line
backgroundhome.create_line(lstart, 685 + dside, lstart + 150 + 30, 685 + dside, fill="white")  # mide right line
backgroundhome.create_text(185, 700, fill="white", anchor=CENTER, font="bold", text="%")  # cpu percent symbol
backgroundhome.create_text(185, 730, fill="white", anchor=CENTER, font="bold", text="%")

backgroundhome.create_line(120, 685, 120, 685 + 60, fill="white")  # midline


def cpu_percent_value():
    val_cpu_percent = psutil.cpu_percent()
    backgroundhome.itemconfig(display_cpu_percent, text=val_cpu_percent)
    backgroundhome.after(1000, cpu_percent_value)


display_cpu_percent = backgroundhome.create_text(145, 700, fill="white", anchor=CENTER, font="bold")
cpu_percent_value()


def memory_percent_value():
    val_memory_percent = psutil.virtual_memory().percent
    backgroundhome.itemconfig(display_memory_percent, text=val_memory_percent)
    backgroundhome.after(1000, memory_percent_value)


display_memory_percent = backgroundhome.create_text(145, 730, fill="white", anchor=CENTER, font="bold")
memory_percent_value()

'''
time
'''
backgroundhome.create_text(lstart + 5, 300, text="TIME", fill="white", font=(fn, fs, b), anchor=W)  # text TIME
backgroundhome.create_line(lstart, 285, lstart + 150, 285, fill="white")  # up line
backgroundhome.create_line(lstart, 285 + 30, lstart + 150, 285 + 30, fill="white")  # down line
backgroundhome.create_line(lstart, 285, lstart, 285 + 30, fill="white")  # left line
backgroundhome.create_line(lstart + 150, 285, lstart + 150, 285 + 30, fill="white")  # right line
backgroundhome.create_line(lstart + 60, 285, lstart + 60, 285 + 30, fill="white")  # right line

lblClock = backgroundhome.create_text(125, 300, fill="white", font=(fn, fs, b))
tick()


def jarvis_color():
    # red = 0
    # blue = 0
    # green = 0

    # while True:
    '''
    haas = "#"
    one = "f"
    two = "f"
    three = "f"
    four = "f"
    five = "a"
    six = "a"
    color_string = (haas+one+two+three+four+five+six)
    '''
    color_string = '#' + ("%06x" % random.randint(0, 0xFFFFFF))
    backgroundhome.itemconfig(text_jarvis, fill=color_string)
    backgroundhome.after(200, jarvis_color)


text_jarvis = backgroundhome.create_text(500, 300 + 100, fill="white", font=(fn, 34, b), text="JARVIS")
jarvis_color()

'''
round_gif = ImageTk.PhotoImage(Image.open("C:\\Users\\jolly\\Desktop\\PROJECT LEGCY\\background\\gif\\rc.gif"))
backgroundhome.create_image(500,600,anchor = NW, image=round_gif)
'''

leftFrame.pack(side=LEFT)

# Frames   RIGHT

rightFrame = Frame(root, width=520, height=820, background="red")

rbg = Canvas(rightFrame, width=530, height=820)
rimage = ImageTk.PhotoImage(Image.open(rightImage))
rbg.create_image(0, 0, anchor=NW, image=rimage)
rbg.pack(fill=BOTH)

'''
CONVERSATION
'''
rbg.create_text(90, 30, text="CONVERSATION", fill="white", font=(fn, 30, b), anchor=W)  # conversion text
rbg.create_line(80, 10, 470, 10, fill="white")  # up line
rbg.create_line(80, 48, 470, 48, fill="white")  # down line
rbg.create_line(80, 10, 80, 48, fill="white")  # left side line
rbg.create_line(470, 10, 470, 48, fill="white")  # right side line

quote= """HAMLET: To be, or not to be--that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune
Or to take arms against a sea of troubles
And by opposing end them. To die, to sleep--
No more--and by a sleep to say we end
The heartache, and the thousand natural shocks
That flesh is heir to. 'Tis a consummation
Devoutly to be wished."""

rbg.create_text(250,200,fill = "blue", text = quote, font=(fn, fs))

'''
dummy button

def create_label_jarvis():
    Ylabel = 80
    label = Label(rightFrame,text = "1",bg = "white")
    label.configure()
    rbg.create_window(40,Ylabel,anchor = W,window = label)
'''


def Move_Label_down():
    AV = 10
    Ylabel = 80
    Ylabel = Ylabel + AV
    # 2
    # Xlabel = 40
    '''
    Xlabel = Xlabel + AV
    '''
    label = Label(rightFrame, text="1", bg="white")
    label.configure()
    rbg.create_window(40, Ylabel, anchor=W, window=label)

'''
button1 = Button(rightFrame, text="Create Label jarvis", command=Move_Label_down)
button1.bind('<Button-1>', Move_Label_down)

button1.configure()
button1_window = rbg.create_window(10, 780, anchor=NW, window=button1)

button2 = Button(rightFrame, text="Create Label user")
button2.configure()
button2_window = rbg.create_window(400, 780, anchor=NW, window=button2)
'''
# To do list

rbg.create_line(0,580,530,580, fill = "white")
rbg.create_text(150,605, text = "TO DO....",fill = "white",font=(fn, 20, b))

# to do entry box
def on_entry_click(event):
    """function that gets called whenever entry is clicked"""
    if e1.get() == 'Write Memo...':
       e1.delete(0, "end") # delete all the text in the entry
       e1.insert(0, '') #Insert blank for user input
       e1.config(fg = 'black')
def on_focusout(event):
    if e1.get() == '':
        e1.insert(0, 'Write Memo...')
        e1.config(fg = 'grey')
e1 = Entry(rbg, justify = CENTER)
e1.pack()
#e1.place(width=150,height=100)
e1.insert(0, "Write Memo...")
e1.bind('<FocusIn>', on_entry_click)
e1.bind('<FocusOut>', on_focusout)
e1.configure()
rbg.create_window(400, 600, window=e1)
rightFrame.pack()

# Window size
#root.geometry("1530x820+0+0")

root.configure(width = screen_width, height = screen_height)
root.maxsize()
root.resizable(width=False, height=False)

root.mainloop()