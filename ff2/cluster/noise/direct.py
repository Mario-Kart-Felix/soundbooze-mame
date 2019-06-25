# -*- coding: utf-8 -*-

import cv2
import mss
import time
import numpy

with mss.mss() as sct:

    body = {"top": 284, "left": 100, "width": 800, "height": 300+24}

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

        cv2.imshow("R", red)
        cv2.imshow("G", green)
        cv2.imshow("B", blue)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

        M = [numpy.sum(red), numpy.sum(green), numpy.sum(blue)]
        m = numpy.argmin(M) #min != yg diharapkhan -> save(gray)
        if m == 0:
            print 'R'
        elif m == 1:
            print 'G'
        elif m == 2:
            print 'B'
