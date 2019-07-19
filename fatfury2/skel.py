import numpy
import time
import cv2
import mss
import multiprocessing

import PIL
import imagehash

from terry import *
from transform import *

class HASH:

    def __init__(self):
        self.H     = {}
        self.depth = 12

    def compute(self, frame):
        def _chop(H, s):
            chop = ''
            for h in range(0, s):
                chop += H[h]
            return chop
        phash = _chop(str(imagehash.phash(PIL.Image.fromarray(frame))), self.depth)
        return phash

class ACT:

    def __init__(self):
        self.terry = TERRY()
        self.action = ['powerwave(0)','burnknuckle(0)','risingtackle(0)','crackshoot(0)','left','jumpleft','defendup(0)','defenddown(0)','shift(0)','punch','kick','downpunch','downkick','powerwave(1)','burnknuckle(1)','risingtackle(1)','crackshoot(1)','right()','jumpright()','defendup(1)','defenddown(1)','shift(1)']
        self.prob   = numpy.random.rand(len(self.action))
        self.prob  /= numpy.sum(self.prob)
        self.shift  = 0

    def next(self):
        self.prob = numpy.random.rand(len(self.action))
        prob = numpy.zeros(len(self.action))
        if self.shift == 0:
            for i in range(len(self.action)/2):
                prob[i] += numpy.random.uniform() * self.prob[i]
        elif self.shift == 1:
            for i in range(len(self.action)/2, len(self.action)):
                prob[i] += numpy.random.uniform() * self.prob[i]
        prob /= numpy.sum(prob)
        return numpy.random.choice(len(prob), 1, p=prob)[0]

    def act(self, ev, ns):

        def _run():
            ns.value = True
            ev.set()

            r = self.next()

            if r == 0:
                self.terry.powerwave(0)
            elif r == 1:
                self.terry.burnknuckle(0)
            elif r == 2:
                self.terry.risingtackle(0)
            elif r == 3:
                self.terry.crackshoot(0)
            elif r == 4:
                self.terry.left(0.1)
            elif r == 5:
                self.terry.jumpleft(0.1)
            elif r == 6:
                self.terry.defendup(0.1, 0)
            elif r == 7:
                self.terry.defenddown(0.1, 0)
            elif r == 8:
                self.terry.shift(0)

            elif r == 9:
                self.terry.punch()
            elif r == 10:
                self.terry.kick()
            elif r == 11:
                self.terry.downpunch()
            elif r == 12:
                self.terry.downkick()

            elif r == 13:
                self.terry.powerwave(1)
            elif r == 14:
                self.terry.burnknuckle(1)
            elif r == 15:
                self.terry.risingtackle(1)
            elif r == 16:
                self.terry.crackshoot(1)
            elif r == 17:
                self.terry.right(0.1)
            elif r == 18:
                self.terry.jumpright(0.1)
            elif r == 19:
                self.terry.defendup(0.1, 1)
            elif r == 20:
                self.terry.defenddown(0.1, 1)
            elif r == 21:
                self.terry.shift(1)

            ns.value = False
            ev.set()

        z = False
        try:
            z = ns.value
            if not z:
                _run()

        except Exception, err:
            _run()
            pass

        ev.wait()

class CONFIG:

    def __init__(self):
        self.INSERT      = [1059132, 1055681]
        self.SELECT      = [831168, 764772]
        self.INTRO       = [508206, 510494]
        self.BLOOD       = [925269, 1434654]
        self.blood       = {"top": 124, "left": 100, "width": 800, "height":100}
        self.scene       = {"top": 284, "left": 100, "width": 800, "height":400}
        self.play        = False
        self.prevBloodP1 = 0
        self.prevBloodP2 = 0

    def reward_penalty(self, img, prevBlood):
        b = img[:, :, 0]
        g = img[:, :, 1]
        ssum = numpy.sum(b.ravel()) + numpy.sum(g.ravel())
        current = ((float(ssum)))
        sub = numpy.sqrt(prevBlood - current)/1000.0
        if current != prevBlood:
            return sub, current
        else:
            return 0, 0

    def blood_count(self, blood):
        b1 = blood[48:56, 120:359]
        b2 = blood[48:56, 120+321:359+321]
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
        phash  = HASH()
        trans  = TRANSFORM()
        config = CONFIG()

        while [ 1 ]:

            scene = numpy.array(sct.grab(config.scene))
            blood = numpy.array(sct.grab(config.blood))

            sumb1, sumb2, curp1, curp2, sp1, sp2 = config.blood_count(blood)

            mgr = multiprocessing.Manager()
            ns = mgr.Namespace()
            ev = multiprocessing.Event()

            if sumb1 >= config.BLOOD[0] and sumb1 <= config.BLOOD[1]:

                if config.play:

                    hblue = phash.compute(trans.blue(scene))

                    a = multiprocessing.Process(target=act.act, args=(ev,ns)) 
                    a.start() 
                    
                    if (sp1 != 0 and sp2 != 0):
                        if numpy.isnan(sp1):
                            sp1 = 0
                        if numpy.isnan(sp2):
                            sp2 = 0
                        if sp1 > 0:
                            act.shift = (act.shift + 1) % 2
                            print hblue, -1.0
                        elif sp2 > 0:
                            act.shift = (act.shift + 1) % 2
                            print hblue, 1.0
                        else:
                            print hblue, 0.0

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
                act.terry.insertcoin()
            elif sumb1 == config.SELECT[0] and sumb2 == config.SELECT[1]:
                print '[Select]'
                act.terry.select()    
            elif sumb1 == config.INTRO[0] and sumb2 == config.INTRO[1]:
                print '[Intro]'
                act.terry.intro()
