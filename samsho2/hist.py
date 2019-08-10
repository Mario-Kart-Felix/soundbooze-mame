import cv2
import numpy

class HIST:

    def compute(self, full):
        numPixels = numpy.prod(full.shape[:2])
        (b, g, r, a) = cv2.split(full)
        histogramR = cv2.calcHist([r], [0], None, [16], [0, 255]) / numPixels
        histogramG = cv2.calcHist([g], [0], None, [16], [0, 255]) / numPixels
        histogramB = cv2.calcHist([b], [0], None, [16], [0, 255]) / numPixels
        H = numpy.array([histogramR, histogramG, histogramB])
        return H.flatten()


