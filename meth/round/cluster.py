import numpy
import random
import pickle
import sys

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def create_train_kmeans(data, number_of_clusters):
    k = KMeans(n_clusters=number_of_clusters, n_jobs=2, random_state=0)
    k.fit(data)
    return k

h = sys.argv[1]
H = numpy.load(h)
I = numpy.zeros(len(H))
Z = numpy.array(zip(I, H))

cluster = int(sys.argv[2])
k = create_train_kmeans(Z, cluster)

Z = []
for i in H:
    p = k.predict([[0, i]])[0]
    Z.append(p)

plt.subplot(211)
plt.plot(Z)
plt.subplot(212)
plt.bar(range(len(Z)), Z)
plt.show()
