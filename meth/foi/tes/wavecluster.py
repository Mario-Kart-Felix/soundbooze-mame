import sys
import cv2
import mss
import pywt
import numpy

def red(frame):
    rg = frame.copy()
    rg[:,:,1] = 0
    rg[:,:,2] = 0
    rg[rg < 255] = 0
    return rg

with mss.mss() as sct:

    monitor = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        img = numpy.array(sct.grab(monitor))
        h, w, _ = img.shape
        #img = cv2.resize(img, (w/4, h/4))
        img = red(img)

        Z = numpy.float32(img)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 4
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10/2,cv2.KMEANS_RANDOM_CENTERS)

        center = numpy.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((img.shape))

        cA, cD = pywt.dwt(img, 'db2')
        cv2.imshow("ca", cA)
        cv2.imshow("cd", cD)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
