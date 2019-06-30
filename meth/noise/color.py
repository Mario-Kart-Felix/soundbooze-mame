# -*- coding: utf-8 -*-

import cv2
import mss
import time
import numpy

with mss.mss() as sct:

    body = {"top": 284, "left": 100, "width": 800, "height": 300+24}

    R, G, B = [], [], []
    i = 0

    while [ 1 ]:

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

        '''
        gray = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
        white = gray.copy()
        white[white > 0] = 255

        '''

        R.append(numpy.sum(red))
        G.append(numpy.sum(green))
        B.append(numpy.sum(blue))
        
        cv2.imshow("R", red)
        cv2.imshow("G", green)
        cv2.imshow("B", blue)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

        if i != 0 and i % 600 == 0:
            M = [numpy.sum(R), numpy.sum(G), numpy.sum(B)]
            m = numpy.argmin(M) #min != yg diharapkhan
            if m == 0:
                print 'R'
            elif m == 1:
                print 'G'
            elif m == 2:
                print 'B'

            R, G, B= [], [], []

        i += 1
