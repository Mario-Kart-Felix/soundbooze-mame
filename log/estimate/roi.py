import os
import mss
import cv2
import time
import numpy
import signal
from skimage.measure import compare_ssim

TOTALSAMPLE =  300
SPLIT       =  4
BOX         =  50*2*4
SLIDE       =  7/7

S           = None                      # screen index
ROI         = [0,0]                     # dominant ROI
ZSUM        = [n-n for n in range(16)]  # min(ROI)

class RingBuffer:

    def __init__(self, size):
        self.size = size 
        self.data = [None for i in xrange(self.size)]

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data

    def size(self):
        return self.size

def similar(t, img_a, img_b):
    if t == 0:
        img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
        img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
        h, w = img_a.shape
        img_a = cv2.resize(img_a, (w/16, h/16))
        img_b = cv2.resize(img_b, (w/16, h/16))
        sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
        return sim

    elif t == 1:
        img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
        img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
        sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
        return sim

    elif t == 2:
        img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
        img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
        h, w = img_a.shape
        img_a = cv2.resize(img_a, (w/2, h/2))
        img_b = cv2.resize(img_b, (w/2, h/2))
        sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
        return sim

def argmax2d(M):
    i = numpy.argmax(M)
    return numpy.unravel_index(i, numpy.array(M).shape)

with mss.mss() as sample:

    rb = RingBuffer(16)
    active = 0
    zcr = 0

    M = {}
    for num, monitor in enumerate(sample.monitors[1:], 1):
        M[num] = monitor

    prevframes = []
    frames = []

    for m in M:
        print 'Monitor #'+str(m-1), M[m]
        prevframes.append(numpy.array(sample.grab(M[m])))

    i = 0
    A = []

    while [ 1 ]: 

        last_time = time.time()

        for m in M:
            img = numpy.array(sample.grab(M[m]))
            frames.append(img)

        if i < TOTALSAMPLE:

            for p, f in zip(prevframes, frames):
                rb.append(similar(0, p, f))

            Z = rb.get()
            ts = time.time()

            try:
                idx = numpy.argmin(Z) % len(M)
                level = float(numpy.sum(Z) / rb.size)
                if active != idx:
                    active = idx
                    zcr += 1
                print ts, '-', '[Active]', '['+str(idx)+']', level, zcr,
                A.append([idx, level, zcr])
            except:
                pass

        elif S is None:
            NA = numpy.array(A)
            idx = NA[:,0]
            level = NA[:,1]
            zcr = NA[:,2]
            z = zcr[numpy.argmax(zcr)]

            XX = []
            YY = []

            u, c = numpy.unique(idx, return_counts=True)
            for x, y in zip(u, c):
                print x, y
                XX.append(x)
                YY.append(y)

            if len(YY) == 1:
                S = XX[0]
            elif len(YY) >= 2:
                S = int(numpy.argmax(YY))

            '''
            for i in u:
                I = numpy.where(idx == int(i))
                print i, numpy.sum(level[I])
            '''

        elif S is not None:
            break

        prevframes = []
        frames = []

        for m in M:
            prevframes.append(numpy.array(sample.grab(M[m])))

        print("fps: {}".format(1 / (time.time() - last_time))),
        print i

        i += 1

with mss.mss() as reg:

    m = (S + 1)
    rb = RingBuffer(32)

    Vprev = numpy.vsplit(numpy.array(reg.grab(M[m])), SPLIT)
    Hprev = []
    for v in Vprev:
        H = numpy.hsplit(v, SPLIT)
        for h in H:
            Hprev.append(h)

    while [ 1 ]: 

        img = numpy.array(reg.grab(M[m]))

        V = numpy.vsplit(img, SPLIT)

        HSUM = []
        for v in V:
            H = numpy.hsplit(v, SPLIT)
            for hprev, h in zip(Hprev, H):
                s = similar(2, hprev, h)
                HSUM.append(s)

        ZSUM = numpy.add(ZSUM, HSUM)

        rb.append(0)

        R = numpy.array(rb.get())
        n = numpy.where(R == None)

        Hprev = []
        for v in Vprev:
            H = numpy.hsplit(v, SPLIT)
            for h in H:
                Hprev.append(h)

        # RingBuffer Full
        if len(n[0]) == 0: 
            h, w, _ = img.shape
            h /= SPLIT 
            w /= SPLIT
            am = numpy.argmin(ZSUM)
            row = int(am/SPLIT) * h 
            col = int(am%SPLIT) * w
            ROI = [row, col]
            print numpy.array(ZSUM).reshape(4,4)
            print 'Index', am, 'Row', row, 'Col', col, ROI
            break

#
#                 ^
# bound-finder <- | ->
#                 +
#

def roi(img, y, x, h, w):
    return img[y:y+h, x:x+w]

with mss.mss() as nav:

    m = (S + 1)

    c1 = roi(img, ROI[0], ROI[1], 270, 480)

    while [ 1 ]: 

        last_time = time.time()

        img = numpy.array(nav.grab(M[m]))

        c2 = roi(img, ROI[0], ROI[1], 270, 480)
        print similar(2, c1, c2),
        c1 = c2

        cv2.imshow("crop", c2)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

        print("fps: {}".format(1 / (time.time() - last_time)))
