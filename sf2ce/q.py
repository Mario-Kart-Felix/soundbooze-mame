import os
import time
import mss
import cv2
import numpy
import pickle
import imagehash
from PIL import Image

from ryu import *

BLOOD  = [2744512, 4089536, 745816 * 4]
RESUME = [1358640, 2623509]

class RINGBUFFER:

    def __init__(self, size):
        self.data = [None for i in xrange(size)]

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data

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
        self.root = str(time.time()) + '/'
        self.Z = {}
        self.action = ['punch', 'kick', 'downkick', 'kick|right|kick', 'kick|jumpup|kick', 'jumpleft|kick', 'jumpright|kick', 'fire(0)', 'fire(1)', 'superpunch(0)', 'superpunch(1)', 'superkick(0)', 'superkick(1)', 'defendup(0)', 'defendup(1)', 'defenddown(0)', 'defenddown(1)'] 
        self.p = [1.0-(0.058*16), 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058]
        self.prevhit    = [0, 0]
        self.currenthit = [0, 0]
        self.i = 0

    def next(self):
        return numpy.random.choice(len(self.p), 1, p=self.p)[0]

    def compute(self, frame):
        phash = imagehash.phash(frame)
        return phash

    def append(self, h, r, hit):
        if h in self.Z:
            i = self.Z[h][2]
            self.Z[h] = [r, hit, i]
        else:
            self.Z[h] = [r, hit, self.i]
            self.i += 1

    def dump(self):
        pickle.dump(self.Z, open(self.root + 'hash-' + str(time.time()) + '.pkl', 'wb'))

class Q:

    def __init__(self, Z, p):
        self.l  = len(Z)
        self.Q = numpy.zeros([len(Z), len(p)])
        self.lr = .85
        self.y  = .99

    def stack(self, Z, p):
        l = len(Z)
        for i in range(self.l, l):
            self.Q = numpy.vstack((self.Q, numpy.zeros(len(p))))
        self.l = l

    def act(self, current, p):
        try:
            return numpy.argmax(self.Q[current,:]) + numpy.random.choice(len(p), 1, p=p)[0]
        except:
            return numpy.random.choice(len(p), 1, p=p)[0]

    def update(self, prev, a, current, hit):
        try:
            self.Q[prev,a] = self.Q[prev,a] + self.lr * (numpy.sum(hit) + self.y * numpy.max(self.Q[current,:]) - self.Q[prev,a])
        except:
            pass

    def save(self):
        root = '/tmp/'
        numpy.save(root + 'bison.q', self.Q)

def act(r):

    if r == 0:
      ryu.punch()
    elif r == 1:
      ryu.kick()
    elif r == 2:
      ryu.downkick()
    elif r == 3:
      ryu.kick()
      ryu.right()
      ryu.kick()
    elif r == 4:
      ryu.kick()
      ryu.jumpup()
      ryu.kick()
    elif r == 5:
      ryu.jumpleft(0.6)
      ryu.kick()
    elif r == 6:
      ryu.jumpright(0.6)
      ryu.kick()
    elif r == 7:
      ryu.fire(0)
    elif r == 8:
      ryu.fire(1)
    elif r == 9:
      ryu.superpunch(0)
    elif r == 10:
      ryu.superpunch(1)
    elif r == 11:
      ryu.superkick(0)
    elif r == 12:
      ryu.superkick(1)
    elif r == 13:
      ryu.defendup(0)
    elif r == 14:
      ryu.defendup(1)
    elif r == 15:
      ryu.defenddown(0)
    elif r == 16:
      ryu.defenddown(1)

def preact(light, blue, ryu, hash, sumb1, sumb2, q):

    hprev = hash.compute(light)
    hcurr = hash.compute(blue)

    r = hash.next()
    if hcurr in hash.Z:
        r = hash.Z[hcurr][0]
    
    hash.currenthit[0], hash.currenthit[1] = (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)

    hit = [0, 0]
    hit[0], hit[1] = hash.currenthit[0] - hash.prevhit[0], hash.currenthit[1] - hash.prevhit[1]
    hit[0], hit[1] =  -1 if hit[0] else 0, 1 if hit[1] else 0

    hash.append(hcurr, r, hit)

    q.stack(hash.Z, hash.p)
    r = q.act(hash.Z[hcurr][2], hash.p)
    try:
        q.update(hash.Z[hprev][2], r, hash.Z[hcurr][2], hit)
    except:
        pass

    act(r)

    for i in range(2):
        hash.prevhit[i] = hash.currenthit[i]

    print("Q[%d] Z[%d] - [%s] %s (%s)" %(len(q.Q), len(hash.Z), hcurr, hash.Z[hcurr], hash.action[r]))

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600}
    scene = {"top": 240+border, "left": 100, "width": 800, "height":400}

    startGame = False

    ryu       = RYU()
    transform = TRANSFORM()
    hash      = HASH()
    rb        = RINGBUFFER(4)
    q         = Q(hash.Z, hash.p)

    light = transform.blue(cv2.resize(numpy.array(sct.grab(scene)),(200,100)))

    while [ 1 ]:

        p1 = numpy.array(sct.grab(blood))
        p2 = p1.copy()

        b1 = p1[60:78, 68:364]
        b2 = p2[60:78, 68+366:364+366]
        ko = p1[60:80, 378:424]

        sumb1, sumb2, kosum = numpy.sum(b1), numpy.sum(b2), numpy.sum(ko)
        rb.append(kosum)

        if sumb1 >= BLOOD[0] and sumb1 <= BLOOD[1]:

            if startGame:
                blue = transform.blue(cv2.resize(numpy.array(sct.grab(scene)),(200,100)))
                preact(Image.fromarray(light), Image.fromarray(blue), ryu, hash, sumb1, sumb2, q)

                R = rb.get()
                rbsum = 0
                try:
                    rbsum = numpy.sum(R)
                except:
                    pass
                    
                light = blue

            if sumb1 == BLOOD[1] and sumb2 == BLOOD[1] and not startGame:
                print '[Start]'
                startGame = True
                time.sleep(1)

            elif sumb1 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P1 [KO]'
                if startGame:
                    q.save()
                startGame = False
                time.sleep(1)

            elif sumb2 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P2 [KO]'
                if startGame:
                    q.save()
                startGame = False
                time.sleep(1)

        elif sumb1 == RESUME[0]:
            ryu.insertcoin()
        
        elif sumb1 == RESUME[1]:
            ryu.select()
