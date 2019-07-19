import sys
import cv2
import mss
import numpy

def green(img):
    img[:,:,0] = 0
    img[:,:,2] = 0
    img[img < 254] = 0
    h, w, _ = img.shape
    img = cv2.resize(img, (w/4, h/4))
    img[img < 254] = 0
    return img

def redgreen(img):
    img[:,:,0] = 0
    img[img < 254] = 0
    h, w, _ = img.shape
    img = cv2.resize(img, (w/4, h/4))
    img[img < 254] = 0
    return img

def spirit(img):
    img[:,:,2] = 0
    img[img < 254] = 0
    h, w, _ = img.shape
    img = cv2.resize(img, (w/4, h/4))
    img[img < 254] = 0
    return img

def blue(img):
    img[:,:,1] = 0
    img[img < 254] = 0
    h, w, _ = img.shape
    img = cv2.resize(img, (w/4, h/4))
    img[img < 254] = 0
    return img

with mss.mss() as sct:

    monitor = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        img = numpy.array(sct.grab(monitor))
        img = blue(img)
        
        Z = numpy.float32(img)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 4
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

        center = numpy.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((img.shape))

        cv2.imshow("aof2", res2)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
