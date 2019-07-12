import os
from PIL import Image
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
                bg = Image.new('RGBA',image.size,(255,255,255))
                bg.paste(image,(0,0))
                tempName = os.path.splitext(im)[0]
                bg.save(("images/"+tempName+".png"), quality=100)
                os.remove("images/"+im)
    except IOError:
        pass

# FIXME: Images array should store only filenames
for infile in os.listdir("images"):
    try:
        with Image.open('images/' + infile) as im:
            print('Found image:', infile, im.format, "%dx%d" % im.size, im.mode)
            images.append(im)
    except IOError:
        pass

if len(images) is 0:
    raise Exception('No images found.')

# FIXME: Templates should be stored as filenames
for infile in os.listdir("templates"):
    try:
        with Image.open('templates/' + infile) as im:
            print('Found template:', infile, im.format, "%dx%d" % im.size, im.mode)
            # FIXME: Optimize platform categorization
            if("instagram" in infile.lower()):
                templates['Instagram'].append(im)
            elif("facebook" in infile.lower()):
                templates['Facebook'].append(im)
            elif("linkedin" in infile):
                templates['Linkedin'].append(im)
            elif("twitter" in infile):
                templates['Twitter'].append(im)
            else:
                warnings.warn("Could not detect platform from filename for " + infile)
    except IOError:
        pass

for im in images:
    platform = None
    print(f'Select a platform for {im.filename}:')
    while platform is None:
        for i, p in enumerate(platform_list):
            print(f'\t[{i}] {p}')
        try: platform = platform_list[int(input())]
        except IndexError: pass

    if len(templates[platform]) > 0:
        for t in templates[platform]:
            a = ArrangeWindow(t.filename, im.filename)
            a.show()
            merge(t.filename, im.filename, a.getMergeData(), a.getFilename())
    else:
        warnings.warn("No templates found for platform")

# TODO: Display message using GUI
print("--- All images processed. ---")