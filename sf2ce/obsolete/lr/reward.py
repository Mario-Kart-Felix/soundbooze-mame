# mame 800x600 +100+100

import cv2
import mss
import numpy
import time

def rewardPenalty(img, prevBlood):

    b = img[:, :, 0]
    g = img[:, :, 1]
    ssum = numpy.sum(b.ravel()) + numpy.sum(g.ravel())
    current = ((float(ssum)))
    sub = numpy.sqrt(prevBlood - current)/1000.0
    if current != prevBlood:
        return sub, current
    else:
        return 0, 0

def grab(width, height, left, top):

    with mss.mss() as sct:

        monitor = {"top": top, "left": left, "width": width, "height": height}

        prevBloodP1 = 0
        prevBloodP2 = 0

        startGame = False

        while [ 1 ]:

            p1 = numpy.array(sct.grab(monitor))
            p2 = p1.copy()

            b1 = p1[60:78, 68:364]
            b2 = p2[60:78, 68+366:364+366]
    
            sp1, curp1 = rewardPenalty(b1, prevBloodP1)
            sp2, curp2 = rewardPenalty(b2, prevBloodP2)

            sumb1 = numpy.sum(b1)
            sumb2 = numpy.sum(b2)

            if sumb1 >= 2744512 and sumb1 <= 4089536:

                if sumb1 == 4089536 and sumb2 == 4089536 and not startGame:
                    print '[Start]'
                    startGame = True
                    time.sleep(2)

                if sumb1 == 2744512:
                    print 'P1 [KO]'
                    startGame = False
                    time.sleep(6)
                elif sumb2 == 2744512:
                    print 'P2 [KO]'
                    startGame = False
                    time.sleep(6)

                if (sp1 != 0 and sp2 != 0):
                    if numpy.isnan(sp1):
                        sp1=0
                    if numpy.isnan(sp2):
                        sp2=0
                    print ("P1: %.5f"% (sp1)),
                    print ("P2: %.5f"% (sp2))

            prevBloodP1 = curp1
            prevBloodP2 = curp2

            '''    
            cv2.imshow("p1", b1)
            cv2.imshow("p2", b2)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            '''

border = 24
grab(800, 600-border, 100, 100+border)
