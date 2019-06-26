import cv2
import sys
import numpy
import matplotlib.pyplot as plt

def diffI(img1, img2):
    h, w = img1.shape
    m = []

    for i in range(h):
        for j in range(w):
            s = numpy.sqrt(numpy.absolute(img1[i,j] - img2[i,j]))
            if s != 0:
                m.append(s)

    return m

img1 = cv2.imread(sys.argv[1], 0)
img2 = cv2.imread(sys.argv[2], 0)

M = diffI(img1, img2)
plt.plot(M)
plt.show()
