import sys
import cv2
import mss
import numpy

with mss.mss() as sct:

    monitor = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        img = numpy.array(sct.grab(monitor))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        #DIST_L1, DIST_L2, DIST_LABEL_PIXEL, DIST_MASK_3, DIST_C
        distance = cv2.distanceTransform(th, cv2.DIST_L2, 5)

        cv2.imshow("torcs", distance)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
