import sys
import cv2
import numpy
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def crop(img, step, w):

    from PIL import Image

    _, width, _ = img.shape

    fn = 0
    sumBlur = []
    for l in range(0, width, step):
        im_pil = Image.fromarray(img)
        im_crop = im_pil.crop((l, 0, l+w, 90))
        im_np = numpy.asarray(im_crop)
        s = numpy.sum(im_np)
        if s > 0:
            sumBlur.append(s)
            cv2.imwrite('tmp/' + str(fn) + '.png', im_np)
            fn = fn + 1

    peaks, _ = find_peaks(sumBlur, height=0)
    print peaks

    plt.plot(sumBlur)
    plt.show()

    '''
    a = numpy.sort(sumBlur)
    a = a[::-1]
    print a
    '''

filename = sys.argv[1] 
img = cv2.imread(filename)
crop(img, 8, 110)
