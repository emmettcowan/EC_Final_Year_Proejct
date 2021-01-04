import tkinter as tk


def main_window():

    button2 = tk.Button(window, text='start')
    button2.config(font=('helvetica',14))
    canvas.create_window(150,250, window=button2)

    button3 = tk.Button(window, text='stop')
    button3.config(font=('helvetica',14))
    canvas.create_window(250,250, window=button3)


def login ():
    x1 = entry1.get()
    print(x1)
    main_window()
    

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


window.mainloop()

