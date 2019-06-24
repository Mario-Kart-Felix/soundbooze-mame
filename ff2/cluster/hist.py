import sys
import numpy
import matplotlib.pyplot as plt
import argparse
import cv2
import mss

fig, ax = plt.subplots()
ax.set_title('Histogram (RGB)')
ax.set_xlabel('Bin')
ax.set_ylabel('Frequency')

bins, lw, alpha = 16, 3, 0.5
lineR, = ax.plot(numpy.arange(bins), numpy.zeros((bins,)), c='r', lw=lw, alpha=alpha, label='Red')
lineG, = ax.plot(numpy.arange(bins), numpy.zeros((bins,)), c='g', lw=lw, alpha=alpha, label='Green')
lineB, = ax.plot(numpy.arange(bins), numpy.zeros((bins,)), c='b', lw=lw, alpha=alpha, label='Blue')
ax.set_xlim(0, bins-1)
ax.set_ylim(0, 1)
ax.legend()
plt.ion()
plt.show()

with mss.mss() as sct:

    full = {"top": 124, "left": 100, "width": 800, "height": 600+24}

    while [1]:
        frame = numpy.array(sct.grab(full))
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        numPixels = numpy.prod(frame.shape[:2])
        (b, g, r, a) = cv2.split(frame)
        histogramR = cv2.calcHist([r], [0], None, [bins], [0, 255]) / numPixels
        histogramG = cv2.calcHist([g], [0], None, [bins], [0, 255]) / numPixels
        histogramB = cv2.calcHist([b], [0], None, [bins], [0, 255]) / numPixels

        lineR.set_ydata(histogramR)
        lineG.set_ydata(histogramG)
        lineB.set_ydata(histogramB)
        fig.canvas.draw()

        '''
        cv2.imshow('RGB', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        '''
