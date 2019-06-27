import os
import sys
import mss
import cv2
import time
import numpy
import signal
from skimage.measure import compare_ssim

from info import *

def sigexit(signal, frame):
    global fp
    fp.close()
    sys.exit(0)

def init(d):

    i = Info()

    directory = d 
    session = i.uniq()
    fullpath = directory + '/' + session + '/'

    if not os.path.exists(fullpath):
        os.mkdir(fullpath)

    fi = open(fullpath + 'info.txt', "w+")
    fi.write("INFO: %s\r\n" % i.info())
    fi.write("CONSTANT: %s\r\n" % i.constant())
    fi.write("UNIQ: %s\r\n" % i.uniq())
    fi.write("SCREEN: %s\r\n" % i.screen())
    fi.close()

    fp = open(fullpath + 'active.csv', "a+")
    fp.write('ts,'+'idx,'+'level,'+'zcr'+'\n')
    signal.signal(signal.SIGINT, sigexit)

    return fp, fullpath

def mksubdir(fd):
    if not os.path.exists(fd):
        os.mkdir(fd)

class RingBuffer:

    def __init__(self):
        self.size = 16
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

def flushtoramdisk(m, fullpath, img):
    h, w, d = img.shape
    cv2.imwrite(fullpath + str(m-1) + '/' + str(time.time()) + '.png', cv2.resize(img, (w/4, h/4)))

fp, fullpath = init(sys.argv[1]) 

with mss.mss() as sct:

    rb = RingBuffer()
    active = 0
    zcr = 0

    M = {}
    for num, monitor in enumerate(sct.monitors[1:], 1):
        M[num] = monitor

    prevframes = []
    frames = []

    for m in M:
        print 'Monitor #'+str(m-1), M[m]
        mksubdir(fullpath + str(m-1))
        prevframes.append(numpy.array(sct.grab(M[m])))

    while [ 1 ]: 

        last_time = time.time()

        for m in M:
            img = numpy.array(sct.grab(M[m]))
            flushtoramdisk(m, fullpath, img)
            frames.append(img)

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
            #print ts, '-', '[Active]', '['+str(idx)+']', level, zcr
            fp.write(str(ts) + ',' + str(idx) + ',' + str(level) + ',' + str(zcr) + '\n')
        except:
            pass

        prevframes = []
        frames = []

        for m in M:
            prevframes.append(numpy.array(sct.grab(M[m])))

        print("fps: {}".format(1 / (time.time() - last_time)))
