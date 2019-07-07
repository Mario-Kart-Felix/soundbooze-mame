import numpy
from ring import *

class CONFIG:

    def __init__(self, root):
        self.BLOOD      = [2744512, 4089536, 745816 * 4]
        self.RESUME     = [1358640, 2617406, 2264400, 2623509]
        self.blood      = {"top": 100+24, "left": 100, "width": 800, "height":600}
        self.scene      = {"top": 240+24, "left": 100, "width": 800, "height":400}
        self.shape      = (200,100)
        self.sumb1      = 0
        self.sumb2      = 0
        self.prevhit    = [0, 0]
        self.currenthit = [0, 0]
        self.play       = False
        self.rb         = RINGBUFFER(4)
        self.root       = root + '/'

    def sum(self, sct):
        h = numpy.array(sct.grab(self.blood))
        b1 = h[60:78, 68:364]
        b2 = h[60:78, 68+366:364+366]
        ko = h[60:80, 378:424]
        kosum = numpy.sum(ko)
        self.rb.append(kosum)
        self.sumb1, self.sumb2 = numpy.sum(b1), numpy.sum(b2)

    def hitcount(self, sumb1, sumb2):
        self.currenthit[0], self.currenthit[1] = (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)
        hit = [0, 0]
        hit[0], hit[1] = self.currenthit[0] - self.prevhit[0], self.currenthit[1] - self.prevhit[1]
        hit[0], hit[1] =  -1 if hit[0] else 0, 1 if hit[1] else 0
        return hit

    def hitupdate(self):
        for i in range(2):
            self.prevhit[i] = self.currenthit[i]
