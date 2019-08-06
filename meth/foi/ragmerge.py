"""
===========
RAG Merging
===========

This example constructs a Region Adjacency Graph (RAG) and progressively merges
regions that are similar in color. Merging two adjacent regions produces
a new region with all the pixels from the merged regions. Regions are merged
until no highly similar region pairs remain.

https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_rag_merge.html#sphx-glr-auto-examples-segmentation-plot-rag-merge-py

"""

import cv2
import mss
import time
import numpy

from skimage import data, io, segmentation, color
from skimage.future import graph
import numpy as np

def _weight_mean_color(graph, src, dst, n):
    diff = graph.node[dst]['mean color'] - graph.node[n]['mean color']
    diff = np.linalg.norm(diff)
    return {'weight': diff}


def merge_mean_color(graph, src, dst):
    graph.node[dst]['total color'] += graph.node[src]['total color']
    graph.node[dst]['pixel count'] += graph.node[src]['pixel count']
    graph.node[dst]['mean color'] = (graph.node[dst]['total color'] /
                                     graph.node[dst]['pixel count'])


with mss.mss() as sct:

    full = {"top": 124, "left": 100, "width": 800, "height": 600}

    global lc

    while [ 1 ]:

        img = numpy.array(sct.grab(full))
        img = cv2.resize(img, (200, 150))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        labels = segmentation.slic(img, compactness=10, n_segments=100) #30 400
        g = graph.rag_mean_color(img, labels)

        labels2 = graph.merge_hierarchical(labels, g, thresh=35, rag_copy=False,
                                           in_place_merge=True,
                                           merge_func=merge_mean_color,
                                           weight_func=_weight_mean_color)

        out = color.label2rgb(labels2, img, kind='avg')
        out = segmentation.mark_boundaries(out, labels2, (0, 0, 0))

        cv2.imshow("1", out)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
