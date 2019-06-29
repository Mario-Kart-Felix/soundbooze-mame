import os
import sys
import cv2
import numpy

import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def scale(img):
    scaler = StandardScaler()
    scaler.fit(img)
    scaled_img = scaler.transform(img)
    return scaled_img

def scatter(X):
    plt.scatter(X[:, 0], X[:, 1])
    plt.xlabel("Feature 0")
    plt.ylabel("Feature 1")
    plt.show()

def reconstruct(x, pca, lowerdimension):
    approximation = pca.inverse_transform(lowerdimension)
    approximation = approximation.reshape(600,800)
    X_norm = x.reshape(600,800)

    plt.subplot(211)
    plt.imshow(X_norm)
    plt.subplot(212)
    plt.imshow(approximation)
    plt.show()

def ppccaa(X):
    pca = PCA(.95)
    px = pca.fit_transform(X)
    pxva = pca.explained_variance_
    pxratio = pca.explained_variance_ratio_
    print px
    print px.shape
    scatter(px)
    reconstruct(x, pca, px)

def ddbbssccaann(X):
    dbscan = DBSCAN(eps=0.123, min_samples=2)
    clusters = dbscan.fit_predict(x)
    print clusters
    plt.plot(clusters)
    plt.show()
    '''
    plt.scatter(x[:, 0], x[:, 1], c=clusters, cmap="plasma")
    plt.xlabel("Feature 0")
    plt.ylabel("Feature 1")
    plt.show()
    '''

def dbsum(S):
    C = []
    dbscan = DBSCAN(eps=0.123, min_samples=2)
    for s in S:
        clusters = dbscan.fit_predict(s)
        C.append(clusters)
    return C

def dbsumabs(S):
    C = []
    dbscan = DBSCAN(eps=0.123, min_samples=2)
    for s in S:
        clusters = dbscan.fit_predict(s)
        C.append(numpy.absolute(clusters))
    return C

def load(d):
    I = []
    for dir_path, subdir_list, file_list in os.walk(d):
        for fname in file_list:
            i = cv2.imread(d + fname, 0)
            I.append(i)
    return I

I = load(sys.argv[1])
S = []

for i in I:
    S.append(StandardScaler().fit_transform(i))

C = dbsum(S)
CA = dbsumabs(S)

n = numpy.sum(C, axis=0)
na = numpy.sum(CA, axis=0)

plt.subplot(211)
plt.plot(n)
plt.subplot(212)
plt.plot(na)
plt.show()

#ppccaa(x)
#ddbbssccaann(x)
