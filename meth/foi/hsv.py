'''
 Based on the following tutorial:
   http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_video/py_meanshift/py_meanshift.html
'''

import cv2 as cv
import mss
import numpy as np

with mss.mss() as sct:

    monitor = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        frame = np.array(sct.grab(monitor))

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # blue
        #lower = np.array([110,50,50])
        #upper = np.array([130,255,255])

        # red
        #lower = np.array([0,150,150])
        #upper = np.array([0,255,255])

        # yellow
        lower = np.array([20,100,100])
        upper = np.array([30,255,255])

        mask = cv.inRange(hsv, lower, upper)
        res = cv.bitwise_and(frame,frame, mask= mask)

        cv.imshow("ms", res)
        if cv.waitKey(1) & 0xFF == ord("q"):
            cv.destroyAllWindows()
            break
