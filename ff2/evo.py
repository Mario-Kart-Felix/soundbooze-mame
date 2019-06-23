# -*- coding: utf-8 -*-

import sys
import cv2
import mss
import numpy
import multiprocessing

from scipy.signal import find_peaks

from terry import *

def act(r, h, ev, ns):

    def _run(r):
        ns.value = True
        ev.set()

        '''
        if h <= 3:
            r = numpy.random.uniform(0,1)
            if r <= 0.5:
                terry.shift(0)
                terry.left()
            elif r > 0.5:
                terry.jumpleft()
                terry.kick()
        elif h > 3:
            r = numpy.random.uniform(0,1)
            if r <= 0.5:
                terry.shift(1)
                terry.right()
            elif r > 0.5:
                terry.jumpright()
                terry.kick()

        if r <= 0.25:
            if h <= 3:
                terry.burnknuckle(0)
            elif h > 3: 
                terry.burnknuckle(1)
        elif r > 0.25 and r <= 0.5:
            if h <= 3:
                terry.powerwave(0)
            elif h > 3: 
                terry.powerwave(1)
        elif r > 0.5 and r <= 0.75:
            if h <= 3:
                terry.risingtackle(0)
            elif h > 3: 
                terry.risingtackle(1)
        elif r > 0.75:
            if h <= 3:
                terry.crackshoot(0)
            elif h > 3: 
                terry.crackshoot(1)
        '''

        ns.value = False
        ev.set()

    z = False
    try:
        z = ns.value
        if not z:
            _run(r)

    except Exception, err:
        _run(r)
        pass
    ev.wait()

with mss.mss() as sct:

    header = {"top": 124, "left": 100, "width": 800, "height": 104}
    body = {"top": 284, "left": 100, "width": 800, "height": 300+24}
    full = {"top": 124, "left": 100, "width": 800, "height": 600+24}

    #prevzcount = 0
    prevframe_h = numpy.array(sct.grab(header))
    prevframe_b = numpy.array(sct.grab(body))

    terry = TERRY()

    mgr = multiprocessing.Manager()
    ns = mgr.Namespace()
    ev = multiprocessing.Event()

    while [ 1 ]:

        last_time = time.time()

        frame_h = numpy.array(sct.grab(header))
        frame_b = numpy.array(sct.grab(body))

        red = frame_b.copy()
        green = frame_b.copy()
        blue = frame_b.copy()
        pink = frame_b.copy()

        # body

        red[:,:,0] = 0
        red[:,:,1] = 0
        red[red < 250] = 0

        green[:,:,0] = 0
        green[:,:,2] = 0
        green[green < 250] = 0

        blue[:,:,1] = 0
        blue[:,:,2] = 0
        blue[blue < 250] = 0

        pink[:,:,0] = 255
        pink[:,:,2] = 255

        gray = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)

        white = gray.copy()
        white[white > 0] = 255

        H = numpy.hsplit(red, 8) #white, 8)
        S = []
        for h in H:
            hsum = numpy.sum(h)/1000000.0
            S.append(hsum)

        peaks, _ = find_peaks(S, height=0)

        if len(peaks) == 2:
            p1 = S[peaks[0]]
            p2 = S[peaks[1]] 
            pabs = numpy.absolute(p1-p2)
            if pabs < 0.18:
                h = numpy.argmax(S)
                print '[↭]', h, pabs
                r = numpy.random.uniform(0,1)
                a = multiprocessing.Process(target=act, args=(r,h,ev,ns)) 
                a.start() 

        # header
        '''
        sumdiff = numpy.sum(frame_h - prevframe_h)
        if sumdiff > 0:
            (b, g, r, a) = cv2.split(frame_h)
            B = b.ravel()
            G = g.ravel()
            B[B<255] = 0
            G[G<255] = 0

            zcount = 0
            for i in range(len(B)):
                if B[i] == 255 and G[i] == 255:
                    zcount += 1
                    
            jump = numpy.absolute(zcount - prevzcount)/1000.0
            if jump > 0:
                print '[↥]', jump
                r = jump
                if r <= 0.25:
                    terry.jumpleft()
                    terry.kick()
                elif r > 0.25 and r <= 0.5:
                    terry.jumpright()
                    terry.kick()
                elif r > 0.5 and r <= 0.75:
                    terry.left()
                    terry.punch()
                    terry.shift(0)
                elif r > 0.75:
                    terry.right()
                    terry.punch()
                    terry.shift(1)

            prevzcount = zcount

        '''

        cv2.imshow("FF2 W", white)
        #cv2.imshow("FF2 R", red)
        #cv2.imshow("FF2 G", green)
        #cv2.imshow("FF2 B", blue)
        #cv2.imshow("FF2 GR", gray)
        #cv2.imshow("FF2 P", pink)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

        prevframe_h = frame_h
        prevframe_b = frame_b

        print("fps: {}".format(1 / (time.time() - last_time)))
