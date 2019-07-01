import mss
import cv2
import time
import numpy

with mss.mss() as sct:

    border = 24
    scene = {"top": 260+border, "left": 100, "width": 800, "height":400}

    orb = cv2.ORB_create()

    #prev-cur
    #cluster

    while [ 1 ]:

        frame = numpy.array(sct.grab(scene))
        gray = frame[:,:,0]

        kpOrb, des = orb.detectAndCompute(gray, None)
        orbimg = cv2.drawKeypoints(gray, kpOrb, None)

        cv2.imshow('ORB', orbimg)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
