# -*- coding: utf-8 -*-

import cv2
import mss
import time
import numpy

def paper(img):
    img[:,:,0] = 0
    img[:,:,2] = 0
    img[img < 127] = 0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    white = gray.copy()
    white[white > 0] = 255
    return white

with mss.mss() as sct:

    body = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        img1 = numpy.array(sct.grab(body))
        img2 = cv2.flip(img1, 1)     # horizontal
        cv2.imshow("l", img1 + img2) # operand
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
