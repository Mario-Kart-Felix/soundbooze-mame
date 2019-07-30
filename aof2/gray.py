import sys
import cv2
import mss
import numpy

def blue(img):
    img[:,:,1] = 0
    img[img < 254] = 0
    h, w, _ = img.shape
    img = cv2.resize(img, (w/2, h/2))
    return img

with mss.mss() as sct:

    monitor = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        img = numpy.array(sct.grab(monitor))
        h, w, _ = img.shape
        img = cv2.resize(img, (w/2, h/2))

        img = blue(img)
        Z = numpy.float32(img)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 4
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        center = numpy.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((img.shape))

        gray = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
        gray[gray > 127] = 0

        cv2.imshow("gray", gray)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
