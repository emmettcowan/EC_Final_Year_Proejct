#########################################################
#   ---              ***MONITOR***                ---   #
#         *                                  *          #
#   ---  ***  ---   By Emmett Cowan    ---  ***   ---   #
#         *                                  *          #
#   ---                  V0.3                     ---   #
#########################################################


import time
import win32gui     
import uiautomation as auto


def activeWindow():
    activeWindowName = None
    window = win32gui.GetForegroundWindow()
    activeWindowName = win32gui.GetWindowText(window)
    return activeWindowName


def chromeUrl():
    _activeWindowName = None
    window = win32gui.GetForegroundWindow()
    chromeControl = auto.ControlFromHandle(window)
    edit = chromeControl.EditControl()
    return '' + edit.GetValuePattern().Value

def urlStrip(url):
    string_list = url.split('/')
    return string_list[0]
    
    
active_window = ""
window = ""

while True:
    import json

    x = {
    "name": "John",
    "age": 30,
    "married": True,
    "divorced": False,
    "children": ("Ann","Billy"),
    "pets": None,
    "cars": [
        {"model": "BMW 230", "mpg": 27.5},
        {"model": "Ford Edge", "mpg": 24.1}
    ]
    }

    print(json.dumps(x))
    
    active_window = activeWindow()      #get current windows app

    if 'Google Chrome' in active_window:     #get url if in chrome app 
        url = chromeUrl()
        active_window = urlStrip(url)

    if active_window != '':                
        if window != active_window:
            if active_window != '':
                print(active_window)
                window = active_window
