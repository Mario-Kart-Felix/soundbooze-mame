import random
import numpy
import cv2
import time
import mss
import hashlib 
import pickle
import math
from PIL import Image, ImageChops

from ryu import *
from rb import *
from archive import *

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

def pil_similar(img_a, img_b):
    a = Image.fromarray(img_a.reshape(50,100))
    b = Image.fromarray(img_b.reshape(50,100))
    diff = ImageChops.difference(a, b) # pip install Pillow-SIMD
    h = diff.histogram()
    sq = (value*((idx%256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(a.size[0] * a.size[1]))
    return rms

def maxsimilarity(A, x): 
    ms = 0
    t1 = time.time()
    img = None
    for a in A:
        for i in a:
            s = pil_similar(x, i)
            if s > ms:
                ms = s
                img = i
    return ms, time.time() - t1, hash(img)

def hash(frame):
    result = hashlib.md5(str(frame.ravel()).encode()) 
    return result.hexdigest()

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600-border}
    scene = {"top": 240+border, "left": 100, "width": 800, "height":480-border}

    prevBloodP1 = 0
    prevBloodP2 = 0

    startGame = False

    ryu = RYU()
    korb = RingBuffer(4)
    archive = Archive()

    rewards = 0
    PENALTY = []
    REWARD = []
    TotalPenalty, TotalReward = 0, 0

    HP = {}
    HR = {}

    ZEQ = []

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

            if startGame:

                x = cv2.resize(numpy.array(sct.grab(scene))[:,:,0],(100,50)).ravel()

                if len(PENALTY) > 0:
                    msp, t, ip = maxsimilarity(PENALTY, x) 
                    rp = random.randint(0,7)
                    HP[ip] = rp

                if len(REWARD) > 0:
                    msr, t, ir = maxsimilarity(REWARD, x) 
                    rr = random.randint(0,8)
                    HR[ir] = rr 

                if msp > msr:
                    #print '[P]', msp, t, ip, rp, sumb1/10000000.0, sumb2/10000000.0
                    #print '[P]', msp, t, ip, rp, sumb1/10000000.0 - ROUND/10000000.0, sumb2/10000000.0 - ROUND/10000000.0
                    #print '[P]', msp, t, ip, rp, (0.8654976000000001 + sumb1/10000000.0) - ROUND/10000000.0, (0.8654976000000001+sumb2/10000000.0) - ROUND/10000000.0
                    print '[P]', msp, t, ip, rp, 0.4089536-sumb1/10000000.0, 0.4089536-sumb2/10000000.0
                    z = ['P', ip, rp, 0.4089536-sumb2/10000000.0]
                    ZEQ.append(z)
                    r = HP[ip]
                    if r == 0:
                        ryu.jumpleft()
                        ryu.kick()
                    elif r == 1:
                        ryu.jumpright()
                        ryu.kick()
                    elif r == 2:
                        ryu.left()
                    elif r == 3:
                        ryu.right()
                    elif r == 4:
                        ryu.defenddown(0)
                    elif r == 5:
                        ryu.defenddown(1)
                    elif r == 6:
                        ryu.defendup(0)
                    elif r == 7:
                        ryu.defendup(1)

                elif msp < msr: 
                    #print '[R]', msr, t, ir, rr, sumb1/10000000.0, sumb2/10000000.0
                    #print '[R]', msr, t, ir, rr, sumb1/10000000.0 - ROUND/10000000.0, sumb2/10000000.0 - ROUND/10000000.0
                    #print '[R]', msr, t, ir, rr, (0.8654976000000001 + sumb1/10000000.0) - ROUND/10000000.0, (0.8654976000000001 + sumb2/10000000.0) - ROUND/10000000.0
                    print '[R]', msr, t, ir, rr, 0.4089536-sumb1/10000000.0, 0.4089536-sumb2/10000000.0
                    z = ['R', ir, rr, 0.4089536-sumb2/10000000.0]
                    ZEQ.append(z)
                    r = HR[ir]
                    if r == 0:
                        ryu.punch()
                    elif r == 1:
                        ryu.kick()
                    elif r == 2:
                        ryu.downkick()
                    elif r == 3:
                        ryu.fire(0)
                    elif r == 4:
                        ryu.fire(1)
                    elif r == 5:
                        ryu.superpunch(0)
                    elif r == 6:
                        ryu.superpunch(1)
                    elif r == 7:
                        ryu.superkick(0)
                    elif r == 8:
                        ryu.superkick(1)

            z = korb.get()
            zsum = 0
            try:
                zsum = numpy.sum(z)
            except:
                pass

            if sumb1 == START and sumb2 == START and not startGame:
                print '[Start]'
                startGame = True
                TotalPenalty, TotalReward = archive.load(numpy.array(sct.grab(scene))[:,:,0])
                PENALTY, REWARD = archive.P, archive.R
                print '[PENALTY]:', len(PENALTY), '('+str(TotalPenalty)+')'
                print '[REWARD]:', len(REWARD),   '('+str(TotalReward)+')'
                rewards = 0
                time.sleep(1)

            elif sumb1 == ROUND and zsum == KO:
                print 'P1 [KO]'
                startGame = False
                print '[-]-----------'
                print len(ZEQ)
                print numpy.array(ZEQ).ravel()
                print ZEQ
                print '[-]-----------'
                ZEQ = []

                time.sleep(1)

            elif sumb2 == ROUND and zsum == KO:
                print 'P2 [KO]'
                startGame = False
                print '[-]-----------'
                print len(ZEQ)
                print numpy.array(ZEQ).ravel()
                print ZEQ
                print '[-]-----------'
                ZEQ = []

                print ''
                print HP
                print HR
                print ''
                time.sleep(1)

            elif (sp1 != 0 and sp2 != 0):
                if numpy.isnan(sp1):
                    sp1 = 0
                if numpy.isnan(sp2):
                    sp2 = 0
                if sp1 > 0:
                    rewards += -1.0
                elif sp2 > 0:
                    rewards += 1.0
                else:
                    rewards += 0

            prevBloodP1 = curp1
            prevBloodP2 = curp2

        elif sumb1 == INSERT:  
            ryu.insertcoin()
        
        elif sumb1 == SELECT:
            ryu.select() 
