# -*- coding: utf-8 -*-

import cv2
import mss
import time
import numpy

from scipy.signal import find_peaks

with mss.mss() as sct:

    header = {"top": 124, "left": 100, "width": 800, "height": 100}

    prevframe_h = numpy.array(sct.grab(header))

    prevzcount = 0

    while [ 1 ]:

        last_time = time.time()

        frame_h = numpy.array(sct.grab(header))

        red = frame_h.copy()
        green = frame_h.copy()
        blue = frame_h.copy()

        sumdiff = numpy.sum(frame_h - prevframe_h)
        if sumdiff > 0:
            (b, g, r, _) = cv2.split(frame_h)
            B = b.ravel()
            G = g.ravel()
            B[B<255] = 0
            G[G<255] = 0

            zcount = 0
            for i in range(len(B)):
                if B[i] == 255 and G[i] == 255:
                    zcount += 1
                    
            j = numpy.absolute(zcount - prevzcount)/1000.0
            if j > 0:
                print '[↥]', time.time(), j, prevzcount

            prevzcount = zcount

        prevframe_h = frame_h

        #print("fps: {}".format(1 / (time.time() - last_time)))
