import matplotlib.pyplot as plt
from scipy import ndimage
from sklearn import cluster
import sys

image = ndimage.imread(sys.argv[1])

x, y, z = image.shape
image_2d = image.reshape(x*y, z)

print image_2d.shape

kmeans_cluster = cluster.KMeans(n_clusters=int(sys.argv[2]))
kmeans_cluster.fit(image_2d)
cluster_centers = kmeans_cluster.cluster_centers_
cluster_labels = kmeans_cluster.labels_

plt.imshow(cluster_centers[cluster_labels].reshape(x, y, z))
plt.show()

#python single file.png 4
