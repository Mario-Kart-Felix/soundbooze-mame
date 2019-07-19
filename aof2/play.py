import numpy
import time
import cv2
import mss
import multiprocessing

import PIL
import imagehash

from q import *
from ring import *
from robert import *
from transform import *

class HASH:

    def __init__(self):
        self.H     = {}
        self.depth = 12

    def chop(self, H, s):
        chop = ''
        for h in range(0, s):
            chop += H[h]
        return chop

    def compute(self, frame):
        phash = self.chop(str(imagehash.phash(PIL.Image.fromarray(frame))), self.depth)
        return phash

class ACT:

    def __init__(self):
        self.robert = ROBERT('Left', 'Right', 'Up', 'Down', 'a', 's', 'z')
        self.action = ['shift(0)','ryugekiken(0)','ryuuga(0)','kyokugenryuurenbuken(0)','hienshippuukyaku(0)','geneikyaku(0)','haohshoukohken(0)','left()','hienryuujinkyaku(0)','defendup(0)','defenddown(0)','punch()','kick()','downpunch()','downkick()','recharge()','shift(1)','ryugekiken(1)','ryuuga(1)','kyokugenryuurenbuken(1)','hienshippuukyaku(1)','geneikyaku(1)','haohshoukohken(1)','right()','hienryuujinkyaku(1)','defendup(1)','defenddown(1)']

    def act(self, r, ev, ns):

        def _run(r):
            ns.value = True
            ev.set()

            if r == 0:
                act.robert.shift(0)
            elif r == 1:
                act.robert.ryugekiken(0)
            elif r == 2:
                act.robert.ryuuga(0)
            elif r == 3:
                act.robert.kyokugenryuurenbuken(0)
            elif r == 4:
                act.robert.hienshippuukyaku(0)
            elif r == 5:
                act.robert.geneikyaku(0)
            elif r == 6:
                act.robert.haohshoukohken(0)
            elif r == 7:
                act.robert.hienryuujinkyaku(0.2, 0)
            elif r == 8:
                act.robert.left(0.1)
            elif r == 9:
                act.robert.defendup(0, 0.1)
            elif r == 10:
                act.robert.defenddown(0, 0.1)

            elif r == 11:
                act.robert.punch()
            elif r == 12:
                act.robert.kick()
            elif r == 13:
                act.robert.downpunch()
            elif r == 14:
                act.robert.downkick()
            elif r == 15:
                act.robert.recharge(0.3)

            elif r == 16:
                act.robert.shift(1)
            elif r == 17:
                act.robert.ryugekiken(1)
            elif r == 18:
                act.robert.ryuuga(1)
            elif r == 19:
                act.robert.kyokugenryuurenbuken(1)
            elif r == 20:
                act.robert.hienshippuukyaku(1)
            elif r == 21:
                act.robert.geneikyaku(1)
            elif r == 22:
                act.robert.haohshoukohken(1)
            elif r == 23:
                act.robert.hienryuujinkyaku(0.2, 1)
            elif r == 24:
                act.robert.right(0.1)
            elif r == 25:
                act.robert.defendup(1, 0.1)
            elif r == 26:
                act.robert.defenddown(1, 0.1)

            ns.value = False
            ev.set()

        z = False
        try:
            z = ns.value
            if not z:
                _run(r)

        except Exception, err:
            _run(r)
            pass

        ev.wait()

class CONFIG:

    def __init__(self):
        self.INSERT      = [0, 0]
        self.SELECT      = [221782, 268034]
        self.BLOOD       = [0, 2276752]
        self.blood       = {"top": 124, "left": 100, "width": 800, "height":100}
        self.scene       = {"top": 284, "left": 100, "width": 800, "height":400}
        self.play        = False
        self.prevBloodP1 = 0
        self.prevBloodP2 = 0

    def reward_penalty(self, img, prevBlood):
        ssum = numpy.sum(img.ravel())
        current = ((float(ssum)))
        sub = prevBlood - current
        if current != prevBlood:
            return sub, current
        else:
            return 0, 0

    def blood_count(self, blood):
        hsv = cv2.cvtColor(blood, cv2.COLOR_BGR2HSV)
        lower = numpy.array([0, 0, 255])
        upper = numpy.array([120, 255, 255]) 
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(blood,blood,mask=mask) 
        b1 = res[40:60, 0:366]
        b2 = res[40:60, 434:800]
        sp1, curp1 = self.reward_penalty(b1, self.prevBloodP1)
        sp2, curp2 = self.reward_penalty(b2, self.prevBloodP2)
        sumb1 = numpy.sum(b1)
        sumb2 = numpy.sum(b2)
        return sumb1, sumb2, curp1, curp2, sp1, sp2

    def blood_update(self):
        config.prevBloodP1 = curp1
        config.prevBloodP2 = curp2

if __name__ == '__main__':

    with mss.mss() as sct:

        act    = ACT()
        q      = Q(len(act.action))
        phash  = HASH()
        trans  = TRANSFORM()
        config = CONFIG()
        ring   = RINGBUFFER(16)

        while [ 1 ]:

            scene = numpy.array(sct.grab(config.scene))
            blood = numpy.array(sct.grab(config.blood))

            sumb1, sumb2, curp1, curp2, sp1, sp2 = config.blood_count(blood)

            mgr = multiprocessing.Manager()
            ns = mgr.Namespace()
            ev = multiprocessing.Event()

            if sumb1 >= config.BLOOD[0] and sumb1 <= config.BLOOD[1]:

                if config.play:

                    hred = phash.compute(trans.red(scene))
                    hred5 = phash.chop(hred, 5)
                    z = '*' if hred5 in q.HQ else ''
                    ring.append(hred5)
                    q.append(hred5)

                    a = q.act(hred5)
                    mp = multiprocessing.Process(target=act.act, args=(a, ev,ns)) 
                    mp.start() 
                    mp.join()
                    
                    hit = 0
                    if (sp1 != 0 and sp2 != 0):
                        if numpy.isnan(sp1):
                            sp1 = 0
                        if numpy.isnan(sp2):
                            sp2 = 0
                        if sp1 > 0:
                            hit = -1
                            R = ring.get()
                            for i in range(len(R)-1):
                                q.update(R[i], R[i+1], a, -1)
                        elif sp2 > 0:
                            hit = 1
                            R = ring.get()
                            for i in range(len(R)-1):
                                q.update(R[i], R[i+1], a, 1)
                        else:
                            hit = 0
                            R = ring.get()
                            for i in range(len(R)-1):
                                q.update(R[i], R[i+1], a, 0)

                    print '(', len(q.HQ), ')', z, '[', hred5, hred, ']', act.action[a], hit

                    config.blood_update()

                if sumb1 == config.BLOOD[1] and sumb2 == config.BLOOD[1] and not config.play:
                    print '[Start]'
                    config.play = True
                    time.sleep(1)

                elif sumb1 == config.BLOOD[0]:
                    print 'P1 [KO]'
                    config.play = False
                    time.sleep(1)

                elif sumb2 == config.BLOOD[0]:
                    print 'P2 [KO]'
                    config.play = False
                    time.sleep(1)

            if sumb1 == config.INSERT[0] and sumb2 == config.INSERT[1]:
                print '[Insert]'
                act.robert.insertcoin()

            elif sumb1 == config.SELECT[0] and sumb2 == config.SELECT[1]:
                print '[Select]'
                act.robert.select()    
