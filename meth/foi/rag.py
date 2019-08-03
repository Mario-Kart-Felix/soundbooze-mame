# -*- coding: utf-8 -*-

import cv2
import mss
import time
import numpy

from skimage import data, io, segmentation, color
from skimage.future import graph
from matplotlib import pyplot as plt

with mss.mss() as sct:

    full = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        img = cv2.resize(numpy.array(sct.grab(full)), (100,75))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        labels1 = segmentation.slic(img, compactness=30, n_segments=400)
        out1 = color.label2rgb(labels1, img, kind='avg')
        g = graph.rag_mean_color(img, labels1)
        labels2 = graph.cut_threshold(labels1, g, 29)
        out2 = color.label2rgb(labels2, img, kind='avg')

        cv2.imshow("1", out1)
        cv2.imshow("2", out2)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
