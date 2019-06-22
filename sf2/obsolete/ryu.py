import random
import time
import sys
import os

import cv2
import mss
import numpy
from PIL import Image

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

def jumpRight(winid):
    os.system('xdotool key --window ' + winid + ' keydown Right')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' key Up')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' keyup Right')

def jumpLeft(winid):
    os.system('xdotool key --window ' + winid + ' keydown Left')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' key Up')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' keyup Left')

def jumpUp(winid):
    os.system('xdotool key --window ' + winid + ' key Up')

def down(winid):
    os.system('xdotool key --window ' + winid + ' keydown Left keydown Down')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' keyup Left keyup Down')

def defend(winid, pos):
    print pos
    if pos == 0:
        for i in range(0, 2):
            left(winid)
    elif pos == 1:
        for i in range(0, 2):
            right(winid)

def ryuMove(winid, smack, pos):

    r = random.choice([0, 1, 2])
    s = random.sample([0, 1, 2, 3], 3)

    print r, s, smack, " - ",

    if r == 0:
        for i in s:

            if smack > 0:
                defend(winid, pos)

            if i % 2 == 0:
                for z in range(0, i):
                    left(winid)
                    if z % 2 == 0:
                        kick(winid)
                    elif z % 3 == 0:
                        jumpLeft(winid)

                superkick(winid, pos)

            else:
                for z in range(0, i):
                    right(winid)
                    if z % 2 == 0:
                        punch(winid)       
                    elif z % 3 == 0:
                        jumpUp(winid)

                superpunch(winid, pos)

    elif r == 1:
        for i in s:

            if smack > 0:
                defend(winid, pos)

            if i % 2 == 0:
                for z in range(0, i):
                    punch(winid)

            else:
                for z in range(0, i):
                    kick(winid)

        jumpLeft(winid)

    elif r == 2: 
        fire(winid, pos)

        for i in s:

            if smack > 0:
                defend(winid, pos)
 
            if i % 2 == 0:
                for z in range(0, i):
                    if i % 2 == 0:
                        jumpRight(winid)
                        down(winid)
                    else:
                        jumpLeft(winid)
                        down(winid)
            else:
                for z in range(0, i):
                    down(winid)

        downKick(winid)

    time.sleep(0.29)

def loadTemplate(filename):
    return cv2.imread(filename, 0)

def findMatch(background, template, threshold):
    img_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = numpy.where(result >= threshold)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

    if len(loc[0]) > 1:
        return True

prevBlood = 0

def smacked(img):
    global prevBlood

    sm_pil = Image.fromarray(img)
    sm_crop = sm_pil.crop((20, 66, 236, 78))
    sm_np = numpy.asarray(sm_crop)

    b = sm_np[:, :, 0]
    g = sm_np[:, :, 1]
    ssum = numpy.sum(b.ravel()) + numpy.sum(g.ravel())

    current = ((float(ssum)))
    sub = numpy.sqrt(prevBlood - current)
    if current != prevBlood:
        print 'Smacked: ' + str(sub) 
    prevBlood = current

    return sub
    #import scipy.misc
    #scipy.misc.imsave(str(int(time.time())) + '.png', im_np)

def grab(width, height, left, top):

    with mss.mss() as sct:

        winid = sys.argv[1]
        focus(winid)

        monitor = {"top": top, "left": left, "width": width, "height": height}

        ryul_t = loadTemplate('tmpl/ryu/ryul.png')
        ryur_t = loadTemplate('tmpl/ryu/ryur.png')

        while [ 1 ]:
            last_time = time.time()

            imgorg = sct.grab(monitor)
            img = numpy.array(imgorg)

            if findMatch(img, ryul_t, 0.8):
                print '[]'
                s = smacked(img)
                ryuMove(winid, s, 0)
            elif findMatch(img, ryur_t, 0.8):
                print '[R]'
                s = smacked(img)
                ryuMove(winid, s, 1)

grab(580, 466, 110, 100)
