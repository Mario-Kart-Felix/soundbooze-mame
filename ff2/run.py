import multiprocessing 
import pickle
import numpy
import cv2
import time
import mss
import sys
import os

from sklearn.cluster import KMeans
from skimage.measure import compare_ssim

from terry import *

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
    t = time.time()
    img_a = cv2.cvtColor(cv2.resize(img_a, (200,100)), cv2.COLOR_BGR2GRAY)
    img_b = cv2.cvtColor(cv2.resize(img_b, (200,100)), cv2.COLOR_BGR2GRAY)
    sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
    return sim, time.time()-t

def act(r, ev, ns):

    def _run(r):
        ns.value = True
        ev.set()

        #todo [nglakoni]: auto seq.order(max) [dipikir]
        #berulang-ulang evolution-fulness -> win(mul.io)->(dump)
        #clustering-on-the-go / various.meth
        if r == 0:
            terry.shift(0)
            terry.shift(1)
            terry.superpunch(0)
            terry.superpunch(1)
        elif r == 1:
            terry.jumpright()
            terry.punch()
            terry.fire(0)
            terry.fire(1)
        elif r == 2:
            terry.kick()
            terry.jumpleft()
            terry.defenddown(0)
            terry.superkick(0)
            terry.superkick(1)
        elif r == 3:
            terry.kick()
            terry.punch()

        ns.value = False
        ev.set()

    z = False
    try:
        #print '[thread]', 'ret'
        z = ns.value
        if not z:
            #print '[thread]', 'run'
            _run(r)

    except Exception, err:
        _run(r)
        pass
    ev.wait()

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

    terry = TERRY()
    k = pickle.load(open(sys.argv[1], 'rb')) #kmeans dbscan/lr

    mgr = multiprocessing.Manager()
    ns = mgr.Namespace()
    ev = multiprocessing.Event()

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

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(gray, (200,100))
            img = numpy.array(img).ravel()

            t = time.time()
            r = k.predict([img])[0]
            print '[Cluster]', '[' + str(r) + ']',

            a = multiprocessing.Process(target=act, args=(r,ev,ns)) 
            a.start() 

            print time.time()-t

            print '[PENALTY]', len(PENALTY)
            if len(PENALTY) > 0:
                for p in PENALTY:
                    s, t = similar(frame, p)
                    if s > 0.0201: #dynamic threshold
                        print s, t
                        terry.shift(0)
                        terry.shift(1)

        if sumb1 >= BLOOD[0] and sumb1 <= BLOOD[1]:

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
                    print -1.0
                    fps = int(1 / (time.time() - last_time))
                    try:
                        PENALTY.append(frames[i - 6])
                        PENALTY.append(frames[i - fps])
                    except:
                        pass
                elif sp2 > 0:
                    print 1.0
                else:
                    print 0.0

            prevBloodP1 = curp1
            prevBloodP2 = curp2

            i += 1

            #print("fps: {}".format(1 / (time.time() - last_time)))

        if sumb1 == INSERT[0] and sumb2 == INSERT[1]:
            print '[Insert]'
            terry.insertcoin()
        elif sumb1 == SELECT[0] and sumb2 == SELECT[1]:
            print '[Select]'
            terry.select()    
        elif sumb1 == INTRO[0] and sumb2 == INTRO[1]:
            print '[Intro]'
            terry.intro()
