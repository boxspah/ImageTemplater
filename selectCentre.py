from tkinter import *
from PIL import Image, ImageTk

def canvasCallback(e):
    print('Clicked at', e.x, e.y)

def gotchu():
    print('Position confirmed.')

def selectCentre(imFile):
    window = Tk()

    cs = Canvas(window, width=800, height=800)
    cs.pack()

    imFile.thumbnail((800, 800))
    imFile = ImageTk.PhotoImage(imFile)
    image = cs.create_image(400, 400, anchor=CENTER, image=imFile)
    cs.bind("<Button-1>", canvasCallback)

    confirm = Button(window, text="Confirm", command=gotchu)
    confirm.pack()

    window.mainloop()