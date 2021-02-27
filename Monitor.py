#########################################################
#   ---              ***MONITOR***                ---   #
#         *                                  *          #
#   ---  ***  ---   By Emmett Cowan    ---  ***   ---   #
#         *                                  *          #
#   ---                  V0.7                     ---   #
#########################################################


import time                     # timestamps
import win32gui                 # active window info
import uiautomation as auto     # url info
import json                     # loggin
import datetime as dt           # timestaps
import pymongo                  # mongodb
from threading import Thread    # gui threading
import tkinter as tk            # gui
from urlDetection import Url    # get url from chrome window        
import pythoncom                # initizlise com ports on threads


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

    def urlStrip(self, url):                       # strip url down 
        string_list = url.split('/')
        return string_list[0]

    def dbPost(self, activityData):             # post  data to mongo
        mydb = self.myclient["Monitor"]
        mycol = mydb[user]
        print(mycol)                        #  swap these comments to
        #mycol.insert_one(activityData)       #  post to db or for testing


    def run(self):                  # thread for main applicaion code
        self.threadRunning = True

        while self.threadRunning:
            self.active_window = self.activeWindow()      #get current windows app

            if 'Google Chrome' in self.active_window:     #get url if in chrome app 
                pythoncom.CoInitialize ()
                u = Url()                       
                urlpre = u.chromeUrl()
                self.active_window = self.urlStrip(urlpre)

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
 
def launchThread():        # gui start thread
    global thread
    if thread:
        print("Monitor already Started")
    else:
        print("Monitor Started")
        thread = detectionThread()
        thread.start()


def stopThread():       # gui stop thread
    global thread
    if thread:
        thread.stopThread()
        thread = None
    else:
        print("Nothing to stop")


def login():            # gui login 
    global user
    x1 = usernameEntry.get()
    user = x1
    print(x1)
    

window= tk.Tk()         #create tkinr object for gui
window.title("Moniter")

canvas = tk.Canvas(window, width = 500, height = 300)       # create canvas 
canvas.pack()                                                                   # set layout and fill widgets

headLable = tk.Label(window, text='Monitor V0.6')
headLable.config(font=('Arial', 15))
canvas.create_window(250, 25, window=headLable)

usernameLable = tk.Label(window, text='Enter Username:')
usernameLable.config(font=('Arial', 12))
canvas.create_window(250, 100, window=usernameLable)

usernameEntry = tk.Entry (window) 
canvas.create_window(250, 140, window=usernameEntry)

loginButton = tk.Button(text='Login', command=login, bg='black', fg='white', font=('Arial', 12, 'bold'))
canvas.create_window(250, 180, window=loginButton)

startButton = tk.Button(window, command=launchThread, text='start')
startButton.config(font=('Arial',16))
canvas.create_window(200,250, window=startButton)

stopButton = tk.Button(window, command=stopThread, text='stop')
stopButton.config(font=('Arial',16))
canvas.create_window(300,250, window=stopButton)

window.mainloop()

#----------------------------------------------------------------------------------------#               
