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
        self.H          = {}
        self.action     = ['left', 'jumpleft|kick', 'kick|left|kick', 'defendup(0)', 'defenddown(0)', 'fire(0)', 'superpunch(0)', 'superkick(0)', 'punch', 'kick', 'downkick', 'kick|jumpup|kick', 'right', 'jumpright|kick', 'kick|right|kick', 'defendup(1)', 'defenddown(1)', 'fire(1)', 'superpunch(1)', 'superkick(1)']
        self.p          = numpy.random.rand(len(self.action))
        self.p         /= numpy.sum(self.p)
        self.shift      = 0
        self.prevhit    = [0, 0]
        self.currenthit = [0, 0]

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

def preact(blue, ryu, hash, sumb1, sumb2, timesteps):

    h = hash.compute(blue)

    hash.currenthit[0], hash.currenthit[1] = (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)

    hit = [0, 0]
    hit[0], hit[1] = hash.currenthit[0] - hash.prevhit[0], hash.currenthit[1] - hash.prevhit[1]
    hit[0], hit[1] =  -1 if hit[0] else 0, 1 if hit[1] else 0

    for i in range(2):
        hash.prevhit[i] = hash.currenthit[i]

    TG = timesteps.get()
    print TG, TG.count(h), hit

    time.sleep(0.19)

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
    for i in range(32):
        timesteps.append(hash.compute(prev_timestep))

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
