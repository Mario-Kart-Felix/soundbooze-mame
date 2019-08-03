# -*- coding: utf-8 -*-

import cv2
import mss
import time
import numpy

from skimage.color import rgb2gray
from skimage.filters.rank import entropy
from skimage.morphology import disk
from skimage import img_as_ubyte

with mss.mss() as sct:

    full = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        img = cv2.resize(numpy.array(sct.grab(full)), (200,150))
        img[:,:,1] = 0
        img[:,:,2] = 0
        img[img < 250] = 0

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        entr_img = entropy(numpy.array(gray), disk(10))

        cv2.imshow("B", entr_img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
