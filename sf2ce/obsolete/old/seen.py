import numpy as np
import cv2
import time
import mss

def last_seen(background, template, threshold):
    img_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
    if len(loc[0]) > 1:
        return True

def grab():

    with mss.mss() as sct:

        monitor = {"top": 400, "left": 100, "width": 800, "height": 100}

        id_t = None
        ls = 0

        while [ 1 ]:

            img = np.array(sct.grab(monitor))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            H = np.hsplit(gray, 2)

            if (id_t is None):
                id_t = H[0][48:130, 158:228]

            if last_seen(img, id_t, 0.8):
                ls = time.time()

            diff = time.time() - ls
            print diff
            if diff < 8.0:
                print 'L'
            elif diff > 8.0:
                print 'R'

            cv2.imshow('L', id_t)
            k = cv2.waitKey(20) & 0xff
            if k == 27:
                break

grab()
