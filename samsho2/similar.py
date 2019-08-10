import cv2
import numpy
from skimage.measure import compare_ssim

class SIMILAR:

    def compute(img_a, img_b):
        img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
        img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
        sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
        return sim
