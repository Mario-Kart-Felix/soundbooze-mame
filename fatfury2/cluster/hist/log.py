import sys
import cv2
import mss
import time
import numpy

def histogramsum(frame):
    numPixels = numpy.prod(frame.shape[:2])
    (b, g, r, a) = cv2.split(frame)
    histogramR = cv2.calcHist([r], [0], None, [16], [0, 255]) / numPixels
    histogramG = cv2.calcHist([g], [0], None, [16], [0, 255]) / numPixels
    histogramB = cv2.calcHist([b], [0], None, [16], [0, 255]) / numPixels
    hsumR = numpy.sum(histogramR.ravel())
    hsumG = numpy.sum(histogramG.ravel())
    hsumB = numpy.sum(histogramB.ravel())
    return hsumR + hsumG + hsumB

with mss.mss() as sct:

    full = {"top": 124, "left": 100, "width": 800, "height": 600+24}

    H = []
    i = 0
    while [1]:

        frame = numpy.array(sct.grab(full))
        H.append(histogramsum(frame))

        if i != 0 and i % 7500 == 0:
            print '[Saved]'
            numpy.save('H-' + str(time.time()), numpy.array(H))
            H = []
            i = 0

        i += 1
