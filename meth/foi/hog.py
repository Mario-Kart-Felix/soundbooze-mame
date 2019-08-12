import sys
import cv2
import mss
import pywt
import numpy

from skimage import exposure
from skimage import feature

def blue(img):
    img[:,:,1] = 0
    img[:,:,2] = 0
    img[img < 254] = 0
    return img

with mss.mss() as sct:

    monitor = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        img = numpy.array(sct.grab(monitor))
        img = blue(img)
        img = cv2.resize(img, (100,75))

        (H, hogImage) = feature.hog(img, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1", visualize=True)
        hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
        hogImage = hogImage.astype("uint8")

        cv2.imshow("H", hogImage)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
