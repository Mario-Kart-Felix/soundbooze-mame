# -*- coding: utf-8 -*-

import cv2
import numpy

class ORB:

    def __init__(self):
        self.orb    = cv2.ORB_create()
        self.O      = {}

    def reset(self):
        self.O      = {}

    def compute(self, frame):
        kp, d = self.orb.detectAndCompute(frame, None)
        sumd = numpy.sum(d) if numpy.sum(d) is not None else 0
        self.O[sumd] = sumd
        return kp, d, sumd

    def percentile(self, sumd):
        Z = []
        for o in self.O:
            Z.append(o)
        Z = numpy.array(Z)

        if    sumd      < numpy.percentile(Z, 20):
            return 0
        elif  sumd    >=  numpy.percentile(Z, 20) and sumd < numpy.percentile(Z, 30):
            return 1
        elif  sumd    >=  numpy.percentile(Z, 40) and sumd < numpy.percentile(Z, 50):
            return 2
        elif  sumd    >=  numpy.percentile(Z, 50) and sumd < numpy.percentile(Z, 60):
            return 3
        elif  sumd    >=  numpy.percentile(Z, 60) and sumd < numpy.percentile(Z, 70):
            return 4
        elif  sumd    >=  numpy.percentile(Z, 70) and sumd < numpy.percentile(Z, 80):
            return 5
        elif  sumd    >=  numpy.percentile(Z, 80) and sumd < numpy.percentile(Z, 90):
            return 6
        elif  sumd    >=  numpy.percentile(Z, 90):
            return 7
