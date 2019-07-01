import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt

gray = cv2.imread(sys.argv[1], 0)

sift = cv2.xfeatures2d.SIFT_create()
surf = cv2.xfeatures2d.SURF_create()
orb = cv2.ORB_create()
brisk = cv2.BRISK_create()

kpSift = sift.detect(gray, None)
kpSurf = surf.detect(gray, None)
kpOrb, des = orb.detectAndCompute(gray, None)
kpBrisk = brisk.detect(gray, None)

img = cv2.drawKeypoints(gray, kpOrb, None)
plt.imshow(img)
plt.show()
