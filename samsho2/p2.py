import cv2
import mss
import numpy

from haohmaru import *
from scene import *
from phash import *
from hist import *
from dft import *
from act import *

if __name__ == '__main__':

    with mss.mss() as sct:

        haohmaru  = HAOHMARU('j', 'l', 'i', 'k', 't', 'g', 'r')
        scene     = SCENE()
        phash     = PHASH()
        hist      = HIST()
        dft       = DFT()
        act       = ACT()

        while [ 1 ]:

            full  = numpy.array(sct.grab(scene.full))
            frame = numpy.array(sct.grab(scene.body))
            r = act.next()
            print phash.compute(frame), '-', act.action[r], numpy.sum(hist.compute(full)), numpy.sum(dft.compute(full))/1000000.0
            haohmaru.act(r)
