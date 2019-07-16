import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
from PIL import Image, ImageTk
import re
import datetime

class Displayable:
    # creates a smaller version of image intended to fit within maxDimensions
    # stores original ImageFile object in initImage
    def __init__(self, image, maxDimensions=(1400, 700)):
        self.initImage = Image.open(image)

        self.image = self.initImage.copy()
        self.image.thumbnail(maxDimensions, Image.ANTIALIAS)
        self.size = self.image.size
        self.width, self.height = self.size
        self.scaleRatio = self.width/self.initImage.width

    # returns a PhotoImage of image for use with tkinter
    def getPhotoImage(self):
        return ImageTk.PhotoImage(self.image)

    # scale resizes relative to current image size by default (zoom decelerates further from original size)
    # 100px --x0.95-> 95px --x0.95-> 90px --x0.95-> 86px
    #        (-5 px)        (-5 px)        (-4 px)
    #
    # absolute=True forces scaling relative to original Displayable size (no deceleration)
    def scale(self, ratio, absolute=False):
        if absolute:
            self.image = self.initImage.resize((int(ratio*self.scaleRatio*self.initImage.width), int(ratio*self.scaleRatio*self.initImage.height)), resample=Image.ANTIALIAS)
        else:
            self.image = self.initImage.resize((int(ratio*self.image.width), int(ratio*self.image.height)), resample=Image.ANTIALIAS)

class ArrangeWindow:
    def __init__(self, template, image):
        # create tkinter window
        self.window = tk.Tk()
        screen_dimensions = (self.window.winfo_screenwidth()*0.7, self.window.winfo_screenheight()*0.7)
        self.window.title('Position the image in the template')

        # handle window close event
        self.window.protocol('WM_DELETE_WINDOW', self.close)

        # create canvas elements
        self.canvasCover = Displayable(template, screen_dimensions)
        self.canvas = tk.Canvas(self.window, width=self.canvasCover.width, height=self.canvasCover.height, borderwidth=0, highlightthickness=0)
        self.image = Displayable(image, screen_dimensions)
        self.imagePhoto = self.image.getPhotoImage()
        self.canvas_image = self.canvas.create_image(self.canvasCover.width, self.canvasCover.height, anchor=tk.SE, image=self.imagePhoto, tags='draggable')
        self.canvasCoverPhoto = self.canvasCover.getPhotoImage()
        self.canvas.create_image(self.canvasCover.width, self.canvasCover.height, anchor=tk.SE, image=self.canvasCoverPhoto)
        # setup drag and drop
        self._drag_data = {'x': 0, 'y': 0, 'item': None}
        self.canvas.bind('<ButtonPress-1>', self.on_drag_start)
        self.canvas.bind('<ButtonRelease-1>', self.on_drag_release)
        self.canvas.bind('<B1-Motion>', self.on_drag_motion)
        # setup scroll-to-zoom
        self.zoomAmount = 1
        self.canvas.bind('<MouseWheel>', self.zoom)

        # create filename field and buttons
        self.rename = tk.Frame(bd=3, relief=tk.GROOVE, padx=10, pady=5)
        self.lab_rename = tk.Label(self.rename, text='Output filename:')
        self.fName = tk.StringVar(value='out/' + datetime.datetime.now().strftime('%Y-%m-%d %H%M%S') + '.png')  # set default filename
        vcmd = (self.rename.register(self.checkFilename), '%P')
        self.filename = tk.Entry(self.rename, width=70, textvariable=self.fName, validate=tk.ALL, validatecommand=vcmd)
        self.filesearch = tk.Button(self.rename, text='Browse', command=self.browseFiles)

        # create bottom buttons
        self.default = tk.Button(self.window, text='Default', command=self.default)
        self.confirm = tk.Button(self.window, text='Confirm', command=self.confirm)

        # position and display all window elements
        self.canvas.pack()
        self.lab_rename.pack(side=tk.TOP)
        self.filename.pack(side=tk.LEFT)
        self.filesearch.pack(side=tk.RIGHT)
        self.rename.pack()
        self.default.pack()
        self.confirm.pack()

        self.window.mainloop()

    def close(self):
        if tkinter.messagebox.askokcancel("Quit", "Do you really want to quit? All previously edited images will be saved and the program will stop running."):
            self.window.destroy()
            raise SystemExit('User requested termination')

    def on_drag_start(self, event):
        # record the item and its location
        self._drag_data['item'] = self.canvas.find_withtag('draggable')
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    def on_drag_release(self, event):
        # snap to template lines if within {threshold} pixels of them
        threshold = 10
        location = self.canvas.bbox(self._drag_data['item'])
        if abs(location[2]-self.canvasCover.width) < threshold:
            self.canvas.move(self._drag_data['item'], -location[2]+self.canvasCover.width, 0)
        if abs(location[3]-self.canvasCover.height) < threshold:
            self.canvas.move(self._drag_data['item'], 0, -location[3]+self.canvasCover.height)
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
            self.zoomAmount -= 0.05
        # scroll up
        if e.num == 4 or e.delta == 120:
            self.zoomAmount += 0.05
        # resize and update canvas image accordingly
        self.image.scale(self.zoomAmount, absolute=True)
        self.imagePhoto = self.image.getPhotoImage()
        self.canvas.itemconfig(self.canvas_image, image=self.imagePhoto)

    def browseFiles(self):
        tempName = tk.filedialog.asksaveasfilename(title="Select a location to save to:", defaultextension='.*', filetypes=(('PNG', '*.png'), ('All files', '*.*')))
        if len(tempName) > 0:
            self.fName.set(tempName)

    def default(self):
        # set filename to current timestamp
        self.fName.set('out/' + datetime.datetime.now().strftime('%Y-%m-%d %H%M%S') + '.png')
        # move image to bottom-right
        self.canvas.coords(self.canvas_image, self.canvasCover.width, self.canvasCover.height)
        # reset zoom and update canvas image
        self.zoomAmount = 1
        self.image.scale(1, absolute=True)
        self.imagePhoto = self.image.getPhotoImage()
        self.canvas.itemconfig(self.canvas_image, image=self.imagePhoto)

    def confirm(self):
        if len(self.fName.get()):
            image_pos = self.canvas.bbox(self.canvas_image)
            # stores percentage of image not visible on each side
            self.mergeData = {
                'crop_left': -image_pos[0]/self.zoomAmount/self.image.width if image_pos[0] < 0 else 0,
                'crop_top': -image_pos[1]/self.zoomAmount/self.image.height if image_pos[1] < 0 else 0,
                'crop_right': (image_pos[2]-self.canvasCover.width)/self.zoomAmount/self.image.width if image_pos[2] > self.canvasCover.width else 0,
                'crop_bottom': (image_pos[3]-self.canvasCover.height)/self.zoomAmount/self.image.height if image_pos[3] > self.canvasCover.height else 0,
            }
            self.window.destroy()
        else:
            self.filename.config(bg='#ff8080')

    def checkFilename(self, newValue):
        # ensure valid filepath using regex pattern
        if re.match(r'^[a-zA-Z0-9 \-_\(\)\/]+\.[a-z]+', newValue):
            return True
        return False