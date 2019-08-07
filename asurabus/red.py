# -*- coding: utf-8 -*-

import cv2
import mss
import time
import numpy

with mss.mss() as sct:

    body = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        red = numpy.array(sct.grab(body))
        red[:,:,0] = 0
        red[:,:,1] = 0
        red[red < 250] = 0
        gray = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
        white = gray.copy()
        white[white > 0] = 255

        cv2.imshow("R", white)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
