# -*- coding: utf-8 -*-

import sys
import cv2
import mss
import numpy
import time
import multiprocessing

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

with mss.mss() as sct:

    header = {"top": 124, "left": 100, "width": 800, "height": 104}
    body = {"top": 284, "left": 100, "width": 800, "height": 300+24}
    full = {"top": 124, "left": 100, "width": 800, "height": 600+24}

    prev = numpy.array(sct.grab(body))
    h,w,d = prev.shape
    blank = numpy.zeros((h,w), numpy.uint8)
    prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    while [ 1 ]:

        last_time = time.time()

        frame_h = numpy.array(sct.grab(header))
        frame_b = numpy.array(sct.grab(body))
        frame_f = numpy.array(sct.grab(full))

        red = frame_b.copy()
        green = frame_b.copy()
        blue = frame_b.copy()
        pink = frame_b.copy()

        # body
        # on-thy-fly [histo] (per-round) :auto min(noise), r,g,b,w,gray
        # for (r,g,b,/) min(sum(sample))
        red[:,:,0] = 0
        red[:,:,1] = 0
        red[red < 250] = 0

        green[:,:,0] = 0
        green[:,:,2] = 0
        green[green < 250] = 0

        blue[:,:,1] = 0
        blue[:,:,2] = 0
        blue[blue < 250] = 0

        gray = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
        white = gray.copy()
        white[white > 0] = 255

        #cv2.imshow("FF2 W", white)
        #cv2.imshow("FF2 R", red)
        #cv2.imshow("FF2 G", green)
        #cv2.imshow("FF2 B", blue)
        #cv2.imshow("FF2 GR", gray)
        #cv2.imshow("FF2 P", pink)

        #k = cv2.waitKey(1) & 0xff
        #if k == 27:
        #    break

        '''
        hsv = cv2.cvtColor(frame_b, cv2.COLOR_BGR2HSV)
        lower_red = numpy.array([0,200,200])
        upper_red = numpy.array([0,255,255])
        #lower_red = numpy.array([161, 155, 84])
        #upper_red = numpy.array([179, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(frame_b,frame_b, mask= mask)

        R = numpy.hsplit(res, 2)
        lr = [numpy.sum(R[0])/1000000.0, numpy.sum(R[1])/1000000.0]
        if lr[0] > lr[1]:
            print 'L'
        else:
            print 'R'
        '''

        #cv2.imshow('mask',mask)
        #cv2.imshow('res',res)

        #flow - pointcluster, r,g,b,a dependent
        # ready(act) ,box-ringbuffer y(max)
        # extreme, sucessfull hit
        vis = red.copy()
        gray = cv2.cvtColor(vis, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prevgray,gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        prevgray = gray

        gray1 = cv2.cvtColor(draw_hsv(flow), cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray1, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            if (w > 4 and h > 4) and (w < 220 and h < 220):
                 cv2.rectangle(red,(x, y),(x+w,y+h),(155, 155, 155),1)

        #cv2.imshow('flow', draw_flow(blank, flow))
        cv2.imshow('flow', red)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

        '''
        #threshold
        gray = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)
        _, th1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
        cv2.THRESH_BINARY,11,2)
        th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        cv2.THRESH_BINARY,11,2)

        cv2.imshow('flow1', th1)
        cv2.imshow('flow2', th3)
        cv2.imshow('flow3', th2)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
        '''

        #print("fps: {}".format(1 / (time.time() - last_time)))
