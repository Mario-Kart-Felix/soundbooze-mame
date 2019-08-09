import mss
import numpy

import PIL
import imagehash

from haohmaru import *

class SCENE:

    def __init__(self):
        self.head = {"top": 124, "left": 100, "width": 800, "height": 100}
        self.body = {"top": 264, "left": 100, "width": 800, "height": 400}

class ACT:

    def __init__(self):
        self.action = ['Walk(0)','Shift(0)','DefendUp(0)','DefendDown(0)','StabSwingBack(0)','OugiSenpuuRetsuZan(0)','OugiKogetsuZan(0)','OugiResshinZan(0)','JumpLeftSlash()','JumpSlash()','DownSlash()','Slash()','Walk(1)','Shift(1)','DefendUp(1)','DefendDown(1)','StabSwingBack(1)','OugiSenpuuRetsuZan(1)','OugiKogetsuZan(1)','OugiResshinZan(1)','JumpRightSlash()']

    def next(self):
        return numpy.random.randint(0, len(self.action))

class PHASH:

    def compute(self, frame):
        phash = str(imagehash.phash(PIL.Image.fromarray(frame)))
        return phash

if __name__ == '__main__':

    with mss.mss() as sct:

        haohmaru  = HAOHMARU('Left', 'Right', 'Up', 'Down', 's', 'z')
        scene     = SCENE()
        act       = ACT()
        phash     = PHASH()

        while [ 1 ]:

            frame = numpy.array(sct.grab(scene.body))
            r = act.next()
            print phash.compute(frame), '-', act.action[r]
            haohmaru.act(r)

    
