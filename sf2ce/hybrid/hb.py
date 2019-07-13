# -*- coding: utf-8 -*-

import cv2
import mss
import time
import numpy

from scipy.signal import find_peaks

with mss.mss() as sct:

    body = {"top": 324, "left": 100, "width": 800, "height": 400}
    head = {"top": 124, "left": 100, "width": 800, "height": 100}

    prevframe_h = numpy.array(sct.grab(head))
    prevzcount = 0

    HB = [0, 0, 0, 0]

    while [ 1 ]:

        frame_h = numpy.array(sct.grab(head))
        frame_b = numpy.array(sct.grab(body))

        red = frame_b.copy()
        red[:,:,0] = 0
        red[:,:,1] = 0
        red[red < 250] = 0

        # head

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

            HB[0], HB[1] = j, prevzcount

            prevzcount = zcount

        prevframe_h = frame_h

        # body

        H = numpy.hsplit(red, 8)
        S = []
        for h in H:
            hsum = numpy.sum(h)/1000000.0
            S.append(hsum)

        peaks, _ = find_peaks(S, height=0)

        if len(peaks) == 2:
            p1 = S[peaks[0]]
            p2 = S[peaks[1]] 
            pabs = numpy.absolute(p1-p2)
            h = numpy.argmax(S)
            HB[2], HB[3] = h, pabs

        print HB
