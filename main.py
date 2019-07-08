import os
from PIL import Image
import cache
import csv

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
                    cache.write([infile,im,"instagram"])
                elif("facebook" in infile.lower()):
                    templates['Facebook'].append(im)
                    cache.write([infile,im,"facebook"])
                elif("linkedin" in infile):
                    templates['Linkedin'].append(im)
                    cache.write([infile,im,"linkedin"])
                elif("twitter" in infile):
                    templates['Twitter'].append(im)
                    cache.write([infile,im,"twitter"])
                else:
                    print("NO KEYWORD IN THE FILENAME FOUND TO INDICATE THE APPROPRIATE TEMPLATE TYPE")
    except IOError:
        pass
with open('cache.csv', newline='') as csvfile:
     reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
     for row in reader:
        templates[row[2].capitalize()].append(row[1])
print(templates)

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