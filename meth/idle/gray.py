import cv2
import mss

import numpy
from scipy.stats import skew, kurtosis

import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

SPLIT        =    2
TOTAL_SAMPLE = 7500

def hsum(gray):
    numPixels = numpy.prod(gray.shape[:2])
    hist = cv2.calcHist([gray], [0], None, [16], [0, 255]) / numPixels
    s = skew(hist)
    k = kurtosis(hist)#, fisher=False)
    v = numpy.var(hist)
    h = numpy.sum(hist) / 100.0
    m = (s + k + v + h) / 4.0
    '''
    print ("%.5f"% (s)),
    print ("%.5f"% (k)),
    print ("%.5f"% (v)),
    print ("%.5f"% (hsum)),
    print ("(%.5f)"% (m))
    '''
    return s[0], k[0], v, h, m[0]

with mss.mss() as sct:

    monitor = {"top": 124, "left": 100, "width": 800, "height": 600}

    i = 0

    Z = [[],[],[],[]]
    
    while [ 1 ]:

        frame = numpy.array(sct.grab(monitor))
        # various-img-transform (color, sub,thres, flow, ...)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        V = numpy.vsplit(gray, SPLIT)
        x = 0
        for v in V:
            H = numpy.hsplit(v, SPLIT)
            for h in H:
                s, k, v, h, m = hsum(h)
                Z[x].append([s, k, v, h, m])
                x += 1

            if x != 0 and x % numpy.power(SPLIT, 2) == 0:
                x = 0

        print i
        if i != 0 and i % TOTAL_SAMPLE == 0:

            y = (numpy.power(SPLIT, 2) * 100) + 111
            for z in Z:
                plt.subplot(y)
                sns.heatmap(numpy.transpose(z))
                y += 1

            plt.show()

            break

        i += 1
