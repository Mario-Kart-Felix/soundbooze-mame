import random
import numpy
import cv2
import time
import mss
import math
from hmmlearn import hmm
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
    for a in A:
        for i in a:
            s = pil_similar(x, i)
            if s > ms:
                ms = s
    return ms, time.time() - t1

def hmmmat():

    def _rndsumone(n):
        R = []
        while (numpy.sum(R)) != 1.0:
            R = numpy.random.multinomial(100.0, numpy.ones(n)/n, size=1)[0]/100.0
        return R

    HMMP = hmm.GaussianHMM(n_components=2, covariance_type="full")
    sp = _rndsumone(2)
    HMMP.startprob_ = numpy.array(sp)
    a, b = _rndsumone(2), _rndsumone(2)
    print '[HMM P]'
    print sp
    print a
    print b
    HMMP.transmat_ = numpy.array([a, b])
    HMMP.means_ = numpy.array([[0.2, 0.8], [0.3, 0.2]])
    HMMP.covars_ = numpy.tile(numpy.identity(2), (9, 1, 1))

    HMMR = hmm.GaussianHMM(n_components=3, covariance_type="full")
    sp = _rndsumone(3)
    HMMR.startprob_ = numpy.array(sp)
    a, b, c = _rndsumone(3), _rndsumone(3), _rndsumone(3)
    print '[HMM R]'
    print sp
    print a
    print b
    print c
    HMMR.transmat_ = numpy.array([a, b, c])
    HMMR.means_ = numpy.array([[0.2, 0.8], [0.3, 0.2], [0.4, 0.6]])
    HMMR.covars_ = numpy.tile(numpy.identity(2), (9, 1, 1))

    '''
    with open("hmm.pkl", "wb") as file: 
        pickle.dump(model, file)

    with open("hmm.pkl", "rb") as file: 
        HMM = pickle.load(file)
        _, Z = HMM.sample(10)
        print Z
    '''

    return HMMP, HMMR

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

    HMMP, HMMR = hmmmat()
    
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

                print '[PENALTY]:', len(PENALTY), '('+str(TotalPenalty)+')'
                print '[REWARD]:', len(REWARD),   '('+str(TotalReward)+')'

                if len(PENALTY) > 0:
                    msp, t = maxsimilarity(PENALTY, x) 
                    if msp > 73:
                        _, Z = HMMP.sample(1)
                        r = Z[0]
                        if r == 0:
                            ryu.superkick(0)
                            ryu.superkick(1)
                        elif r == 1:
                            ryu.superpunch(0)
                            ryu.superpunch(1)
                        print '[P]', msp, t

                if len(REWARD) > 0:
                    msr, t = maxsimilarity(REWARD, x) 
                    if msr > 73:
                        _, Z = HMMR.sample(1)
                        r = Z[0]
                        if r == 0:
                            for i in range(2):
                                ryu.superkick(0)
                                ryu.superkick(1)
                        elif r == 1:
                            for i in range(2):
                                ryu.superpunch(0)   
                                ryu.superpunch(1)   
                        elif r == 2:
                            for i in range(2):
                                ryu.fire(0)
                                ryu.fire(1)
                        print '[R]', msr, t

                action = random.randint(0,9)
                if action == 0:
                    ryu.left()
                elif action == 1:
                    ryu.right()
                elif action == 2:
                    ryu.jumpleft(0.6)
                    ryu.kick()
                elif action == 3:
                    ryu.jumpright(0.6)
                    ryu.kick()
                elif action == 4:
                    ryu.jumpup()
                    ryu.kick()
                elif action == 5:
                    ryu.defenddown(0)
                elif action == 6:
                    ryu.defendup(0)
                elif action == 7:
                    ryu.defenddown(1)
                elif action == 8:
                    ryu.defendup(1)
                elif action == 9:
                    ryu.downkick()

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
                rewards = 0
                time.sleep(1)

            elif sumb1 == ROUND and zsum == KO:
                print 'P1 [KO]'
                startGame = False
                HMMP, HMMR = hmmmat()
                time.sleep(1)

            elif sumb2 == ROUND and zsum == KO:
                print 'P2 [KO]'
                startGame = False
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

                print '[Rewards]', rewards

            prevBloodP1 = curp1
            prevBloodP2 = curp2

        elif sumb1 == INSERT:  
            ryu.insertcoin()
        
        elif sumb1 == SELECT:
            ryu.select() 
