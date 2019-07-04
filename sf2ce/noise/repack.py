import os
import cv2
import time
import pickle

PENALTY = []

for i in range(1, 20): 
    for dir_path, subdir_list, file_list in os.walk(str(i) + '/'):
        for fname in file_list:
            full_path = os.path.join(dir_path, fname)
            x = cv2.imread(full_path, 0) 
            print x.shape
            PENALTY.append(x.ravel())

with open('penalty-' + str(time.time()), 'wb') as fp:
    pickle.dump(PENALTY, fp)
