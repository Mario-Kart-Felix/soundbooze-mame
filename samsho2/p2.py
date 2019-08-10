import cv2
import mss
import numpy

from scene import *
from phash import *
from hist import *
from dft import *
from act import *

if __name__ == '__main__':

    with mss.mss() as sct:

        scene     = SCENE()
        phash     = PHASH()
        hist      = HIST()
        dft       = DFT()
        act       = ACT('j', 'l', 'i', 'k', 't', 'g', 'r')

        while [ 1 ]:

            start_ts = time.time()

            full  = numpy.array(sct.grab(scene.full))
            frame = numpy.array(sct.grab(scene.body))
            r = act.next()
            act.act(r)
            print phash.compute(frame), '-', act.action[r], numpy.sum(hist.compute(full)), numpy.sum(dft.compute(full))/1000000.0, numpy.sum(dft.threshold(full)/100.0)

            fps = 1 / (time.time() - start_ts)
            delta = 1 / fps - (time.time() - start_ts)
            if delta > 0:
                time.sleep(delta)
