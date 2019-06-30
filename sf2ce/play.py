import mss
import cv2
import time
import numpy
import random
import hashlib 

from ryu import *
from rb import *
from archive import *

ROUND  = 2744512
START  = 4089536
INSERT = 1358640
SELECT = 2623509
KO     = 745816 * 4

class Image:

    def __init__(self, directory):
        self.directory = directory
        self.i = self.directory + '/i/'
        self.x = self.directory + '/x/'
        self.c = 0

    def dump(self, x, i):
        cv2.imwrite(self.i + str(c) + '.png', numpy.reshape(x, (50,100)))
        cv2.imwrite(self.x + str(c) + '.png', numpy.reshape(i, (50,100)))
        self.c += 1

    def hash(self, img):
        result = hashlib.md5(str(img.ravel()).encode()) 
        return result.hexdigest()

    def minsubtract(self, A, x): 

        def _graysub(img_a, img_b):
            diff = numpy.sum((img_a - img_b))/100000000.0
            return diff

        ms = numpy.iinfo('i').max
        t = time.time()
        img = None
        for a in A:
            for i in a:
                s = _graysub(x, i)
                if s < ms:
                    ms = s
                    img = i

        return ms, time.time() - t, self.hash(img)

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

    def _inference():

        if len(PENALTY) > 0:
            msp, t, ip = image.minsubtract(PENALTY, x) 
            rp = random.randint(0,7)
            HP[ip] = rp

        if len(REWARD) > 0:
            msr, t, ir = image.minsubtract(REWARD, x) 
            rr = random.randint(0,8)
            HR[ir] = rr 

        if msp < msr:
            print '[P]',
            print ("%.5f"% (msp)),
            print ("%.5f"% (t)),
            print ip, rp,
            print ("%.5f"% (0.4089536-sumb1/10000000.0)),
            print ("%.5f"% (0.4089536-sumb2/10000000.0))
            z = ['P', ip, rp, 0.4089536-sumb2/10000000.0]
            ZEQ.append(z)

        elif msp > msr: 
            print '[R]',
            print ("%.5f"% (msr)),
            print ("%.5f"% (t)),
            print ir, rr,
            print ("%.5f"% (0.4089536-sumb1/10000000.0)),
            print ("%.5f"% (0.4089536-sumb2/10000000.0))
            z = ['R', ir, rr, 0.4089536-sumb2/10000000.0]
            ZEQ.append(z)

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600}
    scene = {"top": 240+border, "left": 100, "width": 800, "height":480}

    prevBloodP1 = 0
    prevBloodP2 = 0

    startGame = False

    ryu = RYU()
    korb = RingBuffer(4)
    archive = Archive()
    image = Image('/tmp/')

    PENALTY = []
    REWARD = []

    rewards, TotalPenalty, TotalReward = 0, 0, 0

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
                _inference()
                
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
                '''
                print '[-]-----------'
                print len(ZEQ)
                print numpy.array(ZEQ).ravel()
                print ZEQ
                print '[-]-----------'
                ZEQ = []
                '''

                time.sleep(1)

            elif sumb2 == ROUND and zsum == KO:
                print 'P2 [KO]'
                startGame = False
                '''
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
                '''

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
