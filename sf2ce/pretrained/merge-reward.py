import numpy
import time
import sys
import os
import pickle

input_path = "reward/"

def load(reward):
    with open (reward, 'rb') as fp:
        return pickle.load(fp)

def save(REWARD):
    with open(input_path + 'reward-merged-' + str(time.time()), 'wb') as fp:
        pickle.dump(REWARD, fp)

REWARD = []

for dir_path, subdir_list, file_list in os.walk(input_path):
    for fname in file_list:
        full_path = os.path.join(dir_path, fname)
        r = load(full_path)
        REWARD.append(r)

save(REWARD)
