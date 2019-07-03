import sys
import cv2 
from scipy.stats import skew
import matplotlib.pyplot as plt

def histSkew(img):

    (b, g, r) = cv2.split(img)
    histb = cv2.calcHist([b],[0],None,[256],[0,256]) 
    histg = cv2.calcHist([g],[0],None,[256],[0,256]) 
    histr = cv2.calcHist([r],[0],None,[256],[0,256]) 

    plt.subplot(411)
    sb = skew(histb)[0]
    plt.title('B ' + str(sb))
    plt.plot(histb, color='blue')

    plt.subplot(412)
    sg = skew(histg)[0]
    plt.title('G ' + str(sg))
    plt.plot(histg, color='green')

    plt.subplot(413)
    sr = skew(histr)[0]
    plt.title('R ' + str(sr))
    plt.plot(histr, color='red')

    plt.subplot(414)
    S = [sb, sg, sr]
    I = range(len(S))
    plt.title('Skewness RGB')
    plt.bar(I, S)

    color = ['blue', 'green', 'red']
    for i, c in zip(range(len(color)), color):
      plt.bar(I[i],S[i],color=c)

    plt.show()

img = cv2.imread(sys.argv[1])
histSkew(img)
