# This python script returns the url from chrome when it is the slected forground window

import uiautomation as auto     # url info
import win32gui                 # active window info
import time



class Url():

    active_window = ""
    window = ""
   

    def chromeUrl(self):                            # get url from chrome
        window = win32gui.GetForegroundWindow()                 #  Refrence :
        chromeControl = auto.ControlFromHandle(window)          #  https://stackoverflow.com/questions/59595763/get-active-chrome-url-in-python
        chromeWindow = chromeControl.EditControl()              #  "Get Active Chrome URL in Python"
        try:
            return '' + chromeWindow.GetValuePattern().Value
        except:
            return ''

