from PIL import Image
img = Image.open('misc/test.png')
import numpy as np
wc = (94, 152, 234)
# pixel_array = np.array(img)
# for x in range(img.width):
#   for y in range(img.height):
#     pixel = img.getpixel((x, y))
pixels = list(img.getdata())
pixel_array = [(int((r*2)/wc[0]), int((g*2)/wc[1]), int((b*2)/wc[2])) for (r, g, b) in pixels]
img.putdata(pixel_array)
img.show()