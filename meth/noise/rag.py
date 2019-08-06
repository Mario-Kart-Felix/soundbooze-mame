# -*- coding: utf-8 -*-

import cv2
import mss
import time
import numpy

from skimage import data, io, segmentation, color
from skimage.future import graph

def _weight_mean_color(graph, src, dst, n):
    diff = graph.node[dst]['mean color'] - graph.node[n]['mean color']
    diff = numpy.linalg.norm(diff)
    return {'weight': diff}


def merge_mean_color(graph, src, dst):
    graph.node[dst]['total color'] += graph.node[src]['total color']
    graph.node[dst]['pixel count'] += graph.node[src]['pixel count']
    graph.node[dst]['mean color'] = (graph.node[dst]['total color'] /
                                     graph.node[dst]['pixel count'])


with mss.mss() as sct:

    body = {"top": 264, "left": 100, "width": 800, "height": 360}

    while [ 1 ]:

        blue = numpy.array(sct.grab(body))
        blue[:,:,1] = 0
        blue[:,:,2] = 0
        blue[blue < 250] = 0
        blue = cv2.resize(blue, (100, 45))
        blue = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
        blue[blue > 0] = 255

        labels = segmentation.slic(blue, compactness=10, n_segments=100) #30 400
        g = graph.rag_mean_color(blue, labels)

        labels2 = graph.merge_hierarchical(labels, g, thresh=35, rag_copy=False,
                                           in_place_merge=True,
                                           merge_func=merge_mean_color,
                                           weight_func=_weight_mean_color)

        out = color.label2rgb(labels2, blue, kind='avg')
        out = segmentation.mark_boundaries(out, labels2, (0, 0, 0))

        cv2.imshow("white", blue)
        cv2.imshow("Rag", out)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
