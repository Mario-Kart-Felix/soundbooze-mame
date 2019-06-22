import time

import sys
import cv2
import mss
import numpy as np

sdThresh = 10

def distMap(frame1, frame2):

    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist

def grab(width, height, left, top):

    with mss.mss() as sct:

        monitor = {"top": top, "left": left, "width": width, "height": height}

        frame1 = np.array(sct.grab(monitor))
        frame2 = np.array(sct.grab(monitor))

        while [ 1 ]:

            frame3 = np.array(sct.grab(monitor))

            rows, cols, _ = np.shape(frame3)
            dist = distMap(frame1, frame3)

            frame1 = frame2
            frame2 = frame3

            mod = cv2.GaussianBlur(dist, (9,9), 0)
            _, thresh = cv2.threshold(mod, 100, 255, 0)
            _, stDev = cv2.meanStdDev(mod)

            cv2.imshow('dist', mod)

            if cv2.waitKey(1) & 0xFF == 27:
                break

grab(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
