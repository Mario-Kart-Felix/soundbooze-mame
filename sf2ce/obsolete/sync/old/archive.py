import os 
import cv2
import pickle
import numpy
from skimage.measure import compare_ssim

class Archive:

    def __init__(self):
        self.enemy = ''
        self.E = ['balrog', 'bison', 'blanka', 'chunli', 'dhalsim', 'guile', 'honda', 'ken', 'ryu', 'sagat', 'vega', 'zangief']
        self.P = []
        self.R = []

    def _similar(self, img_a, img_b):
        sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
        return sim

    def _count(self):
        tp = 0
        if len(self.P) > 0:
            for p in self.P:
                tp += len(p)
        tr = 0
        if len(self.R) > 0:
            for r in self.R:
                tr += len(r)
        return tp, tr

    def load(self, startframe):

        def _l(d):
            with open (d, 'rb') as fp:
                return pickle.load(fp)

        self.P, self.R = [], []

        ms = 0
        for e in self.E:
            img = cv2.imread('../noise/' + e + '/' + '1.png', 0)
            s = self._similar(cv2.resize(img, (200, 100)), cv2.resize(startframe, (200, 100)))
            print '[eList]', e, s
            if s > ms:
                ms = s
                self.enemy = e

        print '[Found]', self.enemy, ms

        for dir_path, subdir_list, file_list in os.walk('../noise/' + self.enemy + '/penalty'):
            for fname in file_list:
                full_path = os.path.join(dir_path, fname)
                r = _l(full_path)
                self.P.append(r)

        for dir_path, subdir_list, file_list in os.walk('../noise/' + self.enemy + '/reward'):
            for fname in file_list:
                full_path = os.path.join(dir_path, fname)
                r = _l(full_path)
                self.R.append(r)

        tp, tr = self._count()
        return tp, tr
