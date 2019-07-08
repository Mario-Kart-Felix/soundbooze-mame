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
from transition import *

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

                t = time.time()

                config.sum(sct)
                rbsum = _rbsum()

                if config.sumb1 >= config.BLOOD[0] and config.sumb1 <= config.BLOOD[1]:

                    if config.play:
                        red = transform.red(cv2.resize(numpy.array(sct.grab(config.scene)),config.shape))
                        trans.process(pink, red)
                        pink = red

                    if config.sumb1 == config.BLOOD[1] and config.sumb2 == config.BLOOD[1] and not config.play:
                        print '[Start]'
                        config.play = True
                        time.sleep(1)

                    elif config.sumb1 == config.BLOOD[0] and rbsum == config.BLOOD[2]:
                        print 'P1 [KO]'
                        if config.play:
                            trans.save(config.root)
                        config.play = False
                        time.sleep(1)

                    elif config.sumb2 == config.BLOOD[0] and rbsum == config.BLOOD[2] :
                        print 'P2 [KO]'
                        if config.play:
                            trans.save(config.root)
                        config.play = False
                        time.sleep(1)

                elif config.sumb1 == config.RESUME[0]:
                    ryu.insertcoin()
            
                elif config.sumb1 == config.RESUME[1] or config.sumb1 == config.RESUME[2] or config.sumb1 == config.RESUME[3]:
                    ryu.select()

                #print("fps: {}".format(1 / (time.time() - t)))

if __name__ == '__main__':

    config    = CONFIG('.')
    transform = TRANSFORM()
    ryu       = RYU()
    trans     = TRANSITION()

    play = Play()
    play.start()
    play.join()
