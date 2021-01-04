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

        canvas = tk.Canvas(self, width = 400, height = 300,  relief = 'raised')
        canvas.pack()

        label1 = tk.Label(self, text='Monitor V0.5')
        label1.config(font=('helvetica', 14))
        canvas.create_window(200, 25, window=label1)

        label2 = tk.Label(self, text='Enter Username:')
        label2.config(font=('helvetica', 10))
        canvas.create_window(200, 100, window=label2)

        entry1 = tk.Entry (self) 
        canvas.create_window(200, 140, window=entry1)

        button1 = tk.Button(text='Login', command=self.login, bg='green', fg='white', font=('helvetica', 9, 'bold'))
        canvas.create_window(200, 180, window=button1)


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

    def login (self):
        x1 = self.entry1.get()
        print(x1)
        self.main_window()

    def stop_thread(self):
        if self.thread:
            self.thread.stop()
            self.thread = None
        else:
            print("no thread running")

if __name__ == '__main__':
    win = Window()
    win.mainloop()