import sys
import cv2
import mss
import numpy
from scipy.stats import skew, kurtosis

from PIL import Image
from PIL import ImageFilter

def calcHistogram(img):

    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    num = numpy.prod(img.shape[:2])
    hist = cv2.calcHist([img], [0], None, [16], [0, 255]) / num
    s = skew(hist)
    k = kurtosis(hist)
    v = numpy.var(hist)
    hsum = numpy.sum(hist)/100.0
    m = (s + k + v + hsum) / 4
    return hsum, m 

def grab(width, height, left, top):

    with mss.mss() as sct:

        monitor = {"top": top, "left": left, "width": width, "height": height}
        subtractor = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=25, detectShadows=True)

        fname = 1
        while [ 1 ]:

            frame = numpy.array(sct.grab(monitor))
            mask = subtractor.apply(frame)
            blur = cv2.GaussianBlur(mask,(5,5),0)

            pil_img = Image.fromarray(blur)
            edge = numpy.array(pil_img.filter(ImageFilter.FIND_EDGES))
            edgecv = cv2.cvtColor(numpy.array(edge), cv2.COLOR_RGB2BGR)

            blursum = (numpy.sum(blur)/1000000.0)
            hsum, m = calcHistogram(blur)

            if m > 0:
                print ("%.5f"% (hsum)),
                print ("%.5f"% blursum)
                if blursum > 0.0 and blursum < 1.8:
                    cv2.imwrite('tmp/' + str(fname) + '.png', blur)

            fname = fname + 1

            cv2.imshow("Blur", edgecv)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break

grab(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
