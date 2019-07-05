import os
from PIL import Image
import random
import colorsys

pixels = []
for im in os.listdir("images"):
	try:
		with Image.open('images/' + im) as image:
			images = []
			pix = image.load()
			width, height = image.size
			for i in range(0,int(((width*height)*0.025))):
				row = random.randint(0,width-1)
				col = random.randint(0,height-1)
				rgb = pix[row,col]
				images.append(colorsys.rgb_to_hls(rgb[0]+1,rgb[1]+1,rgb[2]+1))

			pixels.append(images)
			print(images)
	except IOError:
		pass