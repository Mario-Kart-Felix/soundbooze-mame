# -*- coding: utf-8 -*-

import cv2
import mss
import time
import numpy

with mss.mss() as sct:

    body = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        frame_b = numpy.array(sct.grab(body))
        frame_b[frame_b != 255] = 0

        gray = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)
        #gray[gray>0] = 255
        #gray[gray != 255] = 0
        gray[gray < 127] = 0
        #gray[gray > 127] = 0

        cv2.imshow("White", gray)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
