import sys
import cv2
import numpy

WIDTH  = 1920
HEIGHT = 1080

EW = 800
EH = 600

filename = sys.argv[1] 

img = cv2.imread(filename, 0)

class ValidFrame:

    def __init__(self):
        self.clustersize = 4
        self.blocksize = 100

    def idlewatch(self, frame):
        return

    def clusterblock(self, frame):
        return

def vsplit(img, s):
    return numpy.vsplit(img, s)

def hsplit(img, s):
    return numpy.hsplit(img, s)

def crop(i, j, img, w, h):
    return img[j:j+h, i:i+w]

def roll(h1, h2, v1, v2, step):
    z = 0
    for i in range(h1, h2, step): # horizontal
        for j in range(v1, v2, step): # vertical
            er = crop(i, j, img, EW, EH)
            h, w = er.shape
            if h == EH and w == EW:
                cv2.imwrite('tmp/' + str(z) + '.png', er)
                z += 1

roll(270, 480)
