import os
import mss
import cv2
import time
import numpy

TOTALSAMPLE = 500

with mss.mss() as sct:

    full = {"top": 124, "left": 100, "width": 800, "height": 600}

    prevframe = numpy.array(sct.grab(full))
    h, w, _ = prevframe.shape
    Z = numpy.zeros(h*w)

    i = 0

    while [ 1 ]: 

        last_time = time.time()

        frame = numpy.array(sct.grab(full))

        p = cv2.cvtColor(prevframe, cv2.COLOR_BGR2GRAY)
        f = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        p = numpy.array(p).ravel()
        f = numpy.array(f).ravel()

        Z = numpy.add(Z, numpy.absolute(p-f))
        Z /= 10000000.0

        prevframe = frame

        if i != 0 and i % TOTALSAMPLE == 0:

            print '[Dump]', time.time()

            Z *= 1000000000000 * 255
            Z = numpy.array(Z).reshape(h,w)
            cv2.imwrite('grad-' + str(time.time()) + '.png', Z)

            Z[Z > 0] = 255
            cv2.imwrite('white-' + str(time.time()) + '.png', Z)

            Z = numpy.zeros(h*w)

            #break

        #print("fps: {}".format(1 / (time.time() - last_time)))

        i += 1
