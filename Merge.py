from PIL import Image

def merge(mergeData):
    back = Image.open(backG)
    fore = Image.open(foreG)
    ratio = min(fore.size[0]/back.size[0], fore.size[1]/back.size[1])
    back = back.resize((math.floor(back.size[0]*ratio), math.floor(back.size[1]*ratio)), Image.ANTIALIAS)
    back = back.crop(box=(centreX-fore.size[0]//2, centreY-fore.size[1]//2, centreX+fore.size[0]//2, centreY+fore.size[1]//2))
    back = back.resize((fore.size[0], fore.size[1]), Image.ANTIALIAS)
    save = backG[7:-4], foreG[10:-4]
    Image.alpha_composite(back, fore).save("out/"+str(save)+".png")