#########################################################
#   ---              ***MONITOR***                ---   #
#         *                                  *          #
#   ---  ***  ---   By Emmett Cowan    ---  ***   ---   #
#         *                                  *          #
#   ---                  V0.4                     ---   #
#########################################################


import time
import win32gui     
import uiautomation as auto
import json
import datetime as dt

active_window = ""
window = ""
startTime = time.time()
firstRun = True

def activeWindow():
    activeWindowName = None
    window = win32gui.GetForegroundWindow()
    activeWindowName = win32gui.GetWindowText(window)
    return activeWindowName


def chromeUrl():
    _activeWindowName = None
    window = win32gui.GetForegroundWindow()
    chromeControl = auto.ControlFromHandle(window)
    chromeWindow = chromeControl.EditControl()
    return '' + chromeWindow.GetValuePattern().Value

def urlStrip(url):
    string_list = url.split('/')
    return string_list[0]
    

while True:
    
    active_window = activeWindow()      #get current windows app

    if 'Google Chrome' in active_window:     #get url if in chrome app 
        url = chromeUrl()
        active_window = urlStrip(url)

    if active_window != '':                
        if window != active_window:
            if active_window != '':
                
                if not firstRun:
                    endTime = time.time()
                    Timestamp = dt.datetime.fromtimestamp(startTime)
                    TimeSpent = startTime - endTime
                    data = {'App': window, 'Date & time': str(Timestamp), 'Total time': int(TimeSpent)*-1}
                    with open('log.json', 'a+') as f:
                        json.dump(data, f, indent=2)
                    startTime = time.time()

                firstRun = False
                window = active_window
                print(window)
                


                
