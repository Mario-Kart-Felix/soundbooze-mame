import mss
import cv2
import time
import numpy
from winid import *

def loadTemplate(filename):
    return cv2.imread(filename, 0)

def findMatch(background, template, threshold):
    img_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = numpy.where(result >= threshold)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

    if len(loc[0]) > 1:
        a = numpy.min(loc[1])
        b = numpy.min(loc[0])
        c = a + 216
        d = b + 12
        print a, b, c, d

def grab(width, height, left, top):

    with mss.mss() as sct:

        monitor = {"top": top, "left": left, "width": width, "height": height}

        pow_t = loadTemplate('tmpl/blood.png')

        while [ 1 ]:
            last_time = time.time()

            imgorg = sct.grab(monitor)
            img = numpy.array(imgorg)

            if findMatch(img, pow_t, 0.8):
                print ''

wid, width, height, left, top = query()
grab(width, height, left, top)
