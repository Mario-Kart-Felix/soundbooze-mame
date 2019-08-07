import mss
import cv2
import time
import numpy

import PIL
import imagehash

from yashaou import *

class CONFIG:

    def __init__(self):

        self.head      = {"top": 124, "left": 100, "width": 800, "height":100}
        self.scene     = {"top": 124, "left": 100, "width": 800, "height":600}
        self.select    = 668378
        self.sumselect = 0
        self.sumcont   = 0
        self.cont_t    = cv2.imread('template/cont.png', 0)
        self.intro_t   = cv2.imread('template/intro.png', 0)
        self.fight_t   = cv2.imread('template/fight.png', 0)

    def findmatch(self, background, template, threshold):
            gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(gray,template,cv2.TM_CCOEFF_NORMED)
            loc = numpy.where(result >= threshold)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
            if len(loc[0]) > 1:
                return True
            else:
                return False

    def render(self):
        return numpy.array(sct.grab(self.scene))

    def compute(self):
        b = numpy.array(sct.grab(self.head))
        select = b[88:108, 666:766]
        self.sumselect = numpy.sum(select) 
            
class PHASH:

    def __init__(self):
        self.H       = {}
        #self.action  = ['left', 'jumpleft|kick', 'kick|left|kick', 'defendup(0)', 'defenddown(0)', 'fire(0)', 'superpunch(0)', 'superkick(0)', 'punch', 'kick', 'downkick', 'kick|jumpup|kick', 'right', 'jumpright|kick', 'kick|right|kick', 'defendup(1)', 'defenddown(1)', 'fire(1)', 'superpunch(1)', 'superkick(1)']
        #self.p       = numpy.random.rand(len(self.action))
        #self.p      /= numpy.sum(self.p)

    def append(self, h, r):
        self.H[h] = r

    def compute(self, frame):
        return str(imagehash.phash(PIL.Image.fromarray(frame)))

if __name__ == '__main__':

    with mss.mss() as sct:

        yashaou  = YASHAOU('Left', 'Right', 'Up', 'Down', 'a', 's', 'd')
        config   = CONFIG()
        phash    = PHASH()
        
        while [ 1 ]:

            start_ts = time.time()
            
            config.compute()
            frame = config.render()

            if config.findmatch(frame, config.cont_t, 0.9):
                print '[Continue]'
                yashaou.cont()
            elif config.findmatch(frame, config.intro_t, 0.9):
                print '[Intro]'
                yashaou.intro()
            elif config.findmatch(frame, config.fight_t, 0.9):
                print '[Fight]'
            elif config.sumselect == config.select:
                print '[Select]'
                yashaou.select()
            else:

                fps = 1 / (time.time() - start_ts)
                delta = 1 / fps - (time.time() - start_ts)
                if delta > 0:
                    time.sleep(delta)

                print phash.compute(frame), 'fps:', fps, 'delta:', delta

                yashaou.act(numpy.random.randint(0,16))
