import os
from PIL import Image

templates = {
    "facebook" : [],
    "instagram" : [],
    "twitter" : [],
    "linkedin" : []
}

for infile in os.listdir("templates"):
    try:
        with Image.open('templates/' + infile) as im:
            print('Found image: ', infile, im.format, "%dx%d" % im.size, im.mode)
            if("instagram" in infile.lower()):
                templates['instagram'].append(im)
            elif("facebook" in infile.lower()):
                templates['facebook'].append(im)
            elif("linkedin" in infile):
                templates['linkedin'].append(im)
            elif("twitter" in infile):
                templates['twitter'].append(im)
            else:
                print("NO KEYWORD IN THE FILENAME FOUND TO INDICATE THE APPROPRIATE TEMPLATE TYPE")
    except IOError:
        pass

print(templates)
