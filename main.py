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
# initialize empty array in dict key for each platform
for p in platform_list:
    templates[p] = []

# get filepaths of images in images/ directory
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

# get filepaths of templates in templates/ directory
# store filepaths in appropriate dict key list
# a template can belong to MORE THAN ONE platform
for infile in os.listdir('templates'):
    identified = False
    try:
        fpath = 'templates/' + infile
        with Image.open(fpath) as im:
            print('Found template:', infile, im.format, "%dx%d" % im.size, im.mode)
            lower_infile = infile.lower()
            for p in platform_list:
                if p.lower() in lower_infile:
                    templates[p].append(fpath)
                    identified = True
            if not identified:
                warnings.warn("Could not detect platform from filename for " + infile)
    except IOError:
        pass

# process each image individually
for im in images:
    print(f'Accessing {im}...')
    # prompt user for destination platform
    pSelect = PlatformSelect(platform_list)

    for platform, isSelected in pSelect.selectedPlatforms.items():
        if isSelected.get():
            if len(templates[platform]):
                print(f'Processing templates for {platform}...')
                # create editor and write output to disk for every template
                for t in templates[platform]:
                    a = ArrangeWindow(t, im)
                    merge(t, im, a.mergeData, a.fName.get())
            else:
                tempDisplay = tk.Tk()
                warnings.warn(f'No templates found for {platform}')
                if not tkinter.messagebox.askokcancel('No templates found', f'No templates were found in templates/ for {platform}. Press OK to continue processing other images, or press CANCEL to stop the program now.'):
                    raise SystemExit('User requested termination')
                tempDisplay.destroy()

tkinter.messagebox.showinfo('Templating finished', 'All images have been processed.')
print("--- All images processed. ---")