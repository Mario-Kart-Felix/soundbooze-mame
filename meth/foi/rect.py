# -*- coding: utf-8 -*-

import os
import sys
import cv2
import numpy

import seaborn as sns; sns.set(color_codes=True)
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def coeff(w, h, tabs):
    x = w * h
    s = numpy.sqrt(x)
    if tabs:
        return numpy.absolute((s-w) + (s-h))
    else:
        return (s-w) + (s-h)

def create_train_kmeans(data, number_of_clusters):
    k = KMeans(n_clusters=number_of_clusters, n_jobs=2, random_state=0)
    k.fit(data)
    return k

directory = sys.argv[1]
cluster = int(sys.argv[2])

R    = []
Rabs = []

for dir_path, subdir_list, file_list in os.walk(directory):
    for fname in file_list:
        fullpath = os.path.join(dir_path, fname)
        rgb = cv2.imread(fullpath)
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        R.append(coeff(w, h, False))
        Rabs.append(coeff(w, h, True))

I = numpy.zeros(len(R))
Z = numpy.array(zip(I, R))
Zabs = numpy.array(zip(I, Rabs))

k = create_train_kmeans(Z, cluster)
kabs = create_train_kmeans(Zabs, cluster)

Z = []
for r in R:
    p = k.predict([[0, r]])[0]
    Z.append(p)

Zabs = []
for r in Rabs:
    p = kabs.predict([[0, r]])[0]
    Zabs.append(p)

plt.subplot(221)
plt.title('Coeff')
plt.plot(R)

plt.subplot(222)
plt.title('Cluster ' + str(cluster))
plt.bar(range(len(Z)), Z)

plt.subplot(223)
plt.title('Coeff (abs)')
plt.plot(Rabs)

plt.subplot(224)
plt.title('Cluster (abs) ' + str(cluster))
plt.bar(range(len(Zabs)), Zabs)

plt.show()
