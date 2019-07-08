import os
from PIL import Image
from CentreSelector import *
import math
import warnings

def mergePics(backG, foreG, centreX, centreY):
    back = Image.open(backG)
    fore = Image.open(foreG)
    ratio = min(fore.size[0]/back.size[0], fore.size[1]/back.size[1])
    back = back.resize((math.floor(back.size[0]*ratio), math.floor(back.size[1]*ratio)), Image.ANTIALIAS)
    back = back.crop(box=(centreX-fore.size[0]//2, centreY-fore.size[1]//2, centreX+fore.size[0]//2, centreY+fore.size[1]//2))
    back = back.resize((fore.size[0], fore.size[1]), Image.ANTIALIAS)
    save = backG[7:-4], foreG[10:-4]
    Image.alpha_composite(back, fore).save("out/"+str(save)+".png")

templates = {}
images = []
imgCentrePoints = []
platform_list = ['Instagram', 'Facebook', 'Twitter', 'Linkedin']
for p in platform_list:
    templates[p] = []

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

for infile in os.listdir("images"):
    try:
        with Image.open('images/' + infile) as im:
            print('Found image:', infile, im.format, "%dx%d" % im.size, im.mode)
            sel = CentreSelector(im)
            sel.show()
            imgCentrePoints.append(sel.getResult())
            images.append(im)
    except IOError:
        pass

if len(images) is 0:
    raise Exception('No images found.')

for infile in os.listdir("templates"):
    try:
        with Image.open('templates/' + infile) as im:
            print('Found template:', infile, im.format, "%dx%d" % im.size, im.mode)
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

for n, im in enumerate(images):
    platform = None
    print(f'Select a platform for {im.filename}:')
    while platform is None:
        for i, p in enumerate(platform_list):
            print(f'\t[{i}] {p}')
        try: platform = platform_list[int(input())]
        except IndexError: pass

    if len(templates[platform]) > 0:
        for t in templates[platform]:
            mergePics(im.filename, t.filename, imgCentrePoints[n][0], imgCentrePoints[n][1])
    else:
        warnings.warn("No templates found for platform")

print("--- All images processed. ---")