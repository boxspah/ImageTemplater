import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk
import re
import datetime

class Displayable:
    # stores a smaller version of image intended to fit within maxDimensions
    # stores resulting scale ratio in scaleRatio
    def __init__(self, image, maxDimensions=(1200, 1000)):
        self.initImage = image
        self.initSize = image.size

        self.image = image.copy()
        self.image.thumbnail(maxDimensions, Image.ANTIALIAS)
        self.size = self.image.size
        self.scaleRatio = self.size[0]/image.width

    # returns a PhotoImage of image for use with tkinter
    def getPhotoImage(self):
        return ImageTk.PhotoImage(self.image)

    # resizes image by ratio
    # ratio scales relative to current image size by default (deceleration behaviour)
    # absolute=True forces scaling relative to original Displayable size
    def scale(self, ratio, absolute=False):
        if absolute:
            self.image = self.initImage.resize((int(ratio*self.scaleRatio*self.initSize[0]), int(ratio*self.scaleRatio*self.initSize[1])), resample=Image.ANTIALIAS)
        else:
            self.image = self.initImage.resize((int(ratio*self.image.width), int(ratio*self.image.height)), resample=Image.ANTIALIAS)

class CentreSelector:
    def __init__(self, template, image):
        self.window = tk.Tk()
        self.window.title('Position the image in the template')

        self.canvasBg = Displayable(template)
        self.canvasSize = self.canvasBg.size
        self.canvas = tk.Canvas(self.window, width=self.canvasSize[0], height=self.canvasSize[1])

        self.image = Displayable(image)
        self.imagePhoto = self.image.getPhotoImage()
        self.canvas_image = self.canvas.create_image(self.canvasSize[0]//2, self.canvasSize[1]//2, anchor=tk.CENTER, image=self.imagePhoto, tags='draggable')
        self._drag_data = {'x': 0, 'y': 0, 'item': None}
        self.zoomLvl = 0
        self.canvas.bind('<ButtonPress-1>', self.on_drag_start)
        self.canvas.bind('<ButtonRelease-1>', self.on_drag_release)
        self.canvas.bind('<B1-Motion>', self.on_drag_motion)
        self.canvas.bind('<MouseWheel>', self.zoom)

        self.canvasBgPhoto = self.canvasBg.getPhotoImage()
        self.canvas.create_image(self.canvasSize[0], self.canvasSize[1], anchor=tk.SE, image=self.canvasBgPhoto)

        self.rename = tk.Frame(bd=3, relief=tk.GROOVE, padx=10, pady=5)
        self.lab_rename = tk.Label(self.rename, text='Output filename:')
        self.filename = tk.Entry(self.rename, width=70)
        self.filesearch = tk.Button(self.rename, text='Browse', command=self.browseFiles)
        self.fName = ''

        self.default = tk.Button(self.window, text='Default', command=self.default)
        self.confirm = tk.Button(self.window, text='Confirm', command=self.confirm)
    
    def on_drag_start(self, event):
        # record the item and its location
        self._drag_data['item'] = self.canvas.find_withtag('draggable')
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    def on_drag_release(self, event):
        # snap to template lines if near them
        threshold = 10
        location = self.canvas.bbox(self._drag_data['item'])
        if abs(location[2]-self.canvasSize[0]) < threshold:
            self.canvas.move(self._drag_data['item'], -location[2]+self.canvasSize[0], 0)
            print('Snapping to right boundary:', -location[2]+self.canvasSize[0])
        if abs(location[0]) < threshold:
            self.canvas.move(self._drag_data['item'], -location[0], 0)
            print('Snapping to left boundary:', -location[0])
        if abs(location[3]-self.canvasSize[1]) < threshold:
            self.canvas.move(self._drag_data['item'], 0, -location[3]+self.canvasSize[1])
            print('Snapping to lower boundary:', -location[3]+self.canvasSize[1])
        if abs(location[1]) < threshold:
            self.canvas.move(self._drag_data['item'], 0, -location[1])
            print('Snapping to upper boundary:', -location[1])
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

    def zoom(self, e):
        # scroll down
        if e.num == 5 or e.delta == -120:
            self.zoomLvl -= 1
        # scroll up
        if e.num == 4 or e.delta == 120:
            self.zoomLvl += 1
        self.image.scale(1 + self.zoomLvl*0.05, absolute=True)
        self.imagePhoto = self.image.getPhotoImage()
        self.canvas.itemconfig(self.canvas_image, image=self.imagePhoto)

    def browseFiles(self):
        tempName = tk.filedialog.asksaveasfilename(title="Select a location to save to:", filetypes=(('PNG', '*.png'), ('All files', '*.*')))
        if len(tempName) > 0:
            self.fName = tempName
            self.filename.delete(0, tk.END)
            self.filename.insert(0, self.fName)

    def default(self):
        self.fName = 'out/' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '.png'
        self.filename.delete(0, tk.END)
        self.filename.insert(0, self.fName)
        # move image to template centre
        self.canvas.coords(self.canvas_image, self.canvasSize[0]//2, self.canvasSize[1]//2)
        # reset zoom
        self.zoomLvl = 0
        self.image.scale(1, absolute=True)
        self.imagePhoto = self.image.getPhotoImage()
        self.canvas.itemconfig(self.canvas_image, image=self.imagePhoto)

    def confirm(self):
        if len(self.filename.get()):
            self.fName = self.filename.get()
            self.window.destroy()
        else:
            self.filename.config(bg='#ff8080')

    def show(self):
        self.canvas.pack()
        self.lab_rename.pack(side=tk.TOP)
        self.filename.pack(side=tk.LEFT)
        self.filename.insert(0, 'out/' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '.png')    # default filename
        self.filesearch.pack(side=tk.RIGHT)
        self.rename.pack()
        self.default.pack()
        self.confirm.pack()

        self.window.mainloop()

    def getFilename(self):
        name = self.fName
        if re.match(r'^[a-zA-Z0-9 \-_\(\)]+\.png$', name):
            return self.fName
        else:
            return self.fName + '.png'
