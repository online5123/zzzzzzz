from tkinter import *

def draw_window():
    root = Tk()
    label = Label(root, text='Hello World!')
    label.pack()

    root.mainloop()

if __name__ == '__main__':
    draw_window()