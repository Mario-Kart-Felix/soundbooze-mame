import os
import mss
import cv2
import time
import numpy

TOTALSAMPLE = 100

with mss.mss() as sct:

    M = {}
    for num, monitor in enumerate(sct.monitors[1:], 1):
        M[num] = monitor

    prevframes = []
    frames = []
    X, Y, Z = [], [], []

    for m in M:
        print 'Monitor #'+str(m-1), M[m]
        prevframes.append(numpy.array(sct.grab(M[m])))
        h, w, _ = prevframes[m-1].shape
        Z.append(numpy.zeros(h*w))

    i = 0

    while [ 1 ]: 

        last_time = time.time()

        for m in M:
            img = numpy.array(sct.grab(M[m]))
            frames.append(img)

        for m in M:
            p = cv2.cvtColor(prevframes[m-1], cv2.COLOR_BGR2GRAY)
            f = cv2.cvtColor(frames[m-1], cv2.COLOR_BGR2GRAY)
            p = numpy.array(p).ravel()
            f = numpy.array(f).ravel()

            Z[m-1] = numpy.add(Z[m-1], p-f)
            Z[m-1] /= 10000000.0

        prevframes = []
        frames = []

        for m in M:
            prevframes.append(numpy.array(sct.grab(M[m])))

        if i != 0 and i % TOTALSAMPLE == 0:

            I = []
            for z in Z:
                I.append(numpy.sum(z))
            u = numpy.argmax(I)

            for i, z in zip(range(len(Z[u])), Z[u]):
                if z:
                    X.append(int(i%w))
                    Y.append(int(i/h))
                    #print int(i/h), int(i%w), z
            l1, t1 = X[numpy.argmin(X)], Y[numpy.argmin(Y)]
            l2, t2 = X[numpy.argmax(X)], Y[numpy.argmax(Y)]

            print '[Monitor #]' + str(u), '-', l1, t1, l2-l1, t2-t1
            break

        #print("fps: {}".format(1 / (time.time() - last_time)))

        i += 1
