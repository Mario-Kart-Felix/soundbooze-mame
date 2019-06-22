import os
import sys
import cv2
import numpy

i = 0

os.mkdir('split')

def split(img):
    global i
    H = numpy.hsplit(img, 2)
    for h in H:
        cv2.imwrite('split/' + str(i) + '.png', h)
        i += 1

directory = sys.argv[1] 
for _, _, fileList in os.walk(directory):
    for fname in fileList:
        img = cv2.imread(directory + fname)
        split(img)

# python splitter.py terrybogard/L/fire/ 
# python splitter.py terrybogard/L/kick/ 
# python splitter.py terrybogard/L/punch/
# python splitter.py terrybogard/L/super/

# python splitter.py terrybogard/R/fire/ 
# python splitter.py terrybogard/R/kick/ 
# python splitter.py terrybogard/R/punch/
# python splitter.py terrybogard/R/super/
