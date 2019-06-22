from skimage.measure import compare_ssim
import time
import numpy
import sys
import cv2

def similar(img_a, img_b):
    sim = 0.0
    t = time.time()
    try:
        img_a = cv2.resize(img_a, (200,100))
        img_b = cv2.resize(img_b, (200,100))
        h1 = numpy.hsplit(img_a, 2)
        h2 = numpy.hsplit(img_b, 2)
        h1 = numpy.vsplit(h1[1], 2)
        h2 = numpy.vsplit(h2[1], 2)
        img_a = cv2.cvtColor(h1[0], cv2.COLOR_BGR2GRAY)
        img_b = cv2.cvtColor(h2[0], cv2.COLOR_BGR2GRAY)
        _,img_a = cv2.threshold(img_a, 127,255,cv2.THRESH_BINARY)
        _,img_b = cv2.threshold(img_b, 127,255,cv2.THRESH_BINARY)
        #cv2.imwrite('1.png', img_a)
        #cv2.imwrite('2.png', img_b)
        sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True, multichannel=True)
    except:
        pass
    print time.time()-t
    return sim

a = cv2.imread(sys.argv[1])
b = cv2.imread(sys.argv[2])
s = similar(a, b)
print s
