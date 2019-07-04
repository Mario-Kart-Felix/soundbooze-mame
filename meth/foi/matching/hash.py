# -*- coding: utf-8 -*-

import os
import cv2
import mss
import time
import numpy
import pickle
import imagehash
from PIL import Image

from transform import *

class HASH:

    def __dir__(self):
        self.rootdirectory = str(time.time()) + '/' 
        self.framedirectory = self.rootdirectory + 'frame/'
        if not os.path.exists(self.rootdirectory):
            os.mkdir(self.rootdirectory)
            os.mkdir(self.framedirectory)

    def __init__(self, log):
        self.hash   = ''
        self.period = 10000
        self.A      = {}
        self.P      = {}
        self.div    = 4
        self.log    = log
        if self.log:
            self.__dir__()

    def reset(self):
        self.A      = {}
        self.P      = {}
        self.__dir__()

    def compute(self, frame):
        ahash = imagehash.average_hash(frame)
        phash = imagehash.phash(frame)
        self.A[ahash] = ahash
        self.P[phash] = phash
        self._show_(ahash, phash)
        if self.log:
            self._log_(ahash, phash, frame, self.div)
        return ahash, phash

    def _show_(self, ahash, phash):
        print ahash, phash

    def _log_(self, ahash, phash, frame, s):
        w, h = frame.size
        frame = frame.resize((w/s,h/s))
        frame.save(self.framedirectory + str(ahash) + '-' + str(phash) + '.png')

        if len(self.A) != 0 and len(self.A) % self.period == 0:
            self.dump(self.A)
        if len(self.P) != 0 and len(self.P) % self.period == 0:
            self.dump(self.P)

    def match(self, Z, sumd):
        for z in Z:
            if numpy.where(sumd == z):
                return sumd

    def load(self, filename):
        return pickle.load(open(filename, 'rb'))

    def dump(self):
        pickle.dump(self.O, open(self.rootdirectory + str(time.time()) + '-hash.pkl', 'wb'))

def display(frame):
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        return True

    return False

with mss.mss() as sct:

    full   = {"top": 124, "left": 100, "width": 800, "height": 600}
    header = {"top": 124, "left": 100, "width": 800, "height": 100}
    body   = {"top": 284, "left": 100, "width": 800, "height": 400}

    transform = Transform()
    hash = HASH(False)

    while [ 1 ]:

        t = time.time()

        frame_b = numpy.array(sct.grab(body))
        frame_t = transform.transform(frame_b, 'g')
        h = hash.compute(Image.fromarray(frame_t))

        '''
        if display(k_b):
            break
        '''

        e = time.time() - t
        if e > 0.029:
            print '[!]'
