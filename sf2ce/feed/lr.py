import os
import time
import mss
import cv2
import numpy
import pickle
import imagehash
from PIL import Image

from ring import *
from ryu import *

BLOOD      = [2744512, 4089536, 745816 * 4]
RESUME     = [1358640, 2617406, 2264400, 2623509]

class TRANSFORM:

    def __init__(self):
        self.b = None

    def blue(self, frame):
        self.b = frame.copy()
        self.b[:,:,1] = 0
        self.b[:,:,2] = 0
        self.b[self.b < 250] = 0
        return self.b

class HASH:

    def __init__(self):
        self.root       = str(time.time()) + '/'
        self.Z          = {}
        self.H          = {}
        self.action     = ['left', 'jumpleft|kick', 'kick|left|kick', 'defendup(0)', 'defenddown(0)', 'fire(0)', 'superpunch(0)', 'superkick(0)', 'punch', 'kick', 'downkick', 'kick|jumpup|kick', 'right', 'jumpright|kick', 'kick|right|kick', 'defendup(1)', 'defenddown(1)', 'fire(1)', 'superpunch(1)', 'superkick(1)']
        self.p          = numpy.random.rand(len(self.action))
        self.p         /= numpy.sum(self.p)
        self.shift      = 0
        self.prevhit    = [0, 0]
        self.currenthit = [0, 0]
        self.stack      = 4

    def next(self):
        return numpy.random.choice(len(self.p), 1, p=self.p)[0]

    def compute(self, frame):

        def _chop(H, s):
            chop = ''
            for h in range(0, s):
                chop += H[h]
            return chop

        phash = _chop(str(imagehash.phash(frame)), 8)
        return phash

    def append(self, h, r, hit):
        self.Z[h] = [r, hit]

    def flush(self):
        for k, v in self.Z.items():
            if numpy.sum(v[1]) == 0:
                del self.Z[k]

    def dump(self):
        fp = open(self.root + 'Z-' + str(time.time()) + '.pkl', 'wb')
        pickle.dump(self.Z, fp)
        fp.close()
    
        fp = open(self.root + 'H-' + str(time.time()) + '.pkl', 'wb')
        pickle.dump(self.H, fp)
        fp.close()

    def _logshift(self, x):

        def _logistic(x, beta, alpha):
            return 1.0 / (1.0 + numpy.exp(numpy.dot(beta, x) + alpha))

        S = [[-88, 10], [88, -10], [88, 0], [-88, 0]]

        prob = list(_logistic(self.p, S[x][0], S[x][1]))
        prob /= numpy.sum(prob)

        return prob

    def fill(self, timesteps, z):

        try:
            H = timesteps.get()
            for h in H:
                self.H[h] = self._logshift(z)
        except:
            pass

def preact(blue, ryu, hash, sumb1, sumb2, timesteps):

    h = hash.compute(blue)
    r = hash.next()

    if h in hash.Z:
        r = hash.Z[h][0]

    if h in hash.H:
        prob = hash.H[h]
        r = numpy.random.choice(len(prob), 1, p=prob)[0]
        print '*',

    hash.currenthit[0], hash.currenthit[1] = (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)

    hit = [0, 0]
    hit[0], hit[1] = hash.currenthit[0] - hash.prevhit[0], hash.currenthit[1] - hash.prevhit[1]
    hit[0], hit[1] =  -1 if hit[0] else 0, 1 if hit[1] else 0

    if hit[0] == -1:
        hash.shift = (hash.shift + 1) % 2
        hash.fill(timesteps, 1)
        #hash.p = shuffle(hash.p, 1)
    if hit[1] == 1:
        hash.shift = (hash.shift + 1) % 2
        hash.fill(timesteps, 0)
        #hash.p = shuffle(hash.p, 0)

    hash.append(h, r, hit)

    ryu.act(r)

    for i in range(2):
        hash.prevhit[i] = hash.currenthit[i]

    print("(%d/%d) - [%s] %s (%s) [%d]" %(len(hash.H), len(hash.Z), h, hash.Z[h], hash.action[r], hash.shift))

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600}
    scene = {"top": 240+border, "left": 100, "width": 800, "height":400}

    startGame = False

    ryu         = RYU('Left', 'Right', 'Up', 'Down', 'c', 'd')
    rb          = RINGBUFFER(4)
    transform   = TRANSFORM()
    hash        = HASH()
    timesteps   = RINGBUFFER(8)

    prev_timestep = Image.fromarray(transform.blue(cv2.resize(numpy.array(sct.grab(scene)),(200,100))))
    for i in range(8):
        timesteps.append(hash.compute(prev_timestep))

    i = 0

    while [ 1 ]:

        p1 = numpy.array(sct.grab(blood))
        p2 = p1.copy()

        b1 = p1[60:78, 68:364]
        b2 = p2[60:78, 68+366:364+366]
        ko = p1[60:80, 378:424]

        sumb1, sumb2, kosum = numpy.sum(b1), numpy.sum(b2), numpy.sum(ko)

        rbsum = 0
        try:
            rbsum = numpy.sum(rb.get())
        except:
            pass

        if sumb1 >= BLOOD[0] and sumb1 <= BLOOD[1]:

            if startGame:
                x = cv2.resize(numpy.array(sct.grab(scene)),(200,100))
                blue = transform.blue(x)
                if i % hash.stack == 0:
                    timesteps.append(hash.compute(Image.fromarray(transform.blue(cv2.resize(numpy.array(sct.grab(scene)),(200,100))))))
                preact(Image.fromarray(blue), ryu, hash, sumb1, sumb2, timesteps)
                
            if sumb1 == BLOOD[1] and sumb2 == BLOOD[1] and not startGame:
                print '[Start]'
                startGame = True
                time.sleep(1)

            elif sumb1 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P1 [KO]'
                hash.flush()
                startGame = False
                time.sleep(1)

            elif sumb2 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P2 [KO]'
                hash.flush()
                startGame = False
                time.sleep(1)

        elif sumb1 == RESUME[0]:
            ryu.insertcoin()
        
        elif sumb1 == RESUME[1] or sumb1 == RESUME[2] or sumb1 == RESUME[3]:
            ryu.select()

        i += 1
