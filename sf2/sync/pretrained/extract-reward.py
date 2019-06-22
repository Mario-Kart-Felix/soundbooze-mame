import numpy
import time
import sys
import os
import pickle
import cv2

input_path = "reward/"

def load(reward):
    with open (reward, 'rb') as fp:
        return pickle.load(fp)

total = 0
idx = 0

for dir_path, subdir_list, file_list in os.walk(input_path):
    for fname in file_list:
        full_path = os.path.join(dir_path, fname)
        r = load(full_path)
        total += len(r)

        for i in r:
            cv2.imwrite('/tmp/reward/png/' + str(idx) + '.png', numpy.array(i).reshape(50,100))
            idx+=1

print 'Total', total 
