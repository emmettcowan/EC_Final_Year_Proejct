#########################################################
#   ---              ***MONITOR***                ---   #
#         *                                  *          #
#   ---  ***  ---   By Emmett Cowan    ---  ***   ---   #
#         *                                  *          #
#   ---                  V0.6                     ---   #
#########################################################


import time                     # timestamps
import win32gui                 # active window info
import uiautomation as auto     # url infor
import json                     # loggin
import datetime as dt           # timestaps
import pymongo                  # mongodb
from threading import Thread    # gui threading
import tkinter as tk            # gui


user = ""
thread = None

class detectionThread(Thread):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")    # mongodb connection
    active_window = ""
    window = ""
    startTime = time.time()
    firstRun = True
    threadRunning = False

    def activeWindow(self):             # get the name of the forground window
        self.activeWindowName = None
        self.activeWindowName = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        return self.activeWindowName


    def chromeUrl(self):                            # get url from chrome
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        chromeWindow = chromeControl.EditControl()
        return '' + chromeWindow.GetValuePattern().Value

    def urlStrip(self, url):                       # strip url down 
        string_list = url.split('/')
        return string_list[0]

    def dbPost(self, activityData):             # post  data to mongo
        mydb = self.myclient["Monitor"]
        mycol = mydb[user]
        print(mycol)                        #swap these comments to post to db or for testing
        #mycol.insert_one(activityData)


    def run(self):                  # thread for main applicaion code
        self.threadRunning = True

        while self.threadRunning:
            self.active_window = self.activeWindow()      #get current windows app

            # if 'Google Chrome' in self.active_window:     #get url if in chrome app 
            #     url = self.chromeUrl()                       #problem with threading
            #     self.active_window = self.urlStrip(url)

            if self.active_window != '':                    #  checking & removing
                if self.window != self.active_window:       #  empty 
                    if self.active_window != '':            #  return values
                        
                        if not self.firstRun:
                            endTime = time.time()
                            Timestamp = dt.datetime.fromtimestamp(self.startTime)
                            TimeSpent = self.startTime - endTime
                            data = {'user': user, 'App': self.window, 'Date & time': str(Timestamp), 'Total time': int(TimeSpent)*-1}
                            self.dbPost(data)
                            self.startTime = time.time()

                        self.firstRun = False
                        self.window = self.active_window
                        print(self.window)
        print("Monitor stoped")

    def stopThread(self):
        self.threadRunning = False

                
#---------------------------------------- GUI CODE --------------------------------------#
 
def launch_thread():        # gui start thread
    global thread
    if thread:
        print("Monitor already Started")
    else:
        print("Monitor Started")
        thread = detectionThread()
        thread.start()


def stopThread_thread():       # gui stop thread
    global thread
    if thread:
        thread.stopThread()
        thread = None
    else:
        print("Nothing to stop")


def login():            # gui login 
    global user
    x1 = entry1.get()
    user = x1
    print(x1)
    

window= tk.Tk()         #create tkinr object for gui

canvas = tk.Canvas(window, width = 400, height = 300,  relief = 'raised')       # create canvas 
canvas.pack()                                                                   # set layout and fill widgets

label1 = tk.Label(window, text='Monitor V0.6')
label1.config(font=('helvetica', 14))
canvas.create_window(200, 25, window=label1)

label2 = tk.Label(window, text='Enter Username:')
label2.config(font=('helvetica', 10))
canvas.create_window(200, 100, window=label2)

entry1 = tk.Entry (window) 
canvas.create_window(200, 140, window=entry1)

button1 = tk.Button(text='Login', command=login, bg='green', fg='white', font=('helvetica', 9, 'bold'))
canvas.create_window(200, 180, window=button1)

button2 = tk.Button(window, command=launch_thread, text='start')
button2.config(font=('helvetica',14))
canvas.create_window(150,250, window=button2)

button3 = tk.Button(window, command=stopThread_thread, text='stop')
button3.config(font=('helvetica',14))
canvas.create_window(250,250, window=button3)

window.mainloop()

#----------------------------------------------------------------------------------------#               
