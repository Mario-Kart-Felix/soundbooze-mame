import random
import numpy
import cv2
import time
import mss
import os

from skimage.measure import compare_ssim

INSERT = [1059132, 1055681]
SELECT = [831168, 764772]
INTRO  = [508206, 510494]
BLOOD  = [925269, 1434654]

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

def similar(img_a, img_b):
    img_a = cv2.cvtColor(cv2.resize(img_a, (200,100)), cv2.COLOR_BGR2GRAY)
    img_b = cv2.cvtColor(cv2.resize(img_b, (200,100)), cv2.COLOR_BGR2GRAY)
    sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
    return sim

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600-border}
    scene = {"top": 260+border, "left": 100, "width": 800, "height":424-border}

    prevBloodP1 = 0
    prevBloodP2 = 0

    startGame = False

    PENALTY = []
    frames = []
    i = 0

    os.mkdir('log')

    while [ 1 ]:

        last_time = time.time()
            
        frame = numpy.array(sct.grab(scene))
        frames.append(frame)

        p1 = numpy.array(sct.grab(blood))
        p2 = p1.copy()

        b1 = p1[48:56, 120:359]
        b2 = p2[48:56, 120+321:359+321]

        sp1, curp1 = reward_penalty(b1, prevBloodP1)
        sp2, curp2 = reward_penalty(b2, prevBloodP2)

        sumb1 = numpy.sum(b1)
        sumb2 = numpy.sum(b2)

        if startGame:

            print '[PENALTY]', len(PENALTY)

            if len(PENALTY) > 0:
                for p in PENALTY:
                    s = similar(frame, p)
                    if s > 0.6:
                        print s
                
        if sumb1 >= BLOOD[0] and sumb1 <= BLOOD[1]:

            if sumb1 == BLOOD[1] and sumb2 == BLOOD[1] and not startGame:
                print '[Start]'
                startGame = True
                time.sleep(1)

            elif sumb1 == BLOOD[0]:
                print 'P1 [KO]'
                startGame = False
                frames = []

                if len(PENALTY) > 0:
                    print '[Dump]'
                    for p in PENALTY:
                        cv2.imwrite('log/' + str(time.time()) + '.png', p)
                PENALTY = []

                time.sleep(1)

            elif sumb2 == BLOOD[0]:
                print 'P2 [KO]'
                startGame = False
                frames = []

                if len(PENALTY) > 0:
                    print '[Dump]'
                    for p in PENALTY:
                        cv2.imwrite('log/' + str(time.time()) + '.png', p)
                PENALTY = []

                time.sleep(1)

            elif (sp1 != 0 and sp2 != 0) and startGame:
                if numpy.isnan(sp1):
                    sp1 = 0
                if numpy.isnan(sp2):
                    sp2 = 0
                if sp1 > 0:
                    #print -1.0
                    fps = int(1 / (time.time() - last_time))
                    try:
                        PENALTY.append(frames[i - 6])
                        PENALTY.append(frames[i - fps])
                    except:
                        pass
                #elif sp2 > 0:
                    #print 1.0
                #else:
                    #print 0.0

            prevBloodP1 = curp1
            prevBloodP2 = curp2

            i += 1

            #print("fps: {}".format(1 / (time.time() - last_time)))
