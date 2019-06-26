# -*- coding: utf-8 -*-

import sys
import cv2
import mss
import numpy

with mss.mss() as sct:

    body = {"top": 284, "left": 100, "width": 800, "height": 300+24}

    R, G, B = [], [], [] 
    i = 0
    while [ 1 ]:

        frame_b = numpy.array(sct.grab(body))

        numPixels = numpy.prod(frame_b.shape[:2])
        (b, g, r, _) = cv2.split(frame_b)
        histogramR = cv2.calcHist([r], [0], None, [16], [0, 255]) / numPixels
        histogramG = cv2.calcHist([g], [0], None, [16], [0, 255]) / numPixels
        histogramB = cv2.calcHist([b], [0], None, [16], [0, 255]) / numPixels

        R.append(numpy.sum(histogramR))
        G.append(numpy.sum(histogramG))
        B.append(numpy.sum(histogramB))

        if i != 0 and i % 1600 == 0:
            M = [numpy.sum(R), numpy.sum(G), numpy.sum(B)]
            m = numpy.argmin(M)
            if m == 0:
                print 'R'
            elif m == 1:
                print 'G'
            elif m == 2:
                print 'B'

            R, G, B = [], [], [] 

        i += 1
