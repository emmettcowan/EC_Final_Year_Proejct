#########################################################
#   ---              ***MONITOR***                ---   #
#         *                                  *          #
#   ---  ***  ---   By Emmett Cowan    ---  ***   ---   #
#         *                                  *          #
#   ---                  V0.6                     ---   #
#########################################################


import time
import win32gui     
import uiautomation as auto
import json
import datetime as dt
import pymongo
from threading import Thread
import tkinter as tk


user = ""
thread = None

class detectionThread(Thread):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    active_window = ""
    window = ""
    startTime = time.time()
    firstRun = True
    threadRunning = False
    #global user

    def activeWindow(self):
        self.activeWindowName = None
        self.activeWindowName = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        return self.activeWindowName


    def chromeUrl(self):
        activeWindowName = None
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        chromeWindow = chromeControl.EditControl()
        return '' + chromeWindow.GetValuePattern().Value

    def urlStrip(self, url):
        string_list = url.split('/')
        return string_list[0]

    def dbPost(self, activityData):
        mydb = self.myclient["Monitor"]
        mycol = mydb[user]
        print(mycol)
        #mycol.insert_one(activityData)

    #user = "andy"#remove when user input name

    def run(self):
        self.threadRunning = True

        while self.threadRunning:
            self.active_window = self.activeWindow()      #get current windows app
            # if 'Google Chrome' in self.active_window:     #get url if in chrome app 
            #     url = self.chromeUrl()
            #     self.active_window = self.urlStrip(url)

            if self.active_window != '':                
                if self.window != self.active_window:
                    if self.active_window != '':
                        
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
        print("Monitor stopThreaded")

    def stopThread(self):
        self.threadRunning = False
                

   
def launch_thread():
    global thread
    if thread:
        print("Monitor already Started")
    else:
        print("Monitor Started")
        thread = detectionThread()
        thread.start()


def stopThread_thread():
    global thread
    if thread:
        thread.stopThread()
        thread = None
    else:
        print("Nothing to stopThread")


def login():
    global user
    x1 = entry1.get()
    user = x1
    print(x1)
    

window= tk.Tk()

canvas = tk.Canvas(window, width = 400, height = 300,  relief = 'raised')
canvas.pack()

label1 = tk.Label(window, text='Monitor V0.5')
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

        
# class Window(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#         self.thread = None

#         tk.Label(self, text='Monitor 0.5')\
#             .grid(row=0, column=0)
#         tk.Button(self, text="Start", command=self.launch_thread)\
#             .grid(row=1, column=0)
#         tk.Button(self, text="stopThread", command=self.stopThread_thread)\
#             .grid(row=2, column=0)

#     def launch_thread(self):
#         if self.thread:
#             print("Monitor already Started")
#         else:
#             print("Monitor Started")
#             self.thread = detectionThread()
#             self.thread.start()


#     def stopThread_thread(self):
#         if self.thread:
#             self.thread.stopThread()
#             self.thread = None
#         else:
#             print("Nothing to stopThread")

# if __name__ == '__main__':
#     win = Window()
#     win.mainloop()

                
