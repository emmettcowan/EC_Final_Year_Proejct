import tkinter as tk

window= tk.Tk()

canvas = tk.Canvas(window, width = 400, height = 300,  relief = 'raised')
canvas.pack()

label1 = tk.Label(window, text='Monitor Login')
label1.config(font=('helvetica', 14))
canvas.create_window(200, 25, window=label1)

label2 = tk.Label(window, text='Enter Username:')
label2.config(font=('helvetica', 10))
canvas.create_window(200, 100, window=label2)

entry1 = tk.Entry (window) 
canvas.create_window(200, 140, window=entry1)

def main_window():
    label1 = tk.Label(window, text='Monitor main page')
    label1.config(font=('helvetica', 14))
    canvas.create_window(200, 25, window=label1)
    
    button2 = tk.Button(window, text='start')
    button2.config(font=('helvetica',14))
    canvas.create_window(200,300, window=button2)

def login ():
    x1 = entry1.get()
    print(x1)
    canvas.pack_forget()
    main_window()
    
button1 = tk.Button(text='Login', command=login, bg='green', fg='white', font=('helvetica', 9, 'bold'))
canvas.create_window(200, 180, window=button1)

window.mainloop()

