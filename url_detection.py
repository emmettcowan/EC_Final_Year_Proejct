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


class detectionThread(Thread):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    active_window = ""
    window = ""
    startTime = time.time()
    firstRun = True
    user = ""
    thread_running = False

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
        mycol = mydb[self.user]
        mycol.insert_one(activityData)

    user = "emmett"#remove later

    def run(self):
        self.thread_running = True

        while self.thread_running:
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
                            data = {'user': self.user, 'App': self.window, 'Date & time': str(Timestamp), 'Total time': int(TimeSpent)*-1}
                            self.dbPost(data)
                            self.startTime = time.time()

                        self.firstRun = False
                        self.window = self.active_window
                        print(self.window)
        print("Monitor Stoped")

    def stop(self):
        self.thread_running = False
                

        
class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.thread = None

        tk.Label(self, text='Monitor 0.5')\
            .grid(row=0, column=0)
        tk.Button(self, text="Start", command=self.launch_thread)\
            .grid(row=1, column=0)
        tk.Button(self, text="Stop", command=self.stop_thread)\
            .grid(row=2, column=0)

    def launch_thread(self):
        if self.thread:
            print("Monitor already Started")
        else:
            print("Monitor Started")
            self.thread = detectionThread()
            self.thread.start()


    def stop_thread(self):
        if self.thread:
            self.thread.stop()
            self.thread = None
        else:
            print("Nothing to Stop")

if __name__ == '__main__':
    win = Window()
    win.mainloop()

                
