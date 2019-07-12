from PIL import Image

def merge(template, image, mergeData, savefile):
    background = Image.open(image)
    foreground = Image.open(template)

    # crops same percentage of the image as was off-screen in the GUI
    background = background.crop(box=(background.width*mergeData['crop_left'], background.height*mergeData['crop_top'], background.width*(1-mergeData['crop_right']), background.height*(1-mergeData['crop_bottom'])))

    # crops same percentage of the image as was off-screen in the GUI
    background = background.crop(box=(background.width*mergeData['crop_x'], background.height*mergeData['crop_y'], background.width, background.height))
    # background = background.resize((int(background.width*ratio), int(background.height*ratio)), Image.ANTIALIAS)
    # background = background.resize((foreground.width, foreground.height), Image.ANTIALIAS)
    background.save(savefile)
    # NOTE: alpha_composite only works if foreground and background are the same size
    # Image.alpha_composite(background, foreground).save(savefile)