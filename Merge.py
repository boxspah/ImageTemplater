from PIL import Image

def merge(template, image, mergeData, savefile):
    background = Image.open(image)
    foreground = Image.open(template)

    # crops same percentage of the image as was off-screen in the GUI
    background = background.crop(box=(background.width*mergeData['crop'][0], background.height*mergeData['crop'][1], background.width*(1-mergeData['crop'][2]), background.height*(1-mergeData['crop'][3])))

    # downsize template to fit image
    foreground = foreground.resize(tuple(int(dim*mergeData['magic_ratio']) for dim in foreground.size), resample=Image.LANCZOS)

    # save combined image to disk
    collage = Image.new('RGBA', foreground.size, color=(255, 255, 255, 0))
    collage.paste(background, box=(int(foreground.width*mergeData['offset'][0]), int(foreground.height*mergeData['offset'][1])))
    collage.paste(foreground, mask=foreground)
    collage.save(savefile)