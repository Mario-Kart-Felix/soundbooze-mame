import numpy
import cv2
import time
import mss
import os

with mss.mss() as sct:

    border = 24
    scene = {"top": 100+border, "left": 100, "width": 800, "height":120-border}

    nfsroot = "nfs/"
    directory = nfsroot + str(time.time())
    os.mkdir(directory)

    i = 0

    while [ 1 ]:

        last_time = time.time()
       
        frame = numpy.array(sct.grab(scene))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127,255,cv2.THRESH_BINARY)
        edges = cv2.Canny(thresh, 100, 200, True)

        cv2.imwrite(directory + '/' + str(time.time()) + '.png', edges)
        i += 1

        #print("fps: {}".format(1 / (time.time() - last_time)))
