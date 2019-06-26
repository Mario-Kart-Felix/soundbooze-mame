import numpy
import time
import sys
import os
import pickle
import cv2
import sys

def load(penalty):
    with open (penalty, 'rb') as fp:
        return pickle.load(fp)

total = 0
idx = 0

r = load(sys.argv[1])
total += len(r)

for i in r:
    cv2.imwrite('/tmp/png/' + str(idx) + '.png', numpy.array(i).reshape(50,100))
    idx+=1

print 'Total', total 
