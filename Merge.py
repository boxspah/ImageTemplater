from PIL import Image

def merge(template, image, mergeData, savefile):
    background = Image.open(image)
    foreground = Image.open(template)

    # crops same percentage of the image as was off-screen in the GUI
    background = background.crop(box=(background.width*mergeData['crop_left'], background.height*mergeData['crop_top'], background.width*(1-mergeData['crop_right']), background.height*(1-mergeData['crop_bottom'])))

    # downsize template to fit image
    foreground.thumbnail(background.size, Image.ANTIALIAS)

    # save combined image to disk
    background.paste(foreground, mask=foreground)
    background.save(savefile)