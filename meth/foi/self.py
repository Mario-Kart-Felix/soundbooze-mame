import numpy
import cv2
import sys

from sklearn.cluster import KMeans

from matplotlib import pyplot as plt
import seaborn as sns; sns.set()

def hinton(matrix, max_weight=None, ax=None):
    ax = ax if ax is not None else plt.gca()

    if not max_weight:
        max_weight = 2 ** numpy.ceil(numpy.log(numpy.abs(matrix).max()) / numpy.log(2))

    ax.patch.set_facecolor('gray')
    ax.set_aspect('equal', 'box')
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())

    for (x, y), w in numpy.ndenumerate(matrix):
        color = 'white' if w > 0 else 'black'
        size = numpy.sqrt(numpy.abs(w) / max_weight)
        rect = plt.Rectangle([x - size / 2, y - size / 2], size, size,
                             facecolor=color, edgecolor=color)
        ax.add_patch(rect)

    ax.autoscale_view()
    ax.invert_yaxis()

def create_train_kmeans(data, number_of_clusters):
    k = KMeans(n_clusters=number_of_clusters, n_jobs=2, random_state=0)
    k.fit(data)
    return k

rgb = cv2.imread(sys.argv[1])
h, w, _ = rgb.shape
rgb = cv2.resize(rgb, (w/4,h/4))
h, w, _ = rgb.shape
B, G, R = cv2.split(rgb)

B = numpy.array(B).ravel()
G = numpy.array(G).ravel()
R = numpy.array(R).ravel()

BGR = []
for b, g, r in zip(B, G, R):
    BGR.append([b, g, r])
    #BGR.append([g, r])
    #BGR.append([0, r])

cluster = int(sys.argv[2])
k = create_train_kmeans(BGR, cluster)

Z = []
for r in BGR:
    p = k.predict([r])[0]
    Z.append(p)

Z = numpy.array(Z).reshape(h, w)

'''
sns.heatmap(Z, cmap="YlGnBu")
plt.show()

plt.imshow(Z)
plt.show()
'''

hinton(Z.transpose())
plt.show()
