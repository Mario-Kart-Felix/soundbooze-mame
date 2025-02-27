import cv2
import numpy

class TEMPLATE:

    def __init__(self):
        self.threshold = 0.9

    def p1s(self):
        return cv2.imread('template/p1/1ps.png', 0)

    def p1l(self):
        return cv2.imread('template/p1/1pl.png', 0)

    def pow(self):
        return cv2.imread('template/p1/pow.png', 0)
 
    def blood(self):
        return cv2.imread('template/blood.png', 0)
 
    def match(self, background, template):
        gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray,template,cv2.TM_CCOEFF_NORMED)
        loc = numpy.where(result >= self.threshold)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        if len(loc[0]) > 1:
            return True
        else:
            return False
