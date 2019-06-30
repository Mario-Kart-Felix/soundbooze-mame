# -*- coding: utf-8 -*-

import os
import sys
import cv2
import numpy

import seaborn as sns; sns.set(color_codes=True)
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def create_train_kmeans(data, number_of_clusters):
    k = KMeans(n_clusters=number_of_clusters, n_jobs=2, random_state=0)
    k.fit(data)
    return k

directory = sys.argv[1]
cluster = int(sys.argv[2])

I = []
R = []
G = []

for dir_path, subdir_list, file_list in os.walk(directory):
    for fname in file_list:
        fullpath = os.path.join(dir_path, fname)
        rgb = cv2.imread(fullpath)
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        I.append(rgb)
        R.append(numpy.sum(rgb)/100000000.0)
        G.append(numpy.sum(gray)/100000000.0)

I = numpy.zeros(len(R))
Z = numpy.array(zip(I, R))

k = create_train_kmeans(Z, cluster)

Z = []
for r in R:
    p = k.predict([[0, r]])[0]
    Z.append(p)

plt.subplot(311)
plt.title('RGB')
plt.plot(R)
plt.subplot(312)
plt.title('Gray')
plt.plot(G)
plt.title('Cluster ' + str(cluster))
plt.subplot(313)
plt.bar(range(len(Z)), Z)
plt.show()
