import tkinter as tk
from PIL import Image, ImageTk
import re

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
        self.window.title('Position the image in the template')

        self.canvasBg = Displayable(template)
        self.canvasSize = self.canvasBg.size
        self.canvas = tk.Canvas(self.window, width=self.canvasSize[0], height=self.canvasSize[1])

        self.image = Displayable(image)
        self.imagePhoto = self.image.getPhotoImage()
        self.canvas.create_image(self.canvasSize[0]//2, self.canvasSize[1]//2, anchor=tk.CENTER, image=self.imagePhoto, tags='draggable')
        self._drag_data = {'x': 0, 'y': 0, 'item': None}
        self.canvas.bind('<ButtonPress-1>', self.on_drag_start)
        self.canvas.bind('<ButtonRelease-1>', self.on_drag_release)
        self.canvas.bind('<B1-Motion>', self.on_drag_motion)

        self.canvasBgPhoto = self.canvasBg.getPhotoImage()
        self.canvas.create_image(self.canvasSize[0], self.canvasSize[1], anchor=tk.SE, image=self.canvasBgPhoto)

        self.rename = tk.Entry(self.window, width=50)

        self.default = tk.Button(self.window, text='Default', command=self.default)
        self.confirm = tk.Button(self.window, text='Confirm', command=self.confirm)
    
    def on_drag_start(self, event):
        # record the item and its location
        self._drag_data['item'] = self.canvas.find_withtag('draggable')
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    def on_drag_release(self, event):
        # reset the drag information
        self._drag_data['item'] = None
        self._drag_data['x'] = 0
        self._drag_data['y'] = 0

    def on_drag_motion(self, event):
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data['x']
        delta_y = event.y - self._drag_data['y']
        # move the object the appropriate amount
        self.canvas.move(self._drag_data['item'], delta_x, delta_y)
        # record the new position
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    def default(self):
        self.fName = 'new.png'
        # move image to template centre
        image = self.canvas.find_withtag('draggable')
        self.canvas.coords(image, self.canvasSize[0]//2, self.canvasSize[1]//2)

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

    def getFilename(self):
        name = self.fName
        if re.match(r"^[a-zA-Z0-9 ]+\.png$", name):
            return self.fName
        else:
            return self.fName + '.png'
