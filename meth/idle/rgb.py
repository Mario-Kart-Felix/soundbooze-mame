import cv2
import mss

import numpy
from scipy.stats import skew, kurtosis

import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

SPLIT        =    2
TOTAL_SAMPLE = 7500

with mss.mss() as sct:

    monitor = {"top": 124, "left": 100, "width": 800, "height": 600}

    i = 0

    Z = [[],[],[],[]]
    
    while [ 1 ]:

        frame = numpy.array(sct.grab(monitor))

        V = numpy.vsplit(frame, SPLIT)
        x = 0
        for v in V:
            H = numpy.hsplit(v, SPLIT)
            for h in H:
                b = h[:,:,0]/255.0
                g = h[:,:,1]/255.0
                r = h[:,:,2]/255.0
                b = numpy.sum(b.ravel()) / 1000000.0
                g = numpy.sum(g.ravel()) / 1000000.0
                r = numpy.sum(r.ravel()) / 1000000.0
                Z[x].append([r, g, b])
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

            y = (numpy.power(SPLIT, 2) * 100) + 111
            for z in Z:
                ax = plt.subplot(y)
                ax.set_color_cycle(['red', 'green', 'blue'])
                plt.plot(z)
                y += 1

            plt.show()
            break

        i += 1
