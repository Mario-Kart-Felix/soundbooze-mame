import os
import cv2
import time
import pickle

PENALTY = []

for dir_path, subdir_list, file_list in os.walk(str(i) + '/'):
    for fname in file_list:
        full_path = os.path.join(dir_path, fname)
        x = cv2.resize(cv2.imread(full_path, 0), (200, 100)) 
        print x.shape
        PENALTY.append(x.ravel())

with open('penalty-' + str(time.time()), 'wb') as fp:
    pickle.dump(PENALTY, fp)
