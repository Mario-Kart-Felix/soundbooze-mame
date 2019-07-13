import os
import time
import mss
import cv2
import numpy
import multiprocessing
from scipy.signal import find_peaks

import tensorflow 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

from ring import *
from ryu import *
from ddqn import *

BLOOD     = [2744512, 4089536, 745816 * 4]
RESUME    = [1358640, 2617406, 2264400, 2623509]

class CONFIG:

    def __init__(self):
        self.action     = ['left', 'jumpleft|kick', 'kick|left|kick', 'defendup(0)', 'defenddown(0)', 'fire(0)', 'superpunch(0)', 'superkick(0)', 'punch', 'kick', 'downkick', 'kick|jumpup|kick', 'right', 'jumpright|kick', 'kick|right|kick', 'defendup(1)', 'defenddown(1)', 'fire(1)', 'superpunch(1)', 'superkick(1)']
        self.prevhit    = [0, 0]
        self.currenthit = [0, 0]

class FEATURE:

    def __init__(self):
        self.HB         = [0, 0, 0, 0]
        self.prevzcount = 0

    def transform(self, frame):
        red = frame.copy()
        red[:,:,0] = 0
        red[:,:,1] = 0
        red[red < 250] = 0
        return red

    def head(self, curr, prev):
        sumdiff = numpy.sum(curr - prev)
        if sumdiff > 0:
            (b, g, r, _) = cv2.split(frame_h)
            B = b.ravel()
            G = g.ravel()
            B[B<255] = 0
            G[G<255] = 0

            zcount = 0
            for i in range(len(B)):
                if B[i] == 255 and G[i] == 255:
                    zcount += 1
                    
            j = numpy.absolute(zcount - self.prevzcount)/1000.0
            self.HB[0], self.HB[1] = j, self.prevzcount
            self.prevzcount = zcount

    def body(self, red):
        H = numpy.hsplit(red, 8)
        S = []
        for h in H:
            hsum = numpy.sum(h)/1000000.0
            S.append(hsum)

        peaks, _ = find_peaks(S, height=0)

        if len(peaks) == 2:
            p1 = S[peaks[0]]
            p2 = S[peaks[1]] 
            pabs = numpy.absolute(p1-p2)
            h = numpy.argmax(S)
            self.HB[2], self.HB[3] = h, pabs

def act(dnh, HB, hit, timesteps, ev, ns):

    def _run():
        ns.value = True
        ev.set()

        r = dnh.act(HB)
        ryu.act(r)

        if numpy.sum(hit) > 0:
            TG = timesteps.get()
            for i in range(len(TG) - 1):
                dnh.remember(TG[i], r, np.sum(hit), TG[i+1])

        ns.value = False
        ev.set()

    try:
        z = ns.value
        if not z:
            _run()

    except Exception, err:
        _run()
        pass

    ev.wait()

def reward(frame, config, sumb1, sumb2):
    config.currenthit[0], config.currenthit[1] = (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)
    hit = [0, 0]
    hit[0], hit[1] = config.currenthit[0] - config.prevhit[0], config.currenthit[1] - config.prevhit[1]
    hit[0], hit[1] =  -1 if hit[0] else 0, 1 if hit[1] else 0
    for i in range(2):
        config.prevhit[i] = config.currenthit[i]
    return hit

with mss.mss() as sct:

    head = {"top": 124, "left": 100, "width": 800, "height": 100}
    body = {"top": 324, "left": 100, "width": 800, "height": 400}

    startGame = False

    config      = CONFIG()
    feature     = FEATURE()
    ryu         = RYU('Left', 'Right', 'Up', 'Down', 'c', 'd')
    rb          = RINGBUFFER(4)
    timesteps   = RINGBUFFER(8)
    dnh         = DQNAgent(4, len(config.action))

    mgr = multiprocessing.Manager()
    ns = mgr.Namespace()
    ev = multiprocessing.Event()

    prevframe_h = numpy.array(sct.grab(head))

    while [ 1 ]:

        frame_h = numpy.array(sct.grab(head))
        frame_b = numpy.array(sct.grab(body))

        p1 = numpy.array(sct.grab(head))
        p2 = p1.copy()

        b1 = p1[60:78, 68:364]
        b2 = p2[60:78, 68+366:364+366]
        ko = p1[60:80, 378:424]

        sumb1, sumb2, kosum = numpy.sum(b1), numpy.sum(b2), numpy.sum(ko)

        rbsum = 0
        try:
            rbsum = numpy.sum(rb.get())
        except:
            pass

        if sumb1 >= BLOOD[0] and sumb1 <= BLOOD[1]:

            if startGame:

                feature.head(frame_h, prevframe_h)
                feature.body(feature.transform(frame_b))
                timesteps.append(feature.HB)

                hit = reward(frame_h, config, sumb1, sumb2)
                a = multiprocessing.Process(target=act, args=(dnh,feature.HB,hit,timesteps,ev,ns)) 
                a.start() 
                a.join()
                
            if sumb1 == BLOOD[1] and sumb2 == BLOOD[1] and not startGame:
                print '[Start]'
                startGame = True
                time.sleep(1)

            elif sumb1 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P1 [KO]'
                startGame = False
                dnh.update_target_model()
                dnh.replay(batch_size)
                time.sleep(1)

            elif sumb2 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P2 [KO]'
                startGame = False
                dnh.update_target_model()
                dnh.replay(batch_size)
                time.sleep(1)

        elif sumb1 == RESUME[0]:
            ryu.insertcoin()
        
        elif sumb1 == RESUME[1] or sumb1 == RESUME[2] or sumb1 == RESUME[3]:
            ryu.select()

        prevframe_h = frame_h
