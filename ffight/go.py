import os
import mss
import cv2
import time
import numpy
import multiprocessing

import PIL
import imagehash
from scipy.stats import skew
from skimage.measure import compare_ssim

from q import *
from ring import *
from player import *
from orb import *

class TRANSFORM:

    def __init__(self):
        self.w     = 4
        self.h     = 4
        self.split = 8
        self.blank  = 122400000.0
        self.orb   = ORB()
        self.scene = {"top": 122, "left": 100, "width": 800, "height":600}

    def red(self, frame):
        red = frame.copy()
        red[:,:,0] = 0
        red[:,:,1] = 0
        red[red < 250] = 0
        return red

    def similar(self, prev, curr):
        a = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
        b = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
        h, w = a.shape
        a = cv2.resize(a, (w/self.w, h/self.h))
        b = cv2.resize(b, (w/self.w, h/self.h))
        s, _ = compare_ssim(numpy.array(a), numpy.array(b), full=True)
        return s

    def histskew(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [16], [0, 255]) / numpy.prod(gray.shape[:2])
        return skew(hist)[0]

    def redmax(self, red):
        FH = numpy.hsplit(red, self.split)
        FHSUM = []
        for fh in FH:
            FHSUM.append((numpy.sum(fh) / (self.blank/self.split)) - 1)
        return numpy.argmax(FHSUM)

    def orbmax(self, red):
        FH = numpy.hsplit(red, self.split)
        ORBFHSUM = []
        for fh in FH:
            _, _, orbsumfh = transform.orb.compute(fh)
            ORBFHSUM.append(orbsumfh)
        return numpy.argmax(ORBFHSUM)

class HASH:

    def __init__(self):
        self.size       = (200, 150)
        self.depth      = 10

    def compute(self, frame):

        def _chop(H, s):
            chop = ''
            for h in range(0, s):
                chop += H[h]
            return chop

        pilimg = PIL.Image.fromarray(cv2.resize(frame, self.size))
        phash = _chop(str(imagehash.phash(pilimg)), self.depth)
        return phash

class MEMORY:

    def __init__(self):
        self.size   = 64
        self.M      = RINGBUFFER(self.size)
        self.H      = {}

    def append(self, k, v):
        self.M.append(k)
        self.H[k] = v

class ACT:

    def __init__(self):
        self.action  = ['walk(0)', 'walk(1)', 'up', 'down', 'punch', 'superkick', 'jumpkick(0)', 'jumpkick(1)']
        self.player  = PLAYER('Left', 'Right', 'Up', 'Down', 's', 'a')
        self.prob    = numpy.random.rand(len(self.action))
        self.prob   /= numpy.sum(self.prob)

    def go(self, r):
        if r == 0:
            self.player.walk(0.4, 0)
        elif r == 1:
            self.player.walk(1.8, 1)
        elif r == 2:
            self.player.up(0.3)
        elif r == 3:
            self.player.down(0.3)
        elif r == 4:
            self.player.punch()
        elif r == 5:
            self.player.superkick()
        elif r == 6:
            self.player.jumpkick(0)
        elif r == 7:
            self.player.jumpkick(1)

    def resume(self):
        self.player.resume()

class THREAD:

    def __init__(self):
        self.hh     = 0
        self.sleep  = 0.123
        self.step   = 4
        self.memory = MEMORY()
        self.ts     = {}
        self.mgr    = multiprocessing.Manager()
        self.ns     = self.mgr.Namespace()
        self.ev     = multiprocessing.Event()
        self.t      = multiprocessing.Process(target=self.run)
        self.t.start() 

    def set(self, value):
        self.ns.value = value
        self.ev.set()

    def get(self):
        try:
            z = self.ns.value
            return z
        except:
            z = [0, 0, 0, 0, 0, 0, 0]
            return z
        ev.wait()

    def _unpack_(self, Z):
        Z = self.get()
        h, s, redhistskew, redmax, orbsum, orbper, orbmax = Z[0], Z[1], Z[2], Z[3], Z[4], Z[5], Z[6]
        return h, s, redhistskew, redmax, orbsum, orbper, orbmax

    def _concate_(self, M, redmax, orbmax, orbper, a):
        ts = ''
        for i in range(len(M)-1, len(M)-self.step, -1):
            if M[i] is not None:
                ts += str(M[i]) + str(redmax) + str(orbmax) + str(orbper)
        if ts in self.ts:
            print '*',
        self.ts[ts] = a
        return ts

    def run(self):

        act    = ACT()
        q      = Q() 
        prevZ  = [0] * len(self.get()) 

        while [ 1 ]:

            h, s, redhistskew, redmax, orbsum, orbper, orbmax = self._unpack_(self.get())
            self.hh = -1 if (numpy.absolute(s - prevZ[1]) == 0) else numpy.absolute(s - prevZ[1])
            self.memory.append(h, self.hh)

            a = q.act(h)
            act.go(a)

            if h in self.memory.H:
                redhistskew -= 0.1 
 
            M = self.memory.M.get()
            R = orbsum/1000000.0 *( redhistskew / (self.hh * (1.0 + (M.count(h)/len(M)))) )/1000.0

            ts = self._concate_(M, redmax, orbmax, orbper, a)

            q.append(ts)
            q.update(M[0], ts, a, R)

            print("%s [%s] - (%s) [%d %d %d %d] %.5f" %(h, ts, act.action[a], M.count(h), redmax, orbmax, orbper, R))

            prevZ = [h, s, redhistskew, redmax, orbsum, orbmax]

            res = str(h)
            if res.find('8e963') or res.find('c9e6e') or res.find('93e3e') or res.find('91e3e'):
                act.resume()

            time.sleep(self.sleep)

if __name__ == '__main__':

    with mss.mss() as sct:

        thread      = THREAD()
        transform   = TRANSFORM()
        phash       = HASH()

        prevred = transform.red(numpy.array(sct.grab(transform.scene)))

        while [ 1 ]:

            start_ts = time.time()

            red = transform.red(numpy.array(sct.grab(transform.scene)))
            
            h = phash.compute(red)
            s = transform.similar(prevred, red)

            kp_b, d, orbsum = transform.orb.compute(red)
            k_b = cv2.drawKeypoints(red, kp_b, None, color=(250,250,250), flags=0) #

            thread.set([h, s, numpy.sum(red/100000000.0) - transform.histskew(red), transform.redmax(red), orbsum, transform.orb.percentile(orbsum), transform.orbmax(red)])

            fps = 1 / (time.time() - start_ts)
            delta = 1 / fps - (time.time() - start_ts)

            if delta > 0:
                time.sleep(delta)

            prevred = red
