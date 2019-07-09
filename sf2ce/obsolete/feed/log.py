import mss
import cv2
import sys
import time
import numpy
import threading
import imagehash
import PIL

from pynput.keyboard import Key, Listener

def hash(frame):
    return imagehash.phash(frame)

class CONFIG:

    def __init__(self, root):
        self.BLOOD      = [2744512, 4089536, 745816 * 4]
        self.RESUME     = [1358640, 2617406, 2264400, 2623509]
        self.blood      = {"top": 100+24, "left": 100, "width": 800, "height":600}
        self.scene      = {"top": 240+24, "left": 100, "width": 800, "height":400}
        self.shape      = (200,100)
        self.sumb1      = 0
        self.sumb2      = 0
        self.prevhit    = [0, 0]
        self.currenthit = [0, 0]
        self.play       = False
        self.rb         = RINGBUFFER(4)
        self.root       = root + '/'

    def sum(self, sct):
        h = numpy.array(sct.grab(self.blood))
        b1 = h[60:78, 68:364]
        b2 = h[60:78, 68+366:364+366]
        ko = h[60:80, 378:424]
        kosum = numpy.sum(ko)
        self.rb.append(kosum)
        self.sumb1, self.sumb2 = numpy.sum(b1), numpy.sum(b2)

    def hitcount(self, sumb1, sumb2):
        self.currenthit[0], self.currenthit[1] = (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)
        hit = [0, 0]
        hit[0], hit[1] = self.currenthit[0] - self.prevhit[0], self.currenthit[1] - self.prevhit[1]
        hit[0], hit[1] =  -1 if hit[0] else 0, 1 if hit[1] else 0
        return hit

    def hitupdate(self):
        for i in range(2):
            self.prevhit[i] = self.currenthit[i]

class RINGBUFFER:

    def __init__(self, size):
        self.data = [None for i in xrange(size)]

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data

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

            prev = cv2.resize(numpy.array(sct.grab(config.scene)),config.shape)
            prev = PIL.Image.fromarray(prev)

            while [ 1 ]:

                config.sum(sct)
                rbsum = _rbsum()

                if config.sumb1 >= config.BLOOD[0] and config.sumb1 <= config.BLOOD[1]:

                    if config.play:

                        curr = cv2.resize(numpy.array(sct.grab(config.scene)),config.shape)
                        curr = PIL.Image.fromarray(curr)

                        print '\t\t\t\t', hash(curr)

                        prev = curr

                    if config.sumb1 == config.BLOOD[1] and config.sumb2 == config.BLOOD[1] and not config.play:
                        print '\t\t\t\t' + '[Start]'
                        config.play = True
                        time.sleep(1)

                    elif config.sumb1 == config.BLOOD[0] and rbsum == config.BLOOD[2]:
                        print '\t\t\t\t' + 'P1 [KO]'
                        config.play = False
                        time.sleep(1)

                    elif config.sumb2 == config.BLOOD[0] and rbsum == config.BLOOD[2] :
                        print '\t\t\t\t' + 'P2 [KO]'
                        config.play = False
                        time.sleep(1)

                elif config.sumb1 == config.RESUME[0]:
                    pass
            
                elif config.sumb1 == config.RESUME[1] or config.sumb1 == config.RESUME[2] or config.sumb1 == config.RESUME[3]:
                    pass
 
class Que (threading.Thread):

    def run(self):

        while [ 1 ]:

            if config.sumb1 >= config.BLOOD[0] and config.sumb1 <= config.BLOOD[1]:

                if config.play:

                    hit = config.hitcount(config.sumb1, config.sumb2)

                    if hit[0] != 0:
                        print '\t\t\t\t[-]', hit

                    if hit[1] != 0:
                        print '\t\t\t\t[+]', hit

                    config.hitupdate()

attr = ['char', 'up', 'down', 'left', 'right']

def on_press(key):

    if hasattr(key, attr[0]):
        print time.time(), 0, key.char

    elif hasattr(key, attr[1]) or hasattr(key, attr[2]) or hasattr(key, attr[3]) or hasattr(key, attr[4]):
        k = ('{0}'.format(key))
        z = k.split('.')
        print time.time(), 0, z[1]

def on_release(key):

    if hasattr(key, attr[0]):
        print time.time(), 1, key.char

    elif hasattr(key, attr[1]) or hasattr(key, attr[2]) or hasattr(key, attr[3]) or hasattr(key, attr[4]):
        k = ('{0}'.format(key))
        z = k.split('.')
        print time.time(), 1, z[1]

class Key (threading.Thread):

    def run(self):

        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

if __name__ == '__main__':

    config    = CONFIG('.')

    play = Play()
    que = Que()
    key = Key()

    play.start()
    que.start()
    key.start()

    play.join()
    que.join()
    key.start()
