import os
import sys
import cv2
import mss
import numpy
import time
import random
from scipy.stats import skew, kurtosis
from scipy.signal import find_peaks

from PIL import Image
from PIL import ImageFilter

def focus(winid):
    os.system('xdotool windowfocus --sync ' + winid)

def kick(winid):
    for i in range(0,2):
        os.system('xdotool key --window ' + winid + ' key C')

def downKick(winid):
    os.system('xdotool key --window ' + winid + ' keydown Down')
    for i in range(0,2):
        os.system('xdotool key --window ' + winid + ' key C')
    os.system('xdotool key --window ' + winid + ' keyup Down')

def punch(winid):
    for i in range(0,2):
        os.system('xdotool key --window ' + winid + ' key D')

def left(winid):
    os.system('xdotool key --window ' + winid + ' keydown Left')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' keyup Left')

def right(winid):
    os.system('xdotool key --window ' + winid + ' keydown Right')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' keyup Right')

def fire(winid, pos):
    z = "Right"
    if pos == 0:
        z = "Right"
    else:
        z = "Left"

    os.system('xdotool key --window ' + winid + ' keydown Down')
    os.system('xdotool key --window ' + winid + ' keydown ' + z)
    os.system('xdotool key --window ' + winid + ' keyup Down')
    os.system('xdotool key --window ' + winid + ' keydown D')
    os.system('xdotool key --window ' + winid + ' keyup ' + z)
    os.system('xdotool key --window ' + winid + ' keyup D')

def superkick(winid, pos):
    z = "Left"
    if pos == 0:
        z = "Left"
    else:
        z = "Right"

    os.system('xdotool key --window ' + winid + ' keydown Down')
    os.system('xdotool key --window ' + winid + ' keydown ' + z)
    os.system('xdotool key --window ' + winid + ' keyup Down')
    os.system('xdotool key --window ' + winid + ' keydown C')
    os.system('xdotool key --window ' + winid + ' keyup ' + z)
    os.system('xdotool key --window ' + winid + ' keyup C')

def superpunch(winid, pos):
    z = "Right"
    if pos == 0:
        z = "Right"
    else:
        z = "Left"

    os.system('xdotool key --window ' + winid + ' keydown ' + z)
    os.system('xdotool key --window ' + winid + ' keydown Down')

    os.system('xdotool key --window ' + winid + ' keyup ' + z)
    os.system('xdotool key --window ' + winid + ' keyup Down')

    os.system('xdotool key --window ' + winid + ' keydown Down')
    os.system('xdotool key --window ' + winid + ' keydown ' + z)

    os.system('xdotool key --window ' + winid + ' keyup Down')
    os.system('xdotool key --window ' + winid + ' keydown D')
    os.system('xdotool key --window ' + winid + ' keyup ' + z)
    os.system('xdotool key --window ' + winid + ' keyup D')

def calcHistogram(img):

    num = numpy.prod(img.shape[:2])
    hist = cv2.calcHist([img], [0], None, [16], [0, 255]) / num
    s = skew(hist)
    k = kurtosis(hist)
    v = numpy.var(hist)
    hsum = numpy.sum(hist)/100.0
    m = (s + k + v + hsum) / 4
    return hsum, m 

def grab():

    with mss.mss() as sct:

        winid = sys.argv[1]
        focus(winid)

        monitor = {"top": 600, "left": 100, "width": 800, "height": 100}
        subtractor = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=25, detectShadows=True)

        while [ 1 ]:

            frame = numpy.array(sct.grab(monitor))
            mask = subtractor.apply(frame)
            blur = cv2.GaussianBlur(mask,(5,5),0)

            pil_img = Image.fromarray(blur)
            edge = numpy.array(pil_img.filter(ImageFilter.FIND_EDGES))
            edgecv = cv2.cvtColor(numpy.array(edge), cv2.COLOR_RGB2BGR)

            blursum = (numpy.sum(blur)/1000000.0)
            hsum, m = calcHistogram(blur)

            HS=[]
            if m > 0:
                if blursum > 0.0 and blursum < 1.8:
                    H = numpy.hsplit(blur, 8)
                    for h in H:
                        sk = numpy.sum(h)/1000000.0
                        if sk < 0.3:
                            print ("%.5f"% (sk)),
                            HS.append(sk)
                        else:
                            HS.append(0)
                            print ("%.5f"% (0)),

                    L = HS[0]+HS[1]+HS[2]+HS[3]
                    R = HS[4]+HS[5]+HS[6]+HS[7]

                    if L < R:
                        fire(winid, 0)
                        fire(winid, 1)
                    elif R < L:
                        superkick(winid, 0)
                        superkick(winid, 1)

                    print ("%.5f"% (L)),
                    print ("%.5f"% (R))

            '''
            cv2.imshow("Blur", edgecv)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
            '''

grab()
