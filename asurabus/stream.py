import mss
import cv2
import time
import numpy

from yashaou import *

if __name__ == '__main__':

    with mss.mss() as sct:

        yashaou     = YASHAOU('Left', 'Right', 'Up', 'Down', 'a', 's', 'd')

        while [ 1 ]:

            start_ts = time.time()
            
            numpy.random.randint(0,16)

            fps = 1 / (time.time() - start_ts)
            delta = 1 / fps - (time.time() - start_ts)

            if delta > 0:
                time.sleep(delta)
