from tkinter import *
from PIL import Image, ImageTk

def canvasCallback(e):
    print('Clicked at', e.x, e.y)

def gotchu():
    print('Position confirmed.')

def selectCentre(imFile):
    window = Tk()

    imFile.thumbnail((1200, 1000))
    cSize = imFile.size
    imFile = ImageTk.PhotoImage(imFile)

    cs = Canvas(window, width=cSize[0], height=cSize[1])
    cs.pack()
    image = cs.create_image(cSize[0]//2, cSize[1]//2, anchor=CENTER, image=imFile)
    cs.bind("<Button-1>", canvasCallback)

    confirm = Button(window, text="Confirm", command=gotchu)
    confirm.pack()

    window.mainloop()

selectCentre(Image.open('images/house-piano-dog.jpg'))