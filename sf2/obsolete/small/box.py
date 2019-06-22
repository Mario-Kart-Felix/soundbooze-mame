import time
import sys
import cv2
import mss

import numpy as np

def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    
    cv2.polylines(vis, lines, 0, (200, 200, 200))
    for (x1, y1), (x2, y2) in lines:      
	cv2.circle(vis, (x1, y1), 1, (200, 200, 200), -1)
    return vis

def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx*fx+fy*fy)
    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[...,0] = ang*(180/np.pi/2)
    hsv[...,1] = 255
    hsv[...,2] = np.minimum(v*4, 255)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr

def grab():

    with mss.mss() as sct:

        monitor = {"top": 100, "left": 100, "width": 400, "height": 300}

        prev = np.array(sct.grab(monitor))

        h,w,d = prev.shape
        blank = np.zeros((h,w), np.uint8)

        prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

        while [ 1 ]:

            img = np.array(sct.grab(monitor))

            vis = img.copy()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prevgray,gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            prevgray = gray

            gray1 = cv2.cvtColor(draw_hsv(flow), cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray1, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 
            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                if (w > 10 and h > 10) and (w < 100 and h < 100):
                     cv2.rectangle(img,(x, y),(x+w,y+h),(0,0,255),2)
                     #snap
                     #colorcluster - https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/
                     #dynamic template match

            #cv2.imshow('flow', draw_flow(blank, flow))
            cv2.imshow('flow', img)
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break
            prvs = next

grab()
