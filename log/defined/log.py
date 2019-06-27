import numpy
import cv2
import time
import mss
import os

os.mkdir('log')

with mss.mss() as sct:
    border = 24
    scene = {"top": 260+border, "left": 100, "width": 800, "height":424-border}
    i = 0
    while [ 1 ]:
        frame = numpy.array(sct.grab(scene))
        cv2.imwrite('log/' + str(i) + '.png', frame)
        i += 1
