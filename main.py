import os
from PIL import Image

def mergePics(back,fore):
    width, height = back.size
    fore = fore.convert("RGBA")
    back = back.convert("RGBA")
    fore = fore.resize((width, height), Image.BILINEAR)
    Image.alpha_composite(back, fore).save("out/"+imgList[0]+templateList[0]+".png")

templates = {}
images = []
platform_list = ['Instagram', 'Facebook', 'Twitter', 'Linkedin']
for p in platform_list:
    templates[p] = []

for infile in os.listdir("images"):
    try:
        with Image.open('images/' + infile) as im:
            print('Found image: ', infile, im.format, "%dx%d" % im.size, im.mode)
            images.append(im)
    except IOError:
        pass

if len(images) is 0:
    raise Exception('No images found.')

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