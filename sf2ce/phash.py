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
        self.action = ['punch', 'kick', 'downkick', 'kick|right|kick', 'kick|jumpup|kick', 'jumpleft|kick', 'jumpright|ryu.kick', 'fire(0)', 'fire(1)', 'superpunch(0)', 'superpunch(1)', 'superkick(0)', 'superkick(1)', 'defendup(0)', 'defendup(1)', 'defenddown(0)', 'defenddown(1)'] 
        self.p = [1.0-(0.058*16), 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058]
        self.prevhit    = [0, 0]
        self.currenthit = [0, 0]

    def next(self):
        return numpy.random.choice(len(self.p), 1, p=self.p)[0]

    def compute(self, frame):
        phash = imagehash.phash(frame)
        return phash

    def append(self, h, r, hit):
        self.Z[h] = [r, hit]

    def flush(self):
        for k, v in self.Z.items():
            if numpy.sum(v[1]) == 0:
                del self.Z[k]

    def dump(self):
        pickle.dump(self.Z, open(self.root + 'hash-' + str(time.time()) + '.pkl', 'wb'))

def act(r, h, hash):

    hit = hash.Z[h][1]
    if hit[0] == -1:
        hash.p[(r+1)%len(hash.p)] += hash.p[r]
        hash.p[r] = 0.0

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
      ryu.kick()
    elif r == 14:
      ryu.defenddown(0)
      ryu.downkick()
    elif r == 15:
      ryu.defendup(1)
      ryu.kick()
    elif r == 16:
      ryu.defenddown(1)
      ryu.downkick()

def preact(blue, ryu, hash, sumb1, sumb2):

    h = hash.compute(blue)
    r = hash.next()
    if h in hash.Z:
        r = hash.Z[h][0]

    hash.currenthit[0], hash.currenthit[1] = (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)

    hit = [0, 0]
    hit[0], hit[1] = hash.currenthit[0] - hash.prevhit[0], hash.currenthit[1] - hash.prevhit[1]
    hit[0], hit[1] =  -1 if hit[0] else 0, 1 if hit[1] else 0

    hash.append(h, r, hit)

    act(r, h, hash)

    for i in range(2):
        hash.prevhit[i] = hash.currenthit[i]

    print("(%d) - [%s] %s (%s)" %(len(hash.Z), h, hash.Z[h], hash.action[r]))

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600}
    scene = {"top": 240+border, "left": 100, "width": 800, "height":400}

    startGame = False

    ryu       = RYU()
    transform = TRANSFORM()
    hash      = HASH()

    while [ 1 ]:

        p1 = numpy.array(sct.grab(blood))
        p2 = p1.copy()

        b1 = p1[60:78, 68:364]
        b2 = p2[60:78, 68+366:364+366]
        ko = p1[60:80, 378:424]

        sumb1, sumb2, kosum = numpy.sum(b1), numpy.sum(b2), numpy.sum(ko)

        if sumb1 >= BLOOD[0] and sumb1 <= BLOOD[1]:

            if startGame:
                x = cv2.resize(numpy.array(sct.grab(scene)),(200,100))
                blue = transform.blue(x)
                preact(Image.fromarray(blue), ryu, hash, sumb1, sumb2)
                
            if sumb1 == BLOOD[1] and sumb2 == BLOOD[1] and not startGame:
                print '[Start]'
                startGame = True
                time.sleep(1)

            elif sumb1 == BLOOD[0]:
                print 'P1 [KO]'
                hash.flush()
                startGame = False
                time.sleep(1)

            elif sumb2 == BLOOD[0]:
                print 'P2 [KO]'
                hash.flush()
                startGame = False
                time.sleep(1)

        elif sumb1 == RESUME[0]:
            ryu.insertcoin()
        
        elif sumb1 == RESUME[1]:
            ryu.select()
