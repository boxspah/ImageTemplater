from tkinter import *
from PIL import Image, ImageTk

class CentreSelector:

    def __init__(self, imFile):
        self.window = Tk()
        self.window.title("Select the centre of the image below:")

        self.orgSize = imFile.size
        imFile.thumbnail((1200, 1000), Image.ANTIALIAS)
        self.cSize = imFile.size
        self.scaleRatio = self.cSize[0]/self.orgSize[0]
        self.imFile = ImageTk.PhotoImage(imFile)

        self.canvas = Canvas(self.window, width=self.cSize[0], height=self.cSize[1])
        self.image = self.canvas.create_image(self.cSize[0]//2, self.cSize[1]//2, anchor=CENTER, image=self.imFile)
        self.canvas.bind("<Button-1>", self.canvasCallback)
        self.finalPoint = None

        self.default = Button(self.window, text="Default", command=self.default)
        self.confirm = Button(self.window, text="Confirm", command=self.confirm, state=DISABLED)

    def canvasCallback(self, e):
        self.finalPoint = (round(e.x*self.scaleRatio, 0), round(e.y*self.scaleRatio, 0))
        if self.confirm['state'] is not NORMAL:
            self.confirm.config(state=NORMAL)
    
    def default(self):
        self.finalPoint = (self.orgSize[0], self.orgSize[1])
        self.window.destroy()

    def confirm(self):
        self.window.destroy()

    def show(self):
        self.canvas.pack()
        self.default.pack()
        self.confirm.pack()

        self.window.mainloop()

    def getResult(self):
        return self.finalPoint