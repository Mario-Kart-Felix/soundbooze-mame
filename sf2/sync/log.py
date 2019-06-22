import random
import numpy
import cv2
import time
import mss
import sys
import pickle
import hashlib 

from ryu import *
from rb import *

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

def similar(img_a, img_b):
    from skimage.measure import compare_ssim
    sim, _ = compare_ssim(img_a, img_b, full=True)
    return sim

def clear(idx, states):
    idx = 0
    states = []

def save(path, PENALTY, REWARD):
    if len(PENALTY) > 0:
        with open(path + '/penalty/' + 'penalty-' + str(time.time()), 'wb') as fp:
            pickle.dump(PENALTY, fp)
    if len(REWARD) > 0:
        with open(path + '/reward/' + 'reward-' + str(time.time()), 'wb') as fp:
            pickle.dump(REWARD, fp)

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600-border}
    scene = {"top": 240+border, "left": 100, "width": 800, "height":480-border}

    prevBloodP1 = 0
    prevBloodP2 = 0

    startGame = False
    startFrame = None

    ryu = RYU()
    korb = RingBuffer(4)

    idx = 0
    states = []

    rewards = 0
    PENALTY = []
    REWARD = []

    path = ''

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

            x = cv2.resize(numpy.array(sct.grab(scene))[:,:,0],(100,50)).ravel()
            states.append(x)

            print '[PENALTY]:', len(PENALTY)
            print '[REWARD]:', len(REWARD)

            if len(PENALTY) > 0:
                for p in PENALTY:
                    s = similar(x, p)
                    if s > 0.88:
                        print '[P]', s

            if len(REWARD) > 0:
                for r in REWARD:
                    s = similar(x, r)
                    if s > 0.88:
                        print '[R]', s

            z = korb.get()
            zsum = 0
            try:
                zsum = numpy.sum(z)
            except:
                pass

            if sumb1 == START and sumb2 == START and not startGame:
                print '[Start]'
                startGame = True

                startFrame = numpy.array(sct.grab(scene))
                result = hashlib.md5(str(startFrame.ravel()).encode()) 
                path = 'pretrained/' + result.hexdigest()
                if not os.path.isdir(path):
                    os.mkdir(path, 0755)
                    os.mkdir(path + '/penalty') 
                    os.mkdir(path + '/reward') 
                    cv2.imwrite(path + '/' + '1.png', numpy.array(sct.grab(scene)))

                clear(idx, states)
                time.sleep(4)

            elif sumb1 == ROUND and zsum == KO:
                print 'P1 [KO]'
                startGame = False
                clear(idx, states)
                save(path, PENALTY, REWARD)
                PENALTY, REWARD = [], []
                time.sleep(8)

            elif sumb2 == ROUND and zsum == KO:
                print 'P2 [KO]'
                startGame = False
                clear(idx, states)
                save(path, PENALTY, REWARD)
                PENALTY, REWARD = [], []
                time.sleep(8)

            elif (sp1 != 0 and sp2 != 0):
                if numpy.isnan(sp1):
                    sp1 = 0
                if numpy.isnan(sp2):
                    sp2 = 0

                if sp1 > 0:
                    rewards += -1.0
                    PENALTY.append(states[idx-4])
                elif sp2 > 0:
                    rewards += 1.0
                    REWARD.append(states[idx-4])
                else:
                    rewards += 0

                print '[Rewards]', rewards

            prevBloodP1 = curp1
            prevBloodP2 = curp2

            idx += 1

        elif sumb1 == INSERT:  
            ryu.insertcoin()
        
        elif sumb1 == SELECT:
            ryu.select()    
