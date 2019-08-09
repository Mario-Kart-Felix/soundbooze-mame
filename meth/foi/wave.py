import sys
import cv2
import mss
import pywt
import numpy

def blue(img):
    img[:,:,1] = 0
    img[:,:,2] = 0
    img[img < 254] = 0
    return img

with mss.mss() as sct:

    monitor = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        img = numpy.array(sct.grab(monitor))
        #img = blue(img)

        cA, cD = pywt.dwt(img, 'db2')

        cv2.imshow("ca", cA)
        cv2.imshow("cd", cD)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
