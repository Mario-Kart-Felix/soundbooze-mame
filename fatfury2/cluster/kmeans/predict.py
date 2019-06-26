from sklearn.cluster import KMeans
import pickle
import numpy
import cv2
import time
import mss

with mss.mss() as sct:

    border = 24
    scene = {"top": 260+border, "left": 100, "width": 800, "height":424-border}

    k = pickle.load(open('kmeans.pkl', 'rb'))

    while [ 1 ]:

        frame = numpy.array(sct.grab(scene))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(gray, (200,100))
        img = numpy.array(img).ravel()

        p = k.predict([img])
        if p[0] == 0:
            print 'Up'
        else:
            print 'Down'
