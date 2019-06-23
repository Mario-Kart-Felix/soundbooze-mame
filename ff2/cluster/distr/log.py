import numpy
import cv2
import time
import mss
import os

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

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600-border}
    scene = {"top": 260+border, "left": 100, "width": 800, "height":424-border}

    prevBloodP1 = 0
    prevBloodP2 = 0

    startGame = False

    frames = []
    i = 0

    nfsroot = "/nfs/"
    directory = nfsroot + str(time.time())
    os.mkdir(directory)
    os.mkdir(directory + '/penalty')

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

        if sumb1 >= BLOOD[0] and sumb1 <= BLOOD[1]:

            cv2.imwrite(directory + '/' + str(time.time()) + '.png', frame[i])

            if sumb1 == BLOOD[1] and sumb2 == BLOOD[1] and not startGame:
                print '[Start]'
                startGame = True
                time.sleep(1)

            elif sumb1 == BLOOD[0]:
                print 'P1 [KO]'
                startGame = False
                frames = []
                time.sleep(1)

            elif sumb2 == BLOOD[0]:
                print 'P2 [KO]'
                startGame = False
                frames = []
                time.sleep(1)

            elif (sp1 != 0 and sp2 != 0) and startGame:
                if numpy.isnan(sp1):
                    sp1 = 0
                if numpy.isnan(sp2):
                    sp2 = 0
                if sp1 > 0:
                    fps = int(1 / (time.time() - last_time))
                    try:
                        #cv2.imwrite(directory + '/penalty/' + str(time.time()) + '.png', frames[i-6])
                        #cv2.imwrite(directory + '/penalty/' + str(time.time()) + '.png', frames[i-fps])
                    except:
                        pass

                #elif sp2 > 0:
                    #print 1.0
                #else:
                    #print 0.0

            prevBloodP1 = curp1
            prevBloodP2 = curp2

        i += 1

        print("fps: {}".format(1 / (time.time() - last_time)))
