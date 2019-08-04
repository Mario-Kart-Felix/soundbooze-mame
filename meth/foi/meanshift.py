'''
 Based on the following tutorial:
   http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_video/py_meanshift/py_meanshift.html
'''

import cv2
import mss
import numpy
import numpy as np

with mss.mss() as sct:

    monitor = {"top": 124, "left": 100, "width": 800, "height": 600}

    frame = numpy.array(sct.grab(monitor))
    rows, cols = frame.shape[:2]

    windowWidth = 150
    windowHeight = 200
    windowCol = int((cols - windowWidth) / 2)
    windowRow = int((rows - windowHeight) / 2)
    window = (windowCol, windowRow, windowWidth, windowHeight)

    roi = frame[windowRow:windowRow + windowHeight, windowCol:windowCol + windowWidth]
    roiHsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lowLimit = np.array((18., 45., 45.))
    highLimit = np.array((90., 255., 255.))
    mask = cv2.inRange(roiHsv, lowLimit, highLimit)

    roiHist = cv2.calcHist([roiHsv], [0], mask, [180], [0, 180])
    cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)

    terminationCriteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS , 1, 1)

    while [ 1 ]:

        frame = numpy.array(sct.grab(monitor))

        frameHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        backprojectedFrame = cv2.calcBackProject([frameHsv], [0], roiHist, [0, 180], 1)

        mask = cv2.inRange(frameHsv, lowLimit, highLimit)
        backprojectedFrame &= mask

        ret, window = cv2.meanShift(backprojectedFrame, window, terminationCriteria)

        windowCol, windowRow = window[:2]
        frame = cv2.rectangle(frame, (windowCol, windowRow), (windowCol + windowWidth, windowRow + windowHeight), 255, 2)

        cv2.imshow("ms", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
