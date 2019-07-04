# -*- coding: utf-8 -*-

import os
import cv2
import mss
import time
import numpy
import pickle

from transform import *

class SIFT:

    def __dir__(self):
        self.rootdirectory = str(time.time()) + '/' 
        self.framedirectory = self.rootdirectory + 'frame/'
        if not os.path.exists(self.rootdirectory):
            os.mkdir(self.rootdirectory)
            os.mkdir(self.framedirectory)

    def __init__(self, log):
        self.sift   = cv2.xfeatures2d.SIFT_create()
        self.period = 10000
        self.S      = {}
        self.div    = 4
        self.log    = log
        if self.log:
            self.__dir__()

    def reset(self):
        self.S      = {}
        self.__dir__()

    def compute(self, frame):
        kp, d = self.sift.detectAndCompute(frame, None)
        sumd = numpy.sum(d)
        if sumd is not None:
            self.S[sumd] = sumd
            self._show_(sumd)
            if self.log:
                self._log_(sumd, frame, self.div)
        return kp, d

    def _show_(self, sumd):
        Z = []
        for s in self.S:
            Z.append(s)
        Z = numpy.array(Z)

        if    sumd      < numpy.percentile(Z, 20):
            print '[0]', sumd
        elif  sumd    >=  numpy.percentile(Z, 20) and sumd < numpy.percentile(Z, 30):
            print '[1]', sumd
        elif  sumd    >=  numpy.percentile(Z, 40) and sumd < numpy.percentile(Z, 50):
            print '[2]', sumd
        elif  sumd    >=  numpy.percentile(Z, 50) and sumd < numpy.percentile(Z, 60):
            print '[3]', sumd
        elif  sumd    >=  numpy.percentile(Z, 60) and sumd < numpy.percentile(Z, 70):
            print '[4]', sumd
        elif  sumd    >=  numpy.percentile(Z, 70) and sumd < numpy.percentile(Z, 80):
            print '[5]', sumd
        elif  sumd    >=  numpy.percentile(Z, 80) and sumd < numpy.percentile(Z, 90):
            print '[6]', sumd
        elif  sumd    >=  numpy.percentile(Z, 90):
            print '[7]', sumd

    def _log_(self, sumd, frame, s):
        h, w, _ = frame.shape
        cv2.imwrite(self.framedirectory + str(sumd) + '.png', cv2.resize(frame, (w/s,h/s)))

        if len(self.S) != 0 and len(self.S) % self.period == 0:
            self.dump()

    def match(self, Z, sumd):
        for z in Z:
            if numpy.where(sumd == z):
                return sumd

    def load(self, filename):
        return pickle.load(open(filename, 'rb'))

    def dump(self):
        pickle.dump(self.S, open(self.rootdirectory + str(time.time()) + '-sift.pkl', 'wb'))

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
    sift = SIFT(False)

    while [ 1 ]:

        t = time.time()

        frame_b = numpy.array(sct.grab(body))
        frame_t = transform.transform(frame_b, 'g')
        kp_b, d = sift.compute(frame_t)
        k_b = cv2.drawKeypoints(frame_t, kp_b, None, color=(200,200,200), flags=0)

        '''
        if display(k_b):
            break
        '''

        e = time.time() - t
        if e > 0.029:
            print '[!]'
