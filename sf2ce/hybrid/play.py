import os
import time
import mss
import cv2
import numpy
import multiprocessing

import tensorflow 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

from ryu import *

BLOOD     = [2744512, 4089536, 745816 * 4]
RESUME    = [1358640, 2617406, 2264400, 2623509]

class RINGBUFFER:

    def __init__(self, size):
        self.data = [None for i in xrange(size)]

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data

class CONFIG:

    def __init__(self):
        self.size       = [100, 50]
        self.action     = ['left', 'jumpleft|kick', 'kick|left|kick', 'defendup(0)', 'defenddown(0)', 'fire(0)', 'superpunch(0)', 'superkick(0)', 'punch', 'kick', 'downkick', 'kick|jumpup|kick', 'right', 'jumpright|kick', 'kick|right|kick', 'defendup(1)', 'defenddown(1)', 'fire(1)', 'superpunch(1)', 'superkick(1)']
        self.prevhit    = [0, 0]
        self.currenthit = [0, 0]
        self.timestep   = 8 

    def white(self, frame):
        b = frame.copy()
        b[:,:,1] = 0
        b[:,:,2] = 0
        b[b < 250] = 0
        g = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
        white = g.copy()
        white[white > 0] = 255
        return white

def reward(white, config, sumb1, sumb2):
    config.currenthit[0], config.currenthit[1] = (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)
    hit = [0, 0]
    hit[0], hit[1] = config.currenthit[0] - config.prevhit[0], config.currenthit[1] - config.prevhit[1]
    hit[0], hit[1] =  -1 if hit[0] else 0, 1 if hit[1] else 0
    for i in range(2):
        config.prevhit[i] = config.currenthit[i]
    return hit

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600}
    scene = {"top": 240+border, "left": 100, "width": 800, "height":400}

    play = False

    config      = CONFIG()
    ryu         = RYU('Left', 'Right', 'Up', 'Down', 'c', 'd')
    rb          = RINGBUFFER(4)
    timesteps   = RINGBUFFER(config.timestep)

    shift = 0

    while [ 1 ]:

        p1 = numpy.array(sct.grab(blood))
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

            if play:

                white = config.white(cv2.resize(numpy.array(sct.grab(scene)),(config.size[0],config.size[1])))
                hit = reward(white, config, sumb1, sumb2)

                if shift % 2 == 0:
                    ryu.fire(0)
                    ryu.fire(1)
                elif shift % 3 == 0:
                    ryu.superpunch(0)
                    ryu.superpunch(1)
                elif shift % 5 == 0:
                    ryu.superkick(0)
                    ryu.superkick(1)

                if hit[0] == -1:
                    shift += 1
                
            if sumb1 == BLOOD[1] and sumb2 == BLOOD[1] and not play:
                print '[Start]'
                play = True
                time.sleep(1)

            elif sumb1 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P1 [KO]'
                play = False
                time.sleep(1)

            elif sumb2 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P2 [KO]'
                play = False
                time.sleep(1)

        elif sumb1 == RESUME[0]:
            ryu.insertcoin()
        
        elif sumb1 == RESUME[1] or sumb1 == RESUME[2] or sumb1 == RESUME[3]:
            ryu.select()
