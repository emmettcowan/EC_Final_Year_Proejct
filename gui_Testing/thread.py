import time
import tkinter as tk
from threading import Thread

class MyThread(Thread):
    thread_running = False

    def run(self):
        k = 0
        self.thread_running = True
        while self.thread_running:
            print(k)
            k +=1
            time.sleep(1)
        print("thread ended")

    def stop(self):
        self.thread_running = False


class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.thread = None

        tk.Button(self, text="launch thread", command=self.launch_thread)\
            .grid(row=1, column=0)
        tk.Button(self, text="stop thread", command=self.stop_thread)\
            .grid(row=2, column=0)

    def launch_thread(self):
        if self.thread:
            print("thread already launched")
        else:
            print("thread launched")
            self.thread = MyThread()
            self.thread.start()


    def stop_thread(self):
        if self.thread:
            self.thread.stop()
            self.thread = None
        else:
            print("no thread running")

if __name__ == '__main__':
    win = Window()
    win.mainloop()