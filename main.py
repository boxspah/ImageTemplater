import os
from PIL import Image

def mergePics(back,fore):
    print(back,fore)
    width, height = back.size
    # fore = fore.convert("RGBA")
    # back = back.convert("RGBA")
    fore = fore.resize((width, height), Image.BILINEAR)
    Image.alpha_composite(back, fore).save("out/"+imgList[0]+templateList[0]+".png")

templates = {}
images = []
platform_list = ['Instagram', 'Facebook', 'Twitter', 'Linkedin']
for p in platform_list:
    templates[p] = []

for im in os.listdir("images"):
    # im = Image.open("Ba_b_do8mag_c6_big.png")
    # bg = Image.new("RGB", im.size, (255,255,255))
    # bg.paste(im,im)
    # bg.save("colors.jpg")
    # Converting jpeg to
for infile in os.listdir("images"):
    try:
        with Image.open('images/' + infile) as im:
            print(im)
            im.convert("RGBA")
            print(im)
            print('Found image: ', infile, im.format, "%dx%d" % im.size, im.mode)
            images.append(im)
    except IOError:
        pass

if len(images) is 0:
    raise Exception('No images found.')

for infile in os.listdir("templates"):
    try:
        with Image.open('templates/' + infile) as im:
            print('Found image: ', infile, im.format, "%dx%d" % im.size, im.mode)
            if("instagram" in infile.lower()):
                templates['Instagram'].append(im)
            elif("facebook" in infile.lower()):
                templates['Facebook'].append(im)
            elif("linkedin" in infile):
                templates['Linkedin'].append(im)
            elif("twitter" in infile):
                templates['Twitter'].append(im)
            else:
                print("NO KEYWORD IN THE FILENAME FOUND TO INDICATE THE APPROPRIATE TEMPLATE TYPE")
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
            mergePics(im,t)
    else:
        print("No appropriate templates found.")

print("--- All images processed. ---")