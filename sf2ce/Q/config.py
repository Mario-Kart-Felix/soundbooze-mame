import numpy
from ring import *

class CONFIG:

    def __init__(self):
        self.BLOOD  = [2744512, 4089536, 745816 * 4]
        self.RESUME = [1358640, 2617406, 2264400]
        self.blood  = {"top": 100+24, "left": 100, "width": 800, "height":600}
        self.scene  = {"top": 240+24, "left": 100, "width": 800, "height":400}
        self.sumb1  = 0
        self.sumb2  = 0
        self.play   = False
        self.rb     = RINGBUFFER(4)

    def sum(self, sct):
        h = numpy.array(sct.grab(self.blood))
        b1 = h[60:78, 68:364]
        b2 = h[60:78, 68+366:364+366]
        ko = h[60:80, 378:424]
        kosum = numpy.sum(ko)
        self.rb.append(kosum)
        self.sumb1, self.sumb2 = numpy.sum(b1), numpy.sum(b2)
