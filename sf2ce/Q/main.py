import mss
import cv2
import sys
import time
import numpy
import Queue
import threading

from config import *
from ring import *
from transform import *
from ryu import *
from process import *

class Play (threading.Thread):

    def run(self):

        def _rbsum():
            rbsum = 0
            try:
                rbsum = numpy.sum(config.rb.get())
            except:
                pass
            return rbsum

        with mss.mss() as sct:

            pink = transform.red(cv2.resize(numpy.array(sct.grab(config.scene)),config.shape))

            while [ 1 ]:

                config.sum(sct)
                rbsum = _rbsum()

                if config.sumb1 >= config.BLOOD[0] and config.sumb1 <= config.BLOOD[1]:

                    if config.play:
                        red = transform.red(cv2.resize(numpy.array(sct.grab(config.scene)),config.shape))
                        process.process(pink, red, ryu)
                        pink = red

                    if config.sumb1 == config.BLOOD[1] and config.sumb2 == config.BLOOD[1] and not config.play:
                        print '[Start]'
                        config.play = True
                        time.sleep(1)

                    elif config.sumb1 == config.BLOOD[0] and rbsum == config.BLOOD[2]:
                        print 'P1 [KO]'
                        if config.play:
                            process.save(config.root)
                        config.play = False
                        time.sleep(1)

                    elif config.sumb2 == config.BLOOD[0] and rbsum == config.BLOOD[2] :
                        print 'P2 [KO]'
                        if config.play:
                            process.save(config.root)
                        config.play = False
                        time.sleep(1)

                elif config.sumb1 == config.RESUME[0]:
                    ryu.insertcoin()
            
                elif config.sumb1 == config.RESUME[1] or config.sumb1 == config.RESUME[2]:
                    ryu.select()

class Que (threading.Thread):

    def run(self):

        while [ 1 ]:

            if config.sumb1 >= config.BLOOD[0] and config.sumb1 <= config.BLOOD[1]:

                if config.play:

                    hit = config.hitcount(config.sumb1, config.sumb2)

                    if hit[0] != 0:
                        print '[-]', process.hash[0], process.hash[2], process.hash[1], hit
                        process.hit(process.hash[0], hit)
                        process.update(process.hash[0], process.hash[2], process.hash[1], hit)
                        process.rminus(process.hash[0], process.hash[2])

                    if hit[1] != 0:
                        print '[+]', process.hash[0], process.hash[2], process.hash[1], hit
                        process.hit(process.hash[0], hit)
                        process.update(process.hash[0], process.hash[2], process.hash[1], hit)
                        process.rplus(process.hash[0], process.hash[2])

                    process.que.put((0))

                    config.hitupdate()

if __name__ == '__main__':

    config    = CONFIG(sys.argv[1])
    transform = TRANSFORM()
    ryu       = RYU()
    process   = PROCESS()

    if len(sys.argv) == 3:
        process.load(sys.argv[2])

    play = Play()
    que = Que()

    play.start()
    que.start()

    play.join()
    que.join()
