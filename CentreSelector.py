from tkinter import *
from PIL import Image, ImageTk

class CentreSelector():

    def __init__(self, imFile):
        self.window = Tk()
        self.window.title("Select the centre of the image below:")

        imFile.thumbnail((1200, 1000))
        self.cSize = imFile.size
        self.imFile = ImageTk.PhotoImage(imFile)

        self.canvas = Canvas(self.window, width=self.cSize[0], height=self.cSize[1])
        self.image = self.canvas.create_image(self.cSize[0]//2, self.cSize[1]//2, anchor=CENTER, image=self.imFile)
        self.canvas.bind("<Button-1>", self.canvasCallback)

        self.confirm = Button(self.window, text="Confirm", command=self.gotchu)

    def canvasCallback(self, e):
        print('Clicked at', e.x, e.y)
    
    def gotchu(self):
        print('Position confirmed.')

    def show(self):
        self.canvas.pack()
        self.confirm.pack()

        self.window.mainloop()