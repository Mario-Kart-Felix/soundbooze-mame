import cv2
import sys
import numpy
import matplotlib.pyplot as plt

def distance_matrix_py(img1, img2):
    #n = len(pts)
    #p = len(pts[0])
    h, w = img1.shape
    m = numpy.zeros((h, w))

    for i in range(h):
        for j in range(w):
            s = numpy.absolute(img1[i,j] - img2[i,j])
            m[i, j] = s

    return m

img1 = cv2.imread(sys.argv[1], 0)
img2 = cv2.imread(sys.argv[2], 0)

M = distance_matrix_py(img1, img2)

cv2.imshow('image',M)
cv2.waitKey(0)
cv2.destroyAllWindows()

plt.imshow(M)
plt.show()
