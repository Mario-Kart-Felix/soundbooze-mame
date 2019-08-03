import numpy
import cv2
import time
import mss
import sys
import random

from joblib import Parallel, delayed

from ryu import *

ROUND  = 2744512
START  = 4089536
INSERT = 1358640
SELECT = 2623509
KO     = 745816 * 4

class RingBuffer:

    def __init__(self, size):
        self.data = [None for i in xrange(size)]

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data

def loadTemplate(filename):
    return cv2.imread(filename)

def findMatch(background, template, threshold):
    result = cv2.matchTemplate(background,template,cv2.TM_CCOEFF_NORMED)
    loc = numpy.where(result >= threshold)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
    if len(loc[0]) > 1:
        return True

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

def lr_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = numpy.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
    fx, fy = flow[y,x].T
    l = len(fx[fx > 0])
    r = len(fx[fx < 0])
    if l > 80 or r > 80:
        return numpy.argmax([l, r])

def du_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = numpy.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
    fx, fy = flow[y,x].T
    u = len(fy[fy < 0])
    d = len(fy[fy > 0])
    if u > 80 or d > 80:
        return numpy.argmax([u, d])

def similar(img_a, img_b):
    from skimage.measure import compare_ssim
    sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
    return sim

ls = 0
def lastseen(frame, ryu_t):
    global ls
    p = Parallel(n_jobs=4)(delayed(findMatch)(frame,ryu_t[i], 0.8) for i in range(10))
    for i in p:
        if i:
            ls = time.time()
    return ls

with mss.mss() as sct:

    global ls

    monitor = {"top": 600, "left": 100, "width": 800, "height": 100}
    scene = {"top": 200, "left": 100, "width": 800, "height": 400}

    prev = numpy.array(sct.grab(monitor))
    prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    P = numpy.hsplit(prevgray, 2)
    prevgrayL = P[0]
    prevgrayR = P[1]

    v = []

    ryu = RYU('Left', 'Right', 'Up', 'Down', 'c', 'd')
    korb = RingBuffer(4)

    ryu_t = []
    for i in range(10):
        ryu_t.append(loadTemplate('template/'+ str(i+1) +'.png'))

    L = 0
    R = 0

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600-border}
    scene = {"top": 240+border, "left": 100, "width": 800, "height":480-border}

    prevBloodP1 = 0
    prevBloodP2 = 0

    startGame = False

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

            img = numpy.array(sct.grab(monitor))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            frame = numpy.array(sct.grab(scene))
            frame = frame[:,:,:3]
            grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            z = korb.get()
            zsum = 0
            try:
                zsum = numpy.sum(z)
            except:
                pass

            lastseen(numpy.hsplit(frame, 2)[0], ryu_t)
            dls = time.time() - ls
            print dls,
            if dls <= 6.0:
                L, R = 1, 0
            elif dls > 6.0:
                R, L = 1, 0

            C = numpy.hsplit(gray, 2)
            grayL = C[0]
            grayR = C[1]
            flowL = cv2.calcOpticalFlowFarneback(prevgrayL, grayL, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            flowR = cv2.calcOpticalFlowFarneback(prevgrayR, grayR, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            prevgrayL = grayL
            prevgrayR = grayR

            s = similar(cv2.resize(prevgray, (200, 100)), cv2.resize(gray, (200, 100)))
            if L and not R:
                ryu.fire(0)
            elif R and not L:
                ryu.superkick(1)

            l = lr_flow(grayL, flowL)
            r = lr_flow(grayR, flowR)

            if l is not None and r is not None:
                print l, r, l-r

                diff = l-r
                r = random.uniform(0,1)
                if r <= 0.25:
                    ryu.punch()
                elif r > 0.25 and r <= 0.5:
                    ryu.kick()
                elif r > 0.5 and r <= 0.75:
                    ryu.jumpup()
                    ryu.kick()
                elif r >  0.75:
                    ryu.downkick()

                if diff < 0:
                    if L and not R:
                        ryu.fire(0)
                    elif R and not L:
                        ryu.fire(1)

                elif diff > 0:
                    if L and not R:
                        ryu.superkick(0)
                    elif R and not L:
                        ryu.superkick(1)

            l = du_flow(grayL, flowL)
            r = du_flow(grayR, flowR)

            if l is not None and r is not None:
                print l, r, l-r

                v.append(l)
                v.append(r)
                if len(v) > 7:
                    if numpy.sum(v) > 7:
                        r = random.uniform(0,1)
                        if r <= 0.3:
                            if L and not R:
                                ryu.fire(0)
                            elif R and not L:
                                ryu.fire(1)
                        elif r > 0.3 and r <= 0.6:
                            if L and not R:
                                ryu.superpunch(0)
                            elif R and not L:
                                ryu.superpunch(1)
                        elif r > 0.6:
                            if L and not R:
                                ryu.superkick(0)
                            elif R and not L:
                                ryu.superkick(1)
                    v = []

            if sumb1 == START and sumb2 == START and not startGame:
                print '[Start]'
                startGame = True
                time.sleep(4)
                
            elif sumb1 == ROUND and zsum == KO:
                print 'P1 [KO]'
                startGame = False
                time.sleep(5)

            elif sumb2 == ROUND and zsum == KO:
                print 'P2 [KO]'
                startGame = False
                time.sleep(5)

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
