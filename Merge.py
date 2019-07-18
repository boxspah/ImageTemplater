from PIL import Image

def merge(template, image, mergeData, savefile):
    background = Image.open(image)
    foreground = Image.open(template)

    magic_ratio = mergeData['magic_ratio']

    # crops same percentage of the image as was off-screen in the GUI
    background = background.crop(box=(background.width*mergeData['crop_left'], background.height*mergeData['crop_top'], background.width*(1-mergeData['crop_right']), background.height*(1-mergeData['crop_bottom'])))

    # downsize template to fit image
    foreground = foreground.resize(tuple(int(dim*mergeData['magic_ratio']) for dim in foreground.size), resample=Image.LANCZOS)

    # save combined image to disk
    background.paste(foreground, mask=foreground)
    background.save(savefile)