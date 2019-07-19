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
        self.image.thumbnail(maxDimensions, Image.LANCZOS)
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
            self.image = self.initImage.resize((int(ratio*self.scaleRatio*self.initImage.width), int(ratio*self.scaleRatio*self.initImage.height)), resample=Image.LANCZOS)
        else:
            self.image = self.initImage.resize((int(ratio*self.image.width), int(ratio*self.image.height)), resample=Image.LANCZOS)

class Editor:
    def __init__(self, template, image):
        # create tkinter window
        self.window = tk.Tk()
        screen_dimensions = (self.window.winfo_screenwidth()*0.7, self.window.winfo_screenheight()*0.7)
        self.window.title('Position the image in the template')
        # handle window close event
        self.window.protocol('WM_DELETE_WINDOW', self.close)

        current_file = tk.Frame(padx=10, pady=5)
        lab_file_name = tk.Label(current_file, text='Currently editing:')
        file_name = tk.Entry(current_file, width=50)
        file_name.insert(0, image)
        file_name.config(state='readonly')
        lab_file_name.pack(side=tk.LEFT)
        file_name.pack(side=tk.RIGHT)
        current_file.pack(pady=5)

        # create canvas elements
        editDisplay = tk.Frame()
        self.canvasCover = Displayable(template, screen_dimensions)
        self.canvas = tk.Canvas(editDisplay, width=self.canvasCover.width, height=self.canvasCover.height, borderwidth=0, highlightthickness=0)
        self.image = Displayable(image, screen_dimensions)
        self.imagePhoto = self.image.getPhotoImage()
        self.canvas_image = self.canvas.create_image(self.canvasCover.width, self.canvasCover.height, anchor=tk.SE, image=self.imagePhoto, tags='draggable')
        self.canvasCoverPhoto = self.canvasCover.getPhotoImage()
        self.canvas.create_image(self.canvasCover.width, self.canvasCover.height, anchor=tk.SE, image=self.canvasCoverPhoto)
        self.canvas.pack()
        # setup drag and drop
        self._drag_data = {'x': 0, 'y': 0, 'item': None}
        self.canvas.bind('<ButtonPress-1>', self.on_drag_start)
        self.canvas.bind('<ButtonRelease-1>', self.on_drag_release)
        self.canvas.bind('<B1-Motion>', self.on_drag_motion)
        # setup scroll-to-zoom
        self.zoomAmount = tk.DoubleVar(value=1.0)
        self.canvas.bind('<MouseWheel>', self.scrollZoom)
        # create slider to adjust zoomAmount
        self.zoomSlider = tk.Scale(editDisplay, label='Zoom', showvalue=True, length=0.8*self.canvasCover.width, from_=0.5, to=5, resolution=0.025, tickinterval=0.25, orient=tk.HORIZONTAL, command=self.sliderZoom)
        self.zoomSlider.set(1.0)
        self.zoomSlider.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        # associated Entry widget to display zoomAmount
        zoomEntry = tk.Entry(editDisplay, width=5, justify=tk.CENTER, textvariable=self.zoomAmount, state='readonly')
        zoomEntry.pack(side=tk.RIGHT, fill=tk.X, padx=5)
        editDisplay.pack(fill=tk.BOTH, expand=True)

        # create filename field and buttons
        rename = tk.Frame(bd=3, relief=tk.GROOVE, padx=10, pady=5)
        lab_rename = tk.Label(rename, text='Output filename:')
        self.fName = tk.StringVar(value='out/' + datetime.datetime.now().strftime('%Y-%m-%d %H%M%S') + '.png')  # set default filename
        self.filename = tk.Entry(rename, width=70, textvariable=self.fName)
        filesearch = tk.Button(rename, text='Browse', command=self.browseFiles)
        lab_rename.pack(side=tk.TOP)
        self.filename.pack(side=tk.LEFT, fill=tk.X, expand=True)
        filesearch.pack(side=tk.RIGHT)
        rename.pack(fill=tk.BOTH, expand=True)

        # create bottom buttons
        self.default = tk.Button(self.window, text='Default', pady=5, command=self.default)
        self.confirm = tk.Button(self.window, text='Confirm', pady=5, command=self.confirm)
        self.default.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.confirm.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # set minimum window size
        self.window.update()
        self.window.minsize(self.window.winfo_width(), self.window.winfo_height())
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
        # snap to canvas boundaries if within {threshold} pixels of them
        threshold = 10
        location = self.canvas.bbox(self._drag_data['item'])
        # right border
        if abs(location[2]-self.canvasCover.width) < threshold:
            self.canvas.move(self._drag_data['item'], -location[2]+self.canvasCover.width, 0)
        # left border
        elif abs(location[0]) < threshold:
            self.canvas.move(self._drag_data['item'], -location[0], 0)
        # bottom border
        if abs(location[3]-self.canvasCover.height) < threshold:
            self.canvas.move(self._drag_data['item'], 0, -location[3]+self.canvasCover.height)
        # top border
        elif abs(location[1]) < threshold:
            self.canvas.move(self._drag_data['item'], 0, -location[1])
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

    def sliderZoom(self, e):
        self.zoomAmount.set(float(e))
        # resize and update canvas image accordingly
        self.image.scale(float(e), absolute=True)
        self.imagePhoto = self.image.getPhotoImage()
        self.canvas.itemconfig(self.canvas_image, image=self.imagePhoto)

    def scrollZoom(self, e):
        # scroll down
        if e.num == 5 or e.delta == -120:
            self.zoomAmount.set(self.zoomAmount.get()-0.05)
        # scroll up
        if e.num == 4 or e.delta == 120:
            self.zoomAmount.set(self.zoomAmount.get()+0.05)
        # update slider
        self.zoomSlider.set(self.zoomAmount.get())
        # resize and update canvas image accordingly
        self.image.scale(self.zoomAmount.get(), absolute=True)
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
        self.zoomAmount.set(1.0)
        self.zoomSlider.set(1.0)
        self.image.scale(1, absolute=True)
        self.imagePhoto = self.image.getPhotoImage()
        self.canvas.itemconfig(self.canvas_image, image=self.imagePhoto)

    def confirm(self):
        if re.match(r'^[^<>:;,?"*|]+\.[a-z]{3,}$', self.fName.get()):
            image_pos = self.canvas.bbox(self.canvas_image)
            zoomAmount = self.zoomAmount.get()
            self.mergeData = {
                # ratio to maintain canvas size ratios for actual images
                'magic_ratio': self.canvasCover.scaleRatio/self.image.scaleRatio/zoomAmount,
                # horizontal and vertical offset from canvas edge (in % of canvas dimensions)
                'offset': (image_pos[0]/self.canvasCover.width if image_pos[0] > 0 else 0,
                           image_pos[1]/self.canvasCover.height if image_pos[1] > 0 else 0),
                # amount of image cut off by canvas (in % of image dimensions)
                'crop': (-image_pos[0]/zoomAmount/self.image.width if image_pos[0] < 0 else 0,
                        -image_pos[1]/zoomAmount/self.image.height if image_pos[1] < 0 else 0,
                        (image_pos[2]-self.canvasCover.width)/zoomAmount/self.image.width if image_pos[2] > self.canvasCover.width else 0,
                        (image_pos[3]-self.canvasCover.height)/zoomAmount/self.image.height if image_pos[3] > self.canvasCover.height else 0),
            }
            self.window.destroy()
        else:
            tkinter.messagebox.showwarning('Invalid filename', 'The provided filename is not valid.')
            self.filename.config(bg='#ff8080')