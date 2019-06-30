# -*- coding: utf-8 -*-

import cv2
import mss
import time
import numpy

from scipy.signal import find_peaks

with mss.mss() as sct:

    body = {"top": 324, "left": 100, "width": 800, "height": 400}

    while [ 1 ]:

        last_time = time.time()

        frame_b = numpy.array(sct.grab(body))

        red = frame_b.copy()
        green = frame_b.copy()
        blue = frame_b.copy()

        # body

        red[:,:,0] = 0
        red[:,:,1] = 0
        red[red < 250] = 0

        green[:,:,0] = 0
        green[:,:,2] = 0
        green[green < 250] = 0

        blue[:,:,1] = 0
        blue[:,:,2] = 0
        blue[blue < 250] = 0

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
            if pabs < 0.18:
                h = numpy.argmax(S)
                print '[↭]', time.time(), h, pabs

        #print("fps: {}".format(1 / (time.time() - last_time)))
