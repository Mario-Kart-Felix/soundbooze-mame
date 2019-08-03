# -*- coding: utf-8 -*-

# versus bison only

import cv2
import mss
import time
import numpy

with mss.mss() as sct:

    body = {"top": 284, "left": 100, "width": 800, "height": 324}

    orbb = cv2.ORB_create()

    while [ 1 ]:

        b = numpy.array(sct.grab(body))
        b[:,:,1] = 0
        b[:,:,2] = 0
        b[b < 255] = 0
        grayb = b[:,:,0]

        kpOrbb, des = orbb.detectAndCompute(grayb, None)
        orbbimg = cv2.drawKeypoints(grayb, kpOrbb, None)

        ptsb = cv2.KeyPoint_convert(kpOrbb)
        for p in ptsb:
            S = [p[0], p[1]]
            ls = 1 if p[0] - 400 > 0 else -1
            rs = 1 if p[1] - 162 > 0 else -1
            print len (ptsb), ls, rs

        '''
        if len(ptsb) > 190:
            print 'siap'
        else:
            print 'blm'
        '''

        cv2.imshow("b", orbbimg)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
