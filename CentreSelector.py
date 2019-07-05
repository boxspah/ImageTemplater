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
        self.finalPoint = None

        self.confirm = Button(self.window, text="Confirm", command=self.confirm, state=DISABLED)

    def canvasCallback(self, e):
        self.finalPoint = (e.x, e.y)
        print(self.finalPoint)
        if self.confirm['state'] is not NORMAL:
            self.confirm.config(state=NORMAL)
    
    def confirm(self):
        print('Position confirmed.')
        self.window.destroy()

    def show(self):
        self.canvas.pack()
        self.confirm.pack()

        self.window.mainloop()

    def getResult(self):
        return self.finalPoint