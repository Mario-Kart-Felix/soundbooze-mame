import os
import sys
import mss
import cv2
import time
import numpy
import signal
import hashlib 
from skimage.measure import compare_ssim

def sigexit(signal, fp):
    fp.close()
    sys.exit(0)

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
    img_a = cv2.resize(img_a, (w/2, h/2))
    img_b = cv2.resize(img_b, (w/2, h/2))
    sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
    return sim

def init(d):
    directory = d 
    session = hashlib.md5(directory).hexdigest()
    fullpath = directory + '/' + session + '/'

    if not os.path.exists(fullpath):
        os.mkdir(fullpath)

    return fullpath

def info(fullpath):

    i = Info()
    fi = open(fullpath + 'info.txt', "w+")
    fi.write("INFO: %s\r\n" % i.info())
    fi.write("CONSTANT: %s\r\n" % i.constant())
    fi.write("UNIQ: %s\r\n" % i.uniq())
    fi.write("SCREEN: %s\r\n" % i.screen())
    fi.close()

    fp = open(fullpath + 'active.csv', "a+")
    signal.signal(signal.SIGINT, sigexit(fp))
    return fp

def flushtoramdisk(m, fullpath, img):
    cv2.imwrite(fullpath + str(m-1) + '-' + str(time.time()) + '.png', img)

with mss.mss() as sct:

    fullpath = init(sys.argv[1]) 
    fp = info(fullpath)

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
            fp.write("%s, " % ts)
            fp.write("%d, " % idx)
            fp.write("%f, " % level)
            fp.write("%d\r\n " % zcr)
        except:
            pass

        prevframes = []
        frames = []

        for m in M:
            prevframes.append(numpy.array(sct.grab(M[m])))

        print("fps: {}".format(1 / (time.time() - last_time)))
