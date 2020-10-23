import time
import win32gui
import uiautomation as auto


def get_active_window():
    active_window_name = None
    window = win32gui.GetForegroundWindow()
    active_window_name = win32gui.GetWindowText(window)
    return active_window_name


def get_chrome_url():
    _active_window_name = None
    window = win32gui.GetForegroundWindow()
    chromeControl = auto.ControlFromHandle(window)
    edit = chromeControl.EditControl()
    return '' + edit.GetValuePattern().Value

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
