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

        monitor = {"top": 600, "left": 100, "width": 800, "height": 100}

        id_t = None
        ls = 0
        ls_flip = 0

        while [ 1 ]:

            img = np.array(sct.grab(monitor))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            H = np.hsplit(gray, 2)

            if (id_t is None):
                id_t = H[0][40:70, 160:280]

            id_t_flip = cv2.flip(id_t, 1)

            if last_seen(img, id_t, 0.8):
                ls = time.time()
                print 'L', time.time() - ls

            elif last_seen(img, id_t_flip, 0.8):
                ls_flip = time.time()
                print 'R', time.time() - ls_flip

            cv2.imshow('L', id_t)
            cv2.imshow('R', id_t_flip)
            k = cv2.waitKey(20) & 0xff
            if k == 27:
                break

grab()
