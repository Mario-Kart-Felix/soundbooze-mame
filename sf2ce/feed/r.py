import time
import mss
import cv2
import numpy

from ryu import *
from ring import *

BLOOD      = [2744512, 4089536, 745816 * 4]
RESUME     = [1358640, 2617406, 2264400, 2623509]

def act(hi, mid, lo, r):

    if r == 0:
        z = numpy.random.randint(0,3)
        if z == 0:
            lo.fire(numpy.random.randint(0,2))
        elif z == 1:
            mid.fire(numpy.random.randint(0,2))
        elif z == 2:
            hi.fire(numpy.random.randint(0,2))

    elif r == 1:
        z = numpy.random.randint(0,3)
        if z == 0:
            lo.superpunch(numpy.random.randint(0,2))
        elif z == 1:
            mid.superpunch(numpy.random.randint(0,2))
        elif z == 2:
            hi.superpunch(numpy.random.randint(0,2))

    elif r == 2:
        z = numpy.random.randint(0,3)
        if z == 0:
            lo.superkick(numpy.random.randint(0,2))
        elif z == 2:
            mid.superkick(numpy.random.randint(0,2))
        elif z == 3:
            hi.superkick(numpy.random.randint(0,2))

    elif r == 3:
        z = numpy.random.randint(0,4)
        if z == 0:
            hi.downkick()
        elif z == 1:
            hi.kick()
            hi.jumpup()
            hi.kick()
        elif z == 2:
            hi.jumpright(numpy.random.uniform(low=0.3, high=0.5))
            hi.kick()
        elif z == 3:
            hi.jumpleft(numpy.random.uniform(low=0.3, high=0.5))
            hi.kick()

    elif r == 4:
        z = numpy.random.randint(0,2)
        if z == 0:
            hi.defendup(numpy.random.randint(0,2))
        elif z == 0:
            hi.defenddown(numpy.random.randint(0,2))

with mss.mss() as sct:

    blood = {"top": 124, "left": 100, "width": 800, "height":600}
    scene = {"top": 264, "left": 100, "width": 800, "height":400}

    play = False

    hi  = RYU('Left', 'Right', 'Up', 'Down', 'c', 'd')
    mid = RYU('Left', 'Right', 'Up', 'Down', 'x', 's')
    lo  = RYU('Left', 'Right', 'Up', 'Down', 'z', 'a')

    rb  = RINGBUFFER(4)

    while [ 1 ]:

        p1 = numpy.array(sct.grab(blood))
        p2 = p1.copy()

        b1 = p1[60:78, 68:364]
        b2 = p2[60:78, 68+366:364+366]
        ko = p1[60:80, 378:424]

        sumb1, sumb2, kosum = numpy.sum(b1), numpy.sum(b2), numpy.sum(ko)
        rb.append(kosum)

        rbsum = 0
        try:
            rbsum = numpy.sum(rb.get())
        except:
            pass

        if sumb1 >= BLOOD[0] and sumb1 <= BLOOD[1]:

            if play:
                act(hi, mid, lo, numpy.random.randint(0,5))
                time.sleep(numpy.random.uniform(low=0.05, high=0.2))
                
            if sumb1 == BLOOD[1] and sumb2 == BLOOD[1] and not play:
                print '[Start]'
                play = True
                time.sleep(1)

            elif sumb1 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P1 [KO]'
                play = False
                time.sleep(1)

            elif sumb2 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P2 [KO]'
                play = False
                time.sleep(1)

        elif sumb1 == RESUME[0]:
            hi.insertcoin()
        
        elif sumb1 == RESUME[1] or sumb1 == RESUME[2] or sumb1 == RESUME[3]:
            hi.select()
