import numpy
import cv2
import time
import mss
import sys

from ryu import *
from rb import *

ROUND  = 2744512
START  = 4089536
INSERT = 1358640
SELECT = 2623509
KO     = 745816 * 4

def reward_penalty(img, prevBlood):
    b = img[:, :, 0]
    g = img[:, :, 1]
    ssum = numpy.sum(b.ravel()) + numpy.sum(g.ravel())
    current = ((float(ssum)))
    sub = numpy.sqrt(prevBlood - current)/1000.0
    if current != prevBlood:
        return sub, current
    else:
        return 0, 0

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600-border}
    scene = {"top": 240+border, "left": 100, "width": 800, "height":480-border}

    prevBloodP1 = 0
    prevBloodP2 = 0

    startGame = False

    ryu = RYU()
    korb = RingBuffer(4)

    while [ 1 ]:

        p1 = numpy.array(sct.grab(blood))
        p2 = p1.copy()

        b1 = p1[60:78, 68:364]
        b2 = p2[60:78, 68+366:364+366]
        ko = p1[60:80, 378:424]

        sp1, curp1 = reward_penalty(b1, prevBloodP1)
        sp2, curp2 = reward_penalty(b2, prevBloodP2)

        sumb1 = numpy.sum(b1)
        sumb2 = numpy.sum(b2)
        kosum = numpy.sum(ko)
        korb.append(kosum)

        if sumb1 >= ROUND and sumb1 <= START:

            frame = numpy.array(sct.grab(scene))

            z = korb.get()
            zsum = 0
            try:
                zsum = numpy.sum(z)
            except:
                pass

            if sumb1 == START and sumb2 == START and not startGame:
                print '[Start]'
                startGame = True
                time.sleep(4)

            elif sumb1 == ROUND and zsum == KO:
                print 'P1 [KO]'
                startGame = False
                time.sleep(8)

            elif sumb2 == ROUND and zsum == KO:
                print 'P2 [KO]'
                startGame = False
                time.sleep(8)

            elif (sp1 != 0 and sp2 != 0):
                if numpy.isnan(sp1):
                    sp1 = 0
                if numpy.isnan(sp2):
                    sp2 = 0
                if sp1 > 0:
                    print -1.0
                elif sp2 > 0:
                    print 1.0
                else:
                    print 0.0

            prevBloodP1 = curp1
            prevBloodP2 = curp2

        elif sumb1 == INSERT:  
            ryu.insertcoin()
        
        elif sumb1 == SELECT:
            ryu.select()    
