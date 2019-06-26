# -*- coding: utf-8 -*-

import cv2
import mss
import numpy
import time

from skimage.measure import compare_ssim

def similar_h(img_a, img_b):
    img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
    h, w = img_a.shape
    img_a = cv2.resize(img_a, (w/4, h/2))
    img_b = cv2.resize(img_b, (w/4, h/2))
    sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
    return sim

def similar_b(img_a, img_b):
    img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
    h, w = img_a.shape
    img_a = cv2.resize(img_a, (w/8, h/8))
    img_b = cv2.resize(img_b, (w/8, h/8))
    sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
    return sim

def yellow(frame):
    #ff2 - yellow blood
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_yellow = numpy.array([15,255,255])
    upper_yellow = numpy.array([30,255,255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    return res

with mss.mss() as sct:

    header = {"top": 124, "left": 100, "width": 800, "height": 100}
    body = {"top": 284, "left": 100, "width": 800, "height": 400}

    firstframe_h = yellow(numpy.array(sct.grab(header)))
    prevframe_h = firstframe_h.copy()

    firstframe_b = numpy.array(sct.grab(body))
    prevframe_b = firstframe_b.copy()

    HA, HZ, BA, BZ = [], [], [], []
    i = 0

    while [ 1 ]:

        frame_h = yellow(numpy.array(sct.grab(header)))
        frame_b = numpy.array(sct.grab(body))

        HA.append(similar_h(prevframe_h, frame_h))
        HZ.append(similar_h(firstframe_h, frame_h))
        BA.append(similar_b(prevframe_b, frame_b))
        BZ.append(similar_b(firstframe_b, frame_b))

        print i
        if i != 0 and i % 800 == 0:
            print '[Saved]'
            numpy.save('HA-' + str(time.time()), numpy.array(HA))
            numpy.save('HZ-' + str(time.time()), numpy.array(HZ))
            numpy.save('BA-' + str(time.time()), numpy.array(BA))
            numpy.save('BZ-' + str(time.time()), numpy.array(BZ))
            HA, HZ, BA, BZ = [], [], [], []
            i = 0

        '''
        cv2.imshow("B", firstframe)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
        '''

        i += 1
        prevframe_h = frame_h
        prevframe_b = frame_b
