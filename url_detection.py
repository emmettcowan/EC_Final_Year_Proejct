import time
from os import system
import json
import datetime
import sys
import win32gui
import uiautomation as auto


def get_active_window():
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)
    return _active_window_name


def get_chrome_url():
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        return 'https://' + edit.GetValuePattern().Value
    return _active_window_name


active_window = ""


while True:
    active_window = get_active_window()
    if 'Google Chrome' in active_window:
        url = get_chrome_url()
        print(url)
        time.sleep(1)
    else:
        print(active_window)
        time.sleep(1)
