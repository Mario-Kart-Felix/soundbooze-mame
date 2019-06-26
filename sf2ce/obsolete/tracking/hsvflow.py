import time
import sys
import cv2
import mss

import numpy as np

def grab(width, height, left, top):

    with mss.mss() as sct:

        monitor = {"top": top, "left": left, "width": width, "height": height}

        frame1 = np.array(sct.grab(monitor))
        prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        hsv = np.zeros_like(frame1)
        hsv[...,1] = 255

        while [ 1 ]:

            frame2 = np.array(sct.grab(monitor))

            next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

            flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

            mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
            hsv[...,0] = ang*180/np.pi/2
            hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
            #rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
            test = hsv[:,:,2]

            zsum = np.sum(test)
            if zsum > 1500000:
                test = np.zeros(test.shape)

            prvs = next

            cv2.imshow('frame2', test)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

grab(800, 100, 100, 440)
