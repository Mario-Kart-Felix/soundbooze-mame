import os
import mss
import cv2
import time
import numpy
import signal
from skimage.measure import compare_ssim

TOTALSAMPLE =  30
SPLIT       =  4
BOX         =  50
SLIDE       =  7/7

S           = []    # dominant screent iindex
ROI         = [0,0] # dominant ROI [SPLIT x SPLIT] ret:screen(x,y)

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

def similar(img_a, img_b):
    img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
    h, w = img_a.shape
    img_a = cv2.resize(img_a, (w/16, h/16))
    img_b = cv2.resize(img_b, (w/16, h/16))
    sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
    return sim

def simslide(img_a, img_b):
    img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
    sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
    return sim

def argmax2d(M):
    i = numpy.argmax(M)
    return numpy.unravel_index(i, numpy.array(M).shape)

# dominant Screen

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
                rb.append(similar(p, f))

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

        elif len(S) <= 0:
            NA = numpy.array(A)
            idx = NA[:,0]
            level = NA[:,1]
            zcr = NA[:,2]
            z = zcr[numpy.argmax(zcr)]

            u, c = numpy.unique(idx, return_counts=True)
            for x, y in zip(u, c):
                S.append(y)

            '''
            for i in u:
                I = numpy.where(idx == int(i))
                print i, numpy.sum(level[I])
            '''

        elif len(S) > 0:
            break

        prevframes = []
        frames = []

        for m in M:
            prevframes.append(numpy.array(sample.grab(M[m])))

        print("fps: {}".format(1 / (time.time() - last_time))),
        print i

        i += 1

# dominant ROI

with mss.mss() as reg:

    m = numpy.argmax(S) + 1
    rb = RingBuffer(64)

    while [ 1 ]: 

        img = numpy.array(reg.grab(M[m]))

        V = numpy.vsplit(img, SPLIT)

        HH = []
        HSUM = []

        for v in V:
            H = numpy.hsplit(v, SPLIT)
            for h in H:
                HH.append(h)
                HSUM.append(numpy.sum(h)/1000000.0)

        NSUM = numpy.array(HSUM)
        NSUM = NSUM.reshape(SPLIT, SPLIT)
        rb.append(argmax2d(NSUM))

        R = numpy.array(rb.get())
        n = numpy.where(R == None)

        # RingBuffer Full
        if len(n[0]) == 0: 
            R = numpy.array(rb.get())
            h, w, _ = img.shape
            h /= SPLIT 
            w /= SPLIT
            am = argmax2d(HSUM)[0]
            row = int(am/SPLIT)
            col = am % SPLIT
            ROI = [row*h, col*w]
            break

# nearest box finder

from PIL import Image
from PIL import ImageFilter

def crop(img, l, t, width, height):
    im_pil = Image.fromarray(img)
    im_crop = im_pil.crop((l, t, l+width, t+height))
    z = numpy.asarray(im_crop)
    return z

with mss.mss() as nav:

    m = numpy.argmax(S) + 1

    c1 = crop(img, ROI[0], ROI[1], BOX, BOX)

    while [ 1 ]: 

        img = numpy.array(nav.grab(M[m]))

        c2 = crop(img, ROI[0], ROI[1], BOX, BOX)
        print simslide(c1, c2)
        c1 = c2

        '''
        cv2.imshow("crop", c)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
        '''
