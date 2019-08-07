import mss
import cv2
import time
import numpy
import PIL
import imagehash
import multiprocessing

from ring import *
from ryu import *

class SCORE:

    def __init__(self):
        self.BLOOD      = [2744512, 4089536, 745816 * 4]
        self.RESUME     = [1358640, 2617406, 2264400, 2623509]
        self.blood      = {"top": 124, "left": 100, "width": 800, "height":100}
        self.scene      = {"top": 264, "left": 100, "width": 800, "height":400}
        self.prevhit    = [0, 0]
        self.currenthit = [0, 0]
        self.sumb1      = 0
        self.sumb2      = 0
        self.rbsum      = 0
        self.rb         = RINGBUFFER(4)
        self.play       = False

    def compute(self):
        h = numpy.array(sct.grab(score.blood))
        b1 = h[60:78, 68:364]
        b2 = h[60:78, 68+366:364+366]
        ko = h[60:80, 378:424]
        self.sumb1, self.sumb2, kosum = numpy.sum(b1), numpy.sum(b2), numpy.sum(ko)
        self.rb.append(kosum)
        self.rbsum = numpy.sum(self.rb.get())
    
    def count(self):
        self.currenthit[0], self.currenthit[1] = (0.4089536-self.sumb1/10000000.0), (0.4089536-self.sumb2/10000000.0)
        hit = [0, 0]
        hit[0], hit[1] = score.currenthit[0] - score.prevhit[0], score.currenthit[1] - score.prevhit[1]
        hit[0], hit[1] =  -1 if hit[0] else 0, 1 if hit[1] else 0
        return hit

    def update(self):
        for i in range(2):
            self.prevhit[i] = self.currenthit[i]

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
        self.H       = {}
        self.action  = ['left', 'jumpleft|kick', 'kick|left|kick', 'defendup(0)', 'defenddown(0)', 'fire(0)', 'superpunch(0)', 'superkick(0)', 'punch', 'kick', 'downkick', 'kick|jumpup|kick', 'right', 'jumpright|kick', 'kick|right|kick', 'defendup(1)', 'defenddown(1)', 'fire(1)', 'superpunch(1)', 'superkick(1)']
        self.p       = numpy.random.rand(len(self.action))
        self.p      /= numpy.sum(self.p)
        self.length  = 5

    def append(self, h, r):
        self.H[h] = r

    def compute(self, frame):
        return str(imagehash.phash(frame))

def act(R):

    for r in R:
        print phash.action[r]
        ryu.act(r)

    print ''

def preact(blue, ryu, phash):

        h = phash.compute(blue)

        r = 0
        if h in phash.H:
            r = phash.H
            #print '*',
        else:
            r = numpy.random.randint(0,20)

        R = numpy.random.choice(len(phash.p), phash.length, p=phash.p)

        p = multiprocessing.Process(target=act, args=(R,))
        p.start()
        p.join()
        phash.append(h, r)

        hit = score.count()

        if hit[0] == -1:
            phash.p   = numpy.random.rand(len(phash.action))
            phash.p  /= numpy.sum(phash.p)
            print '[!]',

        if hit[1] == 1:
            print '[+]',

        score.update()

        try:
            print("%s %s" %(h, phash.action[r]))
        except:
            pass

if __name__ == '__main__':

    with mss.mss() as sct:

        ryu         = RYU('Left', 'Right', 'Up', 'Down', 'c', 'd')
        score       = SCORE()
        transform   = TRANSFORM()
        phash       = HASH()

        while [ 1 ]:

            start_ts = time.time()

            score.compute()

            if score.sumb1 >= score.BLOOD[0] and score.sumb1 <= score.BLOOD[1]:

                if score.play:
                    x = cv2.resize(numpy.array(sct.grab(score.scene)),(200,100))
                    blue = transform.blue(x)
                    preact(PIL.Image.fromarray(blue), ryu, phash)
                    
                if score.sumb1 == score.BLOOD[1] and score.sumb2 == score.BLOOD[1] and not score.play:
                    print '[Start]'
                    score.play = True
                    time.sleep(1.08)

                elif score.sumb1 == score.BLOOD[0] and score.rbsum == score.BLOOD[2]:
                    print 'P1 [KO]'
                    for k, v in phash.H.items():
                        phash.H[k] = 5
                    score.play = False
                    time.sleep(3.4)

                elif score.sumb2 == score.BLOOD[0] and score.rbsum == score.BLOOD[2]:
                    print 'P2 [KO]'
                    score.play = False
                    time.sleep(3.4)

            elif score.sumb1 == score.RESUME[0]:
                ryu.insertcoin()
            
            elif score.sumb1 == score.RESUME[1] or score.sumb1 == score.RESUME[2] or score.sumb1 == score.RESUME[3]:
                ryu.select()

            fps = 1 / (time.time() - start_ts)
            delta = 1 / fps - (time.time() - start_ts)

            if delta > 0:
                time.sleep(delta)
            else:
                time.sleep(0.05)
