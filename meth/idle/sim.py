import cv2
import mss

import numpy
import matplotlib.pyplot as plt

from skimage.measure import compare_ssim

SPLIT        =    2
TOTAL_SAMPLE = 7500

def similar(img_a, img_b):
    img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
    h, w = img_a.shape
    img_a = cv2.resize(img_a, (w/SPLIT/2, h/SPLIT/2))
    img_b = cv2.resize(img_b, (w/SPLIT/2, h/SPLIT/2))
    sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
    return sim

with mss.mss() as sct:

    monitor = {"top": 124, "left": 100, "width": 800, "height": 600}

    i = 0

    Z = [[],[],[],[]]

    prevframes = []
    prevframe = numpy.array(sct.grab(monitor))

    VV = numpy.vsplit(prevframe, SPLIT)
    for vv in VV:
        HH = numpy.hsplit(vv, SPLIT)
        for hh in HH:
            prevframes.append(hh)

    while [ 1 ]:

        frames = []
        frame = numpy.array(sct.grab(monitor))

        V = numpy.vsplit(frame, SPLIT)

        for v in V:
            H = numpy.hsplit(v, SPLIT)
            for h in H:
                frames.append(h)
        
        x = 0
        for p, f in zip(prevframes, frames):
            s = similar(p, f)
            Z[x].append(s)
            x += 1

        prevframes = []
        prevframe = frame

        VV = numpy.vsplit(prevframe, SPLIT)
        xv = 0
        for vv in VV:
            HH = numpy.hsplit(vv, SPLIT)
            for hh in HH:
                prevframes.append(hh)
                xv += 1

        print i
        if i != 0 and i % TOTAL_SAMPLE == 0:

            y = (numpy.power(SPLIT, 2) * 100) + 111
            for z in Z:
                plt.subplot(y)
                plt.plot(z)
                y += 1

            plt.show()

            break

        i += 1
