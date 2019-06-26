import os
import sys
import cv2
import numpy

i = 0

os.mkdir('resize')

def resize(img):
    global i
    cv2.imwrite('resize/' + str(i) + '.png', cv2.resize(img, (200, 100)))
    i += 1

directory = sys.argv[1] 
for _, _, fileList in os.walk(directory):
    for fname in fileList:
        img = cv2.imread(directory + fname)
        resize(img)

# python resize.py terrybogard/L/fire/ 
# python resize.py terrybogard/L/kick/ 
# python resize.py terrybogard/L/punch/
# python resize.py terrybogard/L/super/

# python resize.py terrybogard/R/fire/ 
# python resize.py terrybogard/R/kick/ 
# python resize.py terrybogard/R/punch/
# python resize.py terrybogard/R/super/
