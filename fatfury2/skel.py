import numpy
import time
import cv2
import mss

from terry import *

class CONFIG:

    def __init__(self):

        self.INSERT = [1059132, 1055681]
        self.SELECT = [831168, 764772]
        self.INTRO  = [508206, 510494]
        self.BLOOD  = [925269, 1434654]

        self.blood  = {"top": 124, "left": 100, "width": 800, "height":600}
        self.scene  = {"top": 284, "left": 100, "width": 800, "height":400}
        self.play   = False

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

with mss.mss() as sct:

    terry = TERRY()
    config = CONFIG()

    while [ 1 ]:

        scene = numpy.array(sct.grab(config.scene))
        blood = numpy.array(sct.grab(config.blood))

        sumb1, sumb2, curp1, curp2, sp1, sp2 = config.blood_count(blood)

        if sumb1 >= config.BLOOD[0] and sumb1 <= config.BLOOD[1]:

            if config.play:

                r = numpy.random.randint(0,12)
                if r == 0:
                    terry.powerwave(0)
                elif r == 1:
                    terry.burnknuckle(0)
                elif r == 2:
                    terry.risingtackle(0)
                elif r == 3:
                    terry.crackshoot(0)
                elif r == 4:
                    terry.left(0.4)
                elif r == 5:
                    terry.jumpleft(0.4)
                elif r == 5:
                    terry.defendup(0.4, 0)
                elif r == 6:
                    terry.defenddown(0.4, 0)

                elif r == 7:
                    terry.punch()
                elif r == 8:
                    terry.kick()
                elif r == 9:
                    terry.downpunch()
                elif r == 10:
                    terry.downkick()

                elif r == 11:
                    terry.powerwave(1)
                elif r == 12:
                    terry.burnknuckle(1)
                elif r == 13:
                    terry.risingtackle(1)
                elif r == 14:
                    terry.crackshoot(1)
                elif r == 15:
                    terry.right(0.4)
                elif r == 16:
                    terry.jumpright(0.4)
                elif r == 17:
                    terry.defendup(0.4, 1)
                elif r == 18:
                    terry.defenddown(0.4, 1)

                if (sp1 != 0 and sp2 != 0):
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

                config.prevBloodP1 = curp1
                config.prevBloodP2 = curp2

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
            terry.insertcoin()
        elif sumb1 == config.SELECT[0] and sumb2 == config.SELECT[1]:
            print '[Select]'
            terry.select()    
        elif sumb1 == config.INTRO[0] and sumb2 == config.INTRO[1]:
            print '[Intro]'
            terry.intro()
