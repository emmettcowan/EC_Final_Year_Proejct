#########################################################
#   ---              ***MONITOR***                ---   #
#         *                                  *          #
#   ---  ***  ---   By Emmett Cowan    ---  ***   ---   #
#         *                                  *          #
#   ---                  V1                       ---   #
#########################################################


import time                     # timestamps
import win32gui                 # active window info
import uiautomation as auto     # url info
import datetime as dt           # timestaps
import pymongo                  # mongodb
from threading import Thread    # gui threading
import tkinter as tk            # gui
from urlDetection import Url    # get url from chrome window        
import pythoncom                # initizlise com ports on threads
import hashlib                  # login verification encryption


user = ""
thread = None

class detectionThread(Thread):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')    # mongodb connection
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
        #print(activityData)                        #  swap these comments to
        mycol.insert_one(activityData)       #  post to db or for testing


    def run(self):                  # thread for main applicaion code
        self.threadRunning = True
        self.startTime = time.time()
        while self.threadRunning:
            self.active_window = self.activeWindow()      #get current windows app

            if 'Google Chrome' in self.active_window:     #get url if in chrome app 
                pythoncom.CoInitialize ()                   # initizlie Com ports on thread 
                urlDetector = Url()                       
                urlpre = urlDetector.chromeUrl()
                self.active_window = self.urlStrip(urlpre)

            if self.active_window != '':                    #  checking & removing
                if self.window != self.active_window:       #  empty 
                    if self.active_window != '':            #  return values
                        
                        if not self.firstRun:
                            endTime = time.time()
                            Timestamp = dt.datetime.fromtimestamp(self.startTime)
                            TimeSpent = self.startTime - endTime
                            data = {'user': user, 'App': self.window, 'Date_time': str(Timestamp),'Start_time': self.startTime, 'End_Time': endTime, 'Total_time': int(TimeSpent)*-1}
                            self.dbPost(data)
                            self.startTime = time.time()

                        self.firstRun = False
                        self.window = self.active_window
                        print(self.window) # for testing in developemtn
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

def verifiyPass(password, hash, salt):      #  verifiy the inputed password with the Hashed value 
    dbPass = hashlib.pbkdf2_hmac('sha256', bytes(password, encoding='utf-8'), bytes(salt, encoding='utf-8'), 25000, dklen=512)
    if(dbPass.hex() == hash):
        return True
    else:
        return False



def login():            # gui login 
    #connect to the user DB
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient["users"]
    mycol = mydb["userInfo"]
    #set up variables
    global user
    userObj = ""
    user = usernameEntry.get()
    password = passEntry.get()
    salt = ""
    #queery the DB and find the user
    query = {"username": user}    
    for x in mycol.find(query):
        userObj = x
    #error check
    if(userObj == ""):
        loginLable['text'] = 'User Not found'
    else:
        salt = userObj['salt']
        hash = userObj['hash']
        if(verifiyPass(password, hash, salt)):
            loginLable['text'] = 'Login Success'
            # show the buttons once the login is successful
            startButton = tk.Button(window, command=launchThread, bg='SpringGreen3', fg='white', text='start')
            startButton.config(font=('Arial',16))
            canvas.create_window(200,300, window=startButton)

            stopButton = tk.Button(window, command=stopThread, bg='Firebrick1', fg='white', text='stop')
            stopButton.config(font=('Arial',16))
            canvas.create_window(300,300, window=stopButton)
        else:
            loginLable['text'] = 'Login Failed'

window= tk.Tk()         #create tkinr object for gui
window.title("Moniter")

canvas = tk.Canvas(window, width = 500, height = 350, bg = "RoyalBlue1")       # create canvas 
canvas.pack()                                                                   # set layout and fill widgets

headLable = tk.Label(window, text='Monitor V0.7',  bg = "RoyalBlue1")
headLable.config(font=('Arial', 20))
canvas.create_window(250, 25, window=headLable)

usernameLable = tk.Label(window, text='Enter Username:',  bg = "RoyalBlue1")
usernameLable.config(font=('Arial', 12))
canvas.create_window(150, 100, window=usernameLable)

usernameEntry = tk.Entry (window) 
canvas.create_window(300, 100, window=usernameEntry)

passLable = tk.Label(window, text='Enter password:',  bg = "RoyalBlue1")
passLable.config(font=('Arial', 12))
canvas.create_window(150, 150, window=passLable)

passEntry = tk.Entry (window) 
canvas.create_window(300, 150, window=passEntry)

loginButton = tk.Button(text='Login', command=login, width=15, bg='ghost white', fg='Black', font=('Arial', 12, 'bold'))
canvas.create_window(250, 200, window=loginButton)

loginLable = tk.Label(window, text='',  bg = "RoyalBlue1")
loginLable.config(font=('Arial', 12))
canvas.create_window(150, 250, window=loginLable)

window.mainloop()

#----------------------------------------------------------------------------------------#               
