import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
import cv2
import mss

'''

# Full
_, width, height, left, top = query()

'''

'''
# horizontal, 60-height

player = 'Mid'
width = 542
height = 60
left = 106
top = 364
'''

# Static bg scene

player = '1'
left = 248

if sys.argv[1] == '1':
    player = '1'
    left  = 248 #p1
elif sys.argv[1] == '2':
    player = '2'
    left  = 248+165 #p2

top = 183
width = 197
height = 12

fig, ax = plt.subplots()
ax.set_title('Histogram (grayscale)')
ax.set_xlabel('Bin')
ax.set_ylabel('Frequency')

bins=16
lw = 3
alpha = 0.5
lineGray, = ax.plot(np.arange(bins), np.zeros((bins,1)), c='k', lw=lw, label='intensity')
ax.set_xlim(0, bins-1)
ax.set_ylim(0, 1)
ax.legend()
plt.ion()
plt.show()

def getFrame():
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        frame = np.array(sct.grab(monitor))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return gray

while True:
    gray = getFrame()
    numPixels = np.prod(gray.shape[:2])
    hist = cv2.calcHist([gray], [0], None, [bins], [0, 255]) / numPixels
    s = skew(hist)
    k = kurtosis(hist)#, fisher=False)
    v = np.var(hist)
    hsum = np.sum(hist)/100.0
    m = (s + k + v + hsum) / 4

    print 'P' + player, 
    print ("%.5f"% (s)),
    print ("%.5f"% (hsum)),
    print ("%.5f"% (v)),
    print ("%.5f"% (k)),
    print ("(%.5f)"% (m))

    '''
    if len(sys.argv) == 2:
        lineGray.set_ydata(hist)
        fig.canvas.draw()
    '''

    #cv2.imshow('Gray', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
