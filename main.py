import os
from PIL import Image
import cache

def mergePics(backG,foreG):
    back = Image.open(backG)
    fore = Image.open(foreG)
    width, height = fore.size
    back = back.resize((width, height), Image.BILINEAR)
    save = backG[7:-4],foreG[10:-4]
    Image.alpha_composite(back, fore).save("out/"+str(save)+".png")

templates = {}
images = []
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
                print(tempName)
                bg.save(("images/"+tempName+".png"), quality=100)
                os.remove("images/"+im)
    except IOError:
        pass


for infile in os.listdir("images"):
    try:
        with Image.open('images/' + infile) as im:
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
            if cache.read(infile) == False:
                if("instagram" in infile.lower()):
                    templates['Instagram'].append(im)
                    cache.write([infile,"instagram"])
                elif("facebook" in infile.lower()):
                    templates['Facebook'].append(im)
                    cache.write([infile,"facebook"])
                elif("linkedin" in infile):
                    templates['Linkedin'].append(im)
                    cache.write([infile,"linkedin"])
                elif("twitter" in infile):
                    templates['Twitter'].append(im)
                    cache.write([infile,"twitter"])
                else:
                    print("NO KEYWORD IN THE FILENAME FOUND TO INDICATE THE APPROPRIATE TEMPLATE TYPE")
            else:
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
            mergePics(im.filename,t.filename)

    else:
        print("No appropriate templates found.")

print("--- All images processed. ---")