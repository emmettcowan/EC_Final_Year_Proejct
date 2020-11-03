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

def url_to_name(url):
    string_list = url.split('/')
    return string_list[0]


active_window = ""
window = ""

while True:
    active_window = get_active_window()

    if 'Google Chrome' in active_window:
        url = get_chrome_url()
        active_window = url;
        time.sleep(1)


    if window != active_window:
        print(active_window)
        window = active_window
