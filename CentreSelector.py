import tkinter as tk
from PIL import Image, ImageTk

class Displayable:
    def __init__(self, image, maxDimensions=(1200, 1000)):
        self.initialSize = image.size
        self.newImage = image.copy()
        self.newImage.thumbnail(maxDimensions, Image.ANTIALIAS)
        self.size = self.newImage.size
        self.scaleRatio = self.size[0]/image.size[0]

    def getPhotoImage(self):
        return ImageTk.PhotoImage(self.newImage)

class CentreSelector:

    def __init__(self, template, image):
        self.window = tk.Tk()
        self.window.title("Position the image in the template")

        self.canvasBg = Displayable(template)
        self.canvasSize = self.canvasBg.size
        self.canvas = tk.Canvas(self.window, width=self.canvasSize[0], height=self.canvasSize[1])
        self.canvasBgPhoto = self.canvasBg.getPhotoImage()
        self.canvasImg = self.canvas.create_image(self.canvasSize[0], self.canvasSize[1], anchor=tk.SE, image=self.canvasBgPhoto)
        self.canvas.bind("<Button-1>", self.canvasCallback)
        self.finalPoint = None

        self.rename = tk.Entry(self.window, width=50)

        self.default = tk.Button(self.window, text="Default", command=self.default)
        self.confirm = tk.Button(self.window, text="Confirm", command=self.confirm, state=tk.DISABLED)

    def canvasCallback(self, e):
        self.finalPoint = (round(e.x*self.canvasBg.scaleRatio, 0), round(e.y*self.canvasBg.scaleRatio, 0))
        if self.confirm['state'] is not tk.NORMAL:
            self.confirm.config(state=tk.NORMAL)
    
    def default(self):
        self.finalPoint = (round(self.canvasBg.initialSize[0]/2, 0), round(self.canvasBg.initialSize[1]/2, 0))
        self.fName = 'new.png'
        self.window.destroy()

    def confirm(self):
        self.fName = self.rename.get()
        self.window.destroy()

    def show(self):
        self.canvas.pack()
        self.rename.pack()
        self.rename.insert(0, 'new.png')    # default filename
        self.default.pack()
        self.confirm.pack()

        self.window.mainloop()

    def getResult(self):
        return self.finalPoint

    def getFilename(self):
        return self.fName