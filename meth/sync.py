# -*- coding: utf-8 -*-

import cv2
import mss
import time
import numpy

with mss.mss() as sct:

    header = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        start_ts = time.time()

        frame = numpy.array(sct.grab(header))

        fps = 1 / (time.time() - start_ts)
        delta = 1 / fps - (time.time() - start_ts)

        if delta > 0:
            time.sleep(delta)

        print fps, delta
