import numpy as np
import cv2
import time
import mss
import cv2 as cv
import sys

def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    
    l = len(fx[fx > 0])
    r = len(fx[fx < 0])

    if l > 99 or r > 99:
        print np.argmax([l, r])

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

        monitor = {"top": 600, "left": 100, "width": 400, "height": 100}

        prev = np.array(sct.grab(monitor))
        prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

        while [ 1 ]:

            img = np.array(sct.grab(monitor))

            vis = img.copy()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prevgray,gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            prevgray = gray

            '''
            gray1 = cv2.cvtColor(draw_hsv(flow), cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray1, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            '''
 
            draw_flow(gray, flow)
            #cv2.imshow('flow', draw_flow(gray, flow))
            #cv2.imshow('flow', draw_flow(np.zeros((100,800), np.uint8), flow))

            k = cv.waitKey(1) & 0xff
            if k == 27:
                break

grab()
