import os
import sys
import cv2
import numpy

i = 0

os.mkdir('crop')

def crop(img, h, w):
    global i
    from PIL import Image
    height, width, _ = img.shape
    for t in range(0, height, h):
        for l in range(0, width, w):
            im_pil = Image.fromarray(img)
            im_crop = im_pil.crop((t, l, t+h, l+w))
            im_np = numpy.asarray(im_crop)
            if numpy.sum(im_np) > 0:
                cv2.imwrite('crop/' + str(i) + '.png', im_np)
                i += 1

directory = sys.argv[1] 
for _, _, fileList in os.walk(directory):
    for fname in fileList:
        img = cv2.imread(directory + fname)
        crop(img, int(sys.argv[2]), int(sys.argv[3]))

# python cropper.py terrybogard/L/fire/ 400 400
# python cropper.py terrybogard/L/kick/ 400 400
# python cropper.py terrybogard/L/punch/ 400 400
# python cropper.py terrybogard/L/super/ 400 400

# python cropper.py terrybogard/R/fire/ 400 400
# python cropper.py terrybogard/R/kick/ 400 400
# python cropper.py terrybogard/R/punch/ 400 400
# python cropper.py terrybogard/R/super/ 400 400
