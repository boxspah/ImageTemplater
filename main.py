import os
from PIL import Image
from PlatformSelect import PlatformSelect
from ArrangeWindow import ArrangeWindow
from Merge import merge
import warnings
import tkinter as tk
import tkinter.messagebox

templates = {}
images = []
platform_list = ['Instagram', 'Facebook', 'Twitter', 'Linkedin']
for p in platform_list:
    templates[p] = []

for infile in os.listdir('images'):
    try:
        fpath = 'images/' + infile
        with Image.open(fpath) as im:
            print('Found image:', infile, im.format, "%dx%d" % im.size, im.mode)
            images.append(fpath)
    except IOError:
        pass

if len(images) is 0:
    tkinter.messagebox.showerror('No images found', 'No images were found in the images/ directory.\nStopping the program.')
    raise FileNotFoundError('No images found.')

for infile in os.listdir('templates'):
    try:
        fpath = 'templates/' + infile
        with Image.open(fpath) as im:
            print('Found template:', infile, im.format, "%dx%d" % im.size, im.mode)
            # FIXME: Optimize platform categorization
            if("instagram" in infile.lower()):
                templates['Instagram'].append(fpath)
            elif("facebook" in infile.lower()):
                templates['Facebook'].append(fpath)
            elif("linkedin" in infile):
                templates['Linkedin'].append(fpath)
            elif("twitter" in infile):
                templates['Twitter'].append(fpath)
            else:
                warnings.warn("Could not detect platform from filename for " + infile)
    except IOError:
        pass

for im in images:
    print(f'Accessing {im}...')
    pSelect = PlatformSelect(platform_list)

    for platform, isSelected in pSelect.selectedPlatforms.items():
        if len(templates[platform]) and isSelected.get():
            print(f'Processing templates for {platform}...')
            for t in templates[platform]:
                a = ArrangeWindow(t, im)
                a.show()
                try:
                    merge(t, im, a.mergeData, a.getFilename())
                except AttributeError:
                    break
        elif not len(templates[platform]):
            tempDisplay = tk.Tk()
            warnings.warn(f'No templates found for {platform}')
            if not tkinter.messagebox.askokcancel('No templates found', f'No templates were found in templates/ for {platform}. Press OK to continue processing other images, or press CANCEL to stop the program now.'):
                raise SystemExit('User requested termination')
            tempDisplay.destroy()

tkinter.messagebox.showinfo('Templating finished', 'All images have been processed.')
print("--- All images processed. ---")