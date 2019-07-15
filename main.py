import os
from PIL import Image
from PlatformSelect import PlatformSelect
from ArrangeWindow import ArrangeWindow
from Merge import merge
import math
import warnings

templates = {}
images = []
platform_list = ['Instagram', 'Facebook', 'Twitter', 'Linkedin']
for p in platform_list:
    templates[p] = []

# TODO: Review whether PNG conversion is even necessary
for im in os.listdir("images"):
    try:
        with Image.open('images/' + im) as image:
            if os.path.splitext(im)[1] != ".png":
                bg = Image.new('RGBA', image.size, (255, 255, 255, 0))
                bg.paste(image)
                tempName = os.path.splitext(im)[0]
                bg.save(("images/"+tempName+".png"), quality=100)
                os.remove("images/"+im)
    except IOError:
        pass

for infile in os.listdir('images'):
    try:
        fpath = 'images/' + infile
        with Image.open(fpath) as im:
            print('Found image:', infile, im.format, "%dx%d" % im.size, im.mode)
            images.append(fpath)
    except IOError:
        pass

if len(images) is 0:
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
                    merge(t, im, a.getMergeData(), a.getFilename())
                except AttributeError:
                    break
        elif not len(templates[platform]):
            warnings.warn(f'No templates found for {platform}')

# TODO: Display message using GUI
print("--- All images processed. ---")