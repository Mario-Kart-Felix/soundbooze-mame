import time
import mss
import cv2
import numpy

from ryu import *

BLOOD      = [2744512, 4089536, 745816 * 4]
RESUME     = [1358640, 2617406, 2264400, 2623509]

def act(r):

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
            ryu.jumpright(0.3)
            ryu.kick()
        elif z == 3:
            ryu.jumpleft(0.3)
            ryu.kick()
    elif r == 4:
        z = numpy.random.randint(0,2)
        if z == 0:
            ryu.defendup(numpy.random.randint(0,2))
        elif z == 0:
            ryu.defenddown(numpy.random.randint(0,2))

with mss.mss() as sct:

    blood = {"top": 124, "left": 100, "width": 800, "height":600}
    scene = {"top": 264, "left": 100, "width": 800, "height":400}

    play = False

    ryu = RYU('Left', 'Right', 'Up', 'Down', 'c', 'd')

    while [ 1 ]:

        p1 = numpy.array(sct.grab(blood))
        p2 = p1.copy()

        b1 = p1[60:78, 68:364]
        b2 = p2[60:78, 68+366:364+366]
        ko = p1[60:80, 378:424]

        sumb1, sumb2, kosum = numpy.sum(b1), numpy.sum(b2), numpy.sum(ko)

        rbsum = 0
        try:
            rbsum = numpy.sum(rb.get())
        except:
            pass

        if sumb1 >= BLOOD[0] and sumb1 <= BLOOD[1]:

            if play:
                act(numpy.random.randint(0,5))
                time.sleep(0.11)
                
            if sumb1 == BLOOD[1] and sumb2 == BLOOD[1] and not play:
                print '[Start]'
                play = True
                time.sleep(1)

            elif sumb1 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P1 [KO]'
                hash.flush()
                play = False
                time.sleep(1)

            elif sumb2 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P2 [KO]'
                hash.flush()
                play = False
                time.sleep(1)

        elif sumb1 == RESUME[0]:
            ryu.insertcoin()
        
        elif sumb1 == RESUME[1] or sumb1 == RESUME[2] or sumb1 == RESUME[3]:
            ryu.select()
