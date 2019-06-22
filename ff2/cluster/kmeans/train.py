from sklearn.cluster import KMeans
import numpy as np
import random
import pickle
import cv2
import sys
import os

def create_train_kmeans(data, number_of_clusters):
    k = KMeans(n_clusters=number_of_clusters, n_jobs=2, random_state=728)
    k.fit(data)
    return k

def train():
    data = []
    directory = sys.argv[2]
    for _, _, fileList in os.walk(directory):
        for fname in fileList:
            img = cv2.imread(directory + fname, 0)
            img = cv2.resize(img, (200,100))
            data.append(np.array(img).ravel())

    k = create_train_kmeans(data, int(sys.argv[1]))
    pickle.dump(k, open('kmeans.pkl', 'wb'))

train()

# python train.py 2 png/
