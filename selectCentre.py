from tkinter import *
from PIL import Image, ImageTk

def canvasCallback(e):
    print('Clicked at', e.x, e.y)

def gotchu():
    print('Position confirmed.')

def selectCentre(imFile):
    window = Tk()

    cs = Canvas(window, width=500, height=500)
    cs.pack()

    imFile = ImageTk.PhotoImage(imFile)
    image = cs.create_image(500, 0, anchor=NE, image=imFile)
    cs.bind("<Button-1>", canvasCallback)

    confirm = Button(window, text="Confirm", command=gotchu)
    confirm.pack()

    window.mainloop()