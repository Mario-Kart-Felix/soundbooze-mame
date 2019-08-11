import cv2
import mss
import numpy
import time

from scene import *
from similar import *
from template import *
from haohmaru import *

class CONFIG:

    def __init__(self):
        self.sumpart   = [2548180, 2569879, 1973379, 1951680]

    def part(self, frame):
        return frame[560:600, 10:200]

if __name__ == '__main__':

    with mss.mss() as sct:

        haohmaru = HAOHMARU('Left', 'Right', 'Up', 'Down', 's', 'z', 'a')
        scene  = SCENE()
        similar = SIMILAR()
        template = TEMPLATE()
        config = CONFIG()

        cont = similar.cont()
        select = similar.select()
        blood = template.blood()
        poww = template.pow()
        p1s = template.p1s()
        p1l = template.p1l()

        while [ 1 ]:
        
            full  = numpy.array(sct.grab(scene.full))

            part = config.part(full)
            sumpart = numpy.sum(part)

            if sumpart ==  config.sumpart[0] or sumpart == config.sumpart[1] or sumpart == config.sumpart[2] or sumpart == config.sumpart[3]:
                print '[Skip]'
                haohmaru.select()

            sc = similar.compute(cont, full)
            ss = similar.compute(select, full)
            
            if sc >= similar.threshold:
                print '[Continue]'
                haohmaru.cont()

            elif ss >= similar.threshold:
                print '[Select]'
                haohmaru.select()

            elif template.match(full, blood):
                print '[Start]', time.time()

            elif template.match(full, poww):
                print '[Pow]', time.time()

            elif template.match(full, p1s) or template.match(full, p1l):
                print '[Sword off]', time.time()

            '''
            cv2.imshow('frame', part)
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break
            '''

