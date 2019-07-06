import mss
import cv2
import time
import numpy
import threading

from config import *
from ring import *
from transform import *
from ryu import *
from process import *
from queue import *

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

            pink = transform.red(cv2.resize(numpy.array(sct.grab(config.scene)),(200,100)))

            while [ 1 ]:

                sumb1, sumb2, kosum = config.sum(sct)
                rbsum = _rbsum()

                if sumb1 >= config.BLOOD[0] and sumb1 <= config.BLOOD[1]:

                    if config.play:
                        red = transform.red(cv2.resize(numpy.array(sct.grab(config.scene)),(200,100)))
                        process.process(pink, red, ryu, sumb1, sumb2)
                        pink = red

                    if sumb1 == config.BLOOD[1] and sumb2 == config.BLOOD[1] and not config.play:
                        print '[Start]'
                        if config.play:
                            process.save()
                        config.play = True
                        time.sleep(1)

                    elif sumb1 == config.BLOOD[0] and rbsum == config.BLOOD[2]:
                        print 'P1 [KO]'
                        if config.play:
                            process.save()
                        config.play = False
                        time.sleep(1)

                    elif sumb2 == config.BLOOD[0] and rbsum == config.BLOOD[2] :
                        print 'P2 [KO]'
                        config.play = False
                        time.sleep(1)

class Resume (threading.Thread):

    def run(self):

        with mss.mss() as sct:

            while [ 1 ]:

                sumb1, _, _ = config.sum(sct)

                if sumb1 == config.RESUME[0]:
                    ryu.insertcoin()
                
                elif sumb1 == config.RESUME[1] or sumb1 == config.RESUME[2]:
                    ryu.select()

if __name__ == '__main__':

    config    = CONFIG()
    transform = TRANSFORM()
    ryu       = RYU()
    process   = PROCESS(sys.argv[1])

    play = Play()
    resume = Resume()

    play.start()
    resume.start()
    play.join()
    resume.join()
