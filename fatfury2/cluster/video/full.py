import numpy
import cv2
import time
import mss
import os

with mss.mss() as sct:

    border = 24
    scene = {"top": 100+border, "left": 100, "width": 800, "height": 600}

    nfsroot = "nfs/"
    directory = nfsroot + str(time.time())
    os.mkdir(directory)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(directory + 'full.avi',fourcc, 20.0, (800,600))

    while [ 1 ]:

        frame = numpy.array(sct.grab(scene))
        out.write(frame)

        if numpy.sum(frame) == 0:
            break

    out.release()
