import numpy
import cv2
import time
import mss
import os

with mss.mss() as sct:

    border = 24
    scene = {"top": 100+border, "left": 100, "width": 800, "height":600-border}

    nfsroot = "nfs/"
    directory = nfsroot + str(time.time())
    os.mkdir(directory)

    i = 0
    while [ 1 ]:

        last_time = time.time()
       
        frame = numpy.array(sct.grab(scene))
        cv2.imwrite(directory + '/' + str(time.time()) + '.png', frame)
        i += 1

        print("fps: {}".format(1 / (time.time() - last_time)))
