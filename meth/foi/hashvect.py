# -*- coding: utf-8 -*-

import cv2
import mss
import numpy
import PIL
import imagehash

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

class CLUSTER:

    def __init__(self):

        self.vectorizer = HashingVectorizer(n_features=2**4)
        self.H = {}
        self.model = None
        self.period = 1000

    def fit(self, size):
        H = []
        for k in self.H.keys():
            H.append(k)

        true_k = size
        X = self.vectorizer.fit_transform(H)
        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
        model.fit(X)
        self.model = model

    def append(self, h):
        self.H[h] = h

    def predict(self, h):
        Y = self.vectorizer.transform([h])
        prediction = self.model.predict(Y)
        return prediction

class TRANSFORM:

    def __init__(self):
        self.b = None

    def blue(self, frame):
        self.b = frame
        self.b[:,:,1] = 0
        self.b[:,:,2] = 0
        self.b[self.b < 250] = 0
        return self.b

    def phash(self, frame):
        phash = str(imagehash.phash(frame))
        return phash

if __name__ == '__main__':

    with mss.mss() as sct:

        body = {"top": 324, "left": 100, "width": 800, "height": 400}

        cluster = CLUSTER()
        transform = TRANSFORM()

        i = 0
        while [ 1 ]:

            frame = numpy.array(sct.grab(body))
            h = transform.phash(PIL.Image.fromarray(transform.blue(numpy.array(sct.grab(body)))))
            cluster.append(h)

            if i != 0 and i % cluster.period == 0:
                cluster.fit(10)

            if cluster.model is not None:
                p = cluster.predict(h)
                print len(cluster.H), '[', p[0], ']', h

            i+=1
