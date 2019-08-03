import random
import numpy
import cv2
import time
import mss
import sys
import pickle
import math
from PIL import Image, ImageChops

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
    sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
    return sim

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

def countPR(P, R):
    tp = 0
    if len(P) > 0:
        for p in P:
            tp += len(p)
    tr = 0
    if len(R) > 0:
        for r in R:
            tr += len(r)
    return tp, tr

def load(startFrame):

    E = ['balrog', 'bison', 'blanka', 'chunli', 'dhalsim', 'guile', 'honda', 'ken', 'ryu', 'sagat', 'vega', 'zangief']
    P, R, enemy = [], [], ''

    def _l(d):
        with open (d, 'rb') as fp:
            return pickle.load(fp)

    ms = 0
    for e in E:
        img = cv2.imread('pretrained/' + e + '/' + '1.png', 0)
        s = similar(cv2.resize(img, (200, 100)), cv2.resize(startFrame, (200, 100)))
        print '[eList]', e, s
        if s > ms:
            ms = s
            enemy = e

    print '[Found]', enemy, ms

    for dir_path, subdir_list, file_list in os.walk('pretrained/' + enemy + '/penalty'):
        for fname in file_list:
            full_path = os.path.join(dir_path, fname)
            r = _l(full_path)
            P.append(r)

    for dir_path, subdir_list, file_list in os.walk('pretrained/' + enemy + '/reward'):
        for fname in file_list:
            full_path = os.path.join(dir_path, fname)
            r = _l(full_path)
            R.append(r)

    return P, R

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600-border}
    scene = {"top": 240+border, "left": 100, "width": 800, "height":480-border}

    prevBloodP1 = 0
    prevBloodP2 = 0

    startGame = False

    korb = RingBuffer(4)

    rewards = 0
    PENALTY = []
    REWARD = []
    TotalPenalty, TotalReward = 0, 0

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
                    print '[P]', msp, t

                if len(REWARD) > 0:
                    msr, t = maxsimilarity(REWARD, x) 
                    print '[R]', msr, t

            z = korb.get()
            zsum = 0
            try:
                zsum = numpy.sum(z)
            except:
                pass

            if sumb1 == START and sumb2 == START and not startGame:
                print '[Start]'
                startGame = True
                PENALTY, REWARD = load(numpy.array(sct.grab(scene))[:,:,0])
                TotalPenalty, TotalReward = countPR(PENALTY, REWARD)
                rewards = 0
                time.sleep(1)

            elif sumb1 == ROUND and zsum == KO:
                print 'P1 [KO]'
                startGame = False
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
