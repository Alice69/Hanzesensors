from tkinter import *
import time, random

# Create Canvas
root = Tk()
canvas = Canvas(root, width=640, height=480, bg='#000')
canvas.pack()

rect = canvas.create_rectangle(0,0,100,100, fill="#FFF")


def GUI():
    x = random.randrange(640)
    y = random.randrange(480)
    canvas.coords(rect, x, y, x + 100, y + 100)

while(1):
    GUI()
    root.update_idletasks()
    root.update()
    time.sleep(0.025)