import tkinter as tk
import time


def tick():
    time_now = time.strftime('%H:%M:%S')
    time_label.config(text=time_now)
    time_label.after(1000, tick)


root = tk.Tk()
time_label = tk.Label(root, font=('times', 48, 'bold'), bg='#3C3F41', fg='#bbbbbb')
time_label.pack()
tick()


if __name__ == '__main__':
    root.mainloop()
