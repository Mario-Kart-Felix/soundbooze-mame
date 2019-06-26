import numpy as np
import cv2
import time
import mss
import sys

def lr_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
    fx, fy = flow[y,x].T
    l = len(fx[fx > 0])
    r = len(fx[fx < 0])
    if l > 80 or r > 80:
        return np.argmax([l, r])

def du_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
    fx, fy = flow[y,x].T
    u = len(fy[fy < 0])
    d = len(fy[fy > 0])
    if u > 80 or d > 80:
        return np.argmax([u, d])

def grab():

    with mss.mss() as sct:

        monitor = {"top": 600, "left": 100, "width": 800, "height": 100}

        prev = np.array(sct.grab(monitor))
        prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
        P = np.hsplit(prevgray, 2)
        prevgrayL = P[0]
        prevgrayR = P[1]

        h = []
        v = []
        while [ 1 ]:

            img = np.array(sct.grab(monitor))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            C = np.hsplit(gray, 2)
            grayL = C[0]
            grayR = C[1]
            flowL = cv2.calcOpticalFlowFarneback(prevgrayL, grayL, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            flowR = cv2.calcOpticalFlowFarneback(prevgrayR, grayR, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            prevgrayL = grayL
            prevgrayR = grayR

            l = lr_flow(grayL, flowL)
            r = lr_flow(grayR, flowR)

            if l is not None and r is not None:
                #print '[LR]', l, r, ' ', l-r # 0 <- , -> 1
                h.append(l-r)

            else:
                h.append(np.nan)

            if len(h) > 1:
                print h #       0 <- <-, 0 -> ->, -1 -> <-
                h = []

            l = du_flow(grayL, flowL)
            r = du_flow(grayR, flowR)

            if l is not None and r is not None:
                #print '[DU]', l, r, l-r # l1,r1 jump
                v.append(l)
                v.append(r)
                if len(v) > 7:
                    print v
                    if np.sum(v) > 7:
                        print time.time(), '[Jump]'
                    v = []

grab()
