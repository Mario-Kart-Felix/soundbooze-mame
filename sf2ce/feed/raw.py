import time
import mss
import cv2
import numpy

from ryu import *

def act(ryu, r):

    if r == 0:
        ryu.fire(numpy.random.randint(0,2))

    elif r == 1:
        ryu.superpunch(numpy.random.randint(0,2))

    elif r == 2:
        ryu.superkick(numpy.random.randint(0,2))

    elif r == 3:
        z = numpy.random.randint(0,4)
        if z == 0:
            ryu.downkick()
        elif z == 1:
            ryu.kick()
            ryu.jumpup()
            ryu.kick()
        elif z == 2:
            ryu.jumpright(0.5)
            ryu.kick()
        elif z == 3:
            ryu.jumpleft(0.5)
            ryu.kick()

with mss.mss() as sct:

    ryu  = RYU('Left', 'Right', 'Up', 'Down', 'c', 'd')

    while [ 1 ]:

        act(ryu, numpy.random.randint(0,4))
        time.sleep(0.3)
