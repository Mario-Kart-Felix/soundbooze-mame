import sys
import cv2
import mss
import numpy
import time
import random
from scipy.stats import skew, kurtosis
from scipy.signal import find_peaks
from PIL import Image
from PIL import ImageFilter

def calcHistogram(img):

    num = numpy.prod(img.shape[:2])
    hist = cv2.calcHist([img], [0], None, [16], [0, 255]) / num
    s = skew(hist)
    k = kurtosis(hist)
    v = numpy.var(hist)
    hsum = numpy.sum(hist)/100.0
    m = (s + k + v + hsum) / 4
    return hsum, m 

def grab():

    with mss.mss() as sct:

        monitor = {"top": 600, "left": 100, "width": 800, "height": 100}
        subtractor = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=25, detectShadows=True)

        HH = []
        while [ 1 ]:

            frame = numpy.array(sct.grab(monitor))
            mask = subtractor.apply(frame)
            blur = cv2.GaussianBlur(mask,(5,5),0)

            pil_img = Image.fromarray(blur)
            edge = numpy.array(pil_img.filter(ImageFilter.FIND_EDGES))
            edgecv = cv2.cvtColor(numpy.array(edge), cv2.COLOR_RGB2BGR)

            blursum = (numpy.sum(blur)/1000000.0)
            hsum, m = calcHistogram(blur)

            HS=[]
            if m > 0:
                if blursum > 0.0 and blursum < 1.8:
                    H = numpy.hsplit(blur, 8)
                    for h in H:
                        sk = numpy.sum(h)/1000000.0
                        if sk < 0.3:
                            HS.append(1)
                        else:
                            HS.append(0)
                                

            if len(HS) > 0 and numpy.sum(HS) < 8:
               if len(HH) < 4:
                    HH.append(HS)
               else:
                    print numpy.matrix(HH)
                    HH = []

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break

grab()
