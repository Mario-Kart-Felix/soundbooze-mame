# -*- coding: utf-8 -*-

import sys
import cv2
import mss
import numpy
import time

import seaborn as sns; sns.set(color_codes=True)
import matplotlib.pyplot as plt

TOTAL_SAMPLE = 1000

def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = numpy.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
    fx, fy = flow[y,x].T
    lines = numpy.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = numpy.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    
    cv2.polylines(vis, lines, 0, (200, 200, 200))
    for (x1, y1), (x2, y2) in lines:      
        cv2.circle(vis, (x1, y1), 1, (200, 200, 200), -1)
    return vis

def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    ang = numpy.arctan2(fy, fx) + numpy.pi
    v = numpy.sqrt(fx*fx+fy*fy)
    hsv = numpy.zeros((h, w, 3), numpy.uint8)
    hsv[...,0] = ang*(180/numpy.pi/2)
    hsv[...,1] = 255
    hsv[...,2] = numpy.minimum(v*4, 255)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr

def crop(img, i, j, w, h):
    return img[j:j+h, i:i+w]

with mss.mss() as sct:

    body = {"top": 324, "left": 100, "width": 800, "height": 400}

    prev = numpy.array(sct.grab(body))
    h,w,d = prev.shape
    blank = numpy.zeros((h,w), numpy.uint8)
    prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    X, Y = [], []
    W, H = [], []

    i = 0
    while [ 1 ]:

        last_time = time.time()

        frame = numpy.array(sct.grab(body))

        vis = frame.copy()
        gray = cv2.cvtColor(vis, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prevgray,gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        prevgray = gray

        gray1 = cv2.cvtColor(draw_hsv(flow), cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray1, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            # match [tmpl, orb, ..] cluster [size, color, intense...], reduce[...]
            cv2.imwrite('tmp/' + str(i) + '.png', crop(frame, x,y,w,h))

            '''
            X.append(x)
            Y.append(y)
            W.append(w)
            H.append(h)
            '''
        print i
        if i != 0 and i % TOTAL_SAMPLE == 0:
            '''
            plt.subplot(311)
            sns.kdeplot(X, Y, cmap='Reds', shade=True)
            plt.subplot(312)
            sns.kdeplot(W, H, cmap='Blues', shade=True)
            plt.subplot(313)
            sns.heatmap([X,Y])
            '''

            '''
            plt.subplot(411)
            plt.plot(X)
            plt.subplot(412)
            plt.plot(Y)
            plt.subplot(413)
            plt.plot(W)
            plt.subplot(414)
            plt.plot(H)
            '''

            '''
            Z = []
            for w, h in zip(W, H):
                if w == h:
                    Z.append(w)
                else:
                    Z.append(0)

            plt.plot(Z)
            plt.show()
            '''

            break

        i += 1
        #print("fps: {}".format(1 / (time.time() - last_time)))
