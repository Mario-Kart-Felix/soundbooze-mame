import time
import cv2
import mss
import numpy

def grab(width, height, left, top):

    with mss.mss() as sct:

        monitor = {"top": top, "left": left, "width": width, "height": height}

        g_kernel = cv2.getGaborKernel((6, 6), 8.0, numpy.pi/4, 10.0, 0.5, 0, ktype=cv2.CV_32F)

        while [ 1 ]:

            img = numpy.array(sct.grab(monitor))
            #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            cv2.imshow('Mame', img)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break

grab(541, 406, 107, 136)
