import numpy
import time
import sys
import os
import pickle

input_path = "penalty/"

def load(penalty):
    with open (penalty, 'rb') as fp:
        return pickle.load(fp)

def save(PENALTY):
    with open(input_path + 'penalty-merged-' + str(time.time()), 'wb') as fp:
        pickle.dump(PENALTY, fp)

PENALTY = []

for dir_path, subdir_list, file_list in os.walk(input_path):
    for fname in file_list:
        full_path = os.path.join(dir_path, fname)
        r = load(full_path)
        PENALTY.append(r)

save(PENALTY)
