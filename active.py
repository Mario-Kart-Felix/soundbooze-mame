import mss
import cv2
import numpy
from skimage.measure import compare_ssim

class RingBuffer:

    def __init__(self, size):
        self.data = [None for i in xrange(size)]

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data

def similar(img_a, img_b):
    img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
    h, w = img_a.shape
    img_a = cv2.resize(img_a, (w/2, h/2))
    img_b = cv2.resize(img_b, (w/2, h/2))
    sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
    return sim

with mss.mss() as sct:

    rb = RingBuffer(16)

    M = {}
    for num, monitor in enumerate(sct.monitors[1:], 1):
        M[num] = monitor

    prevframes = []
    frames = []
    for m in M:
        print 'Monitor #'+str(m), M[m]
        prevframes.append(numpy.array(sct.grab(M[m])))

    while [ 1 ]: 

        for m in M:
            frames.append(numpy.array(sct.grab(M[m])))

        for p, f in zip(prevframes, frames):
            rb.append(similar(p, f))

        Z = rb.get()
        try:
            print '[Active]', numpy.argmin(Z) % len(M)
        except:
            pass

        prevframes = []
        frames = []

        for m in M:
            prevframes.append(numpy.array(sct.grab(M[m])))


    # swig: simd-vector omp
    '''
    TODO:
    slide-window-> (min-stride)
        brute-force
        max(sim-change)
        grab-rect()
    '''
