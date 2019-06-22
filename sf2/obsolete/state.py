import os
import sys
import time
import cv2
import mss
import numpy
from winid import *

def loadTemplate(filename):
    return cv2.imread(filename, 0)

def findMatch(background, template, threshold):
    img_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = numpy.where(result >= threshold)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

    if len(loc[0]) > 1:
        return True

def grab(winid, width, height, left, top):

    with mss.mss() as sct:

        monitor = {"top": top, "left": left, "width": width, "height": height}

        ryul_t = loadTemplate('tmpl/ryu/ryul.png')
        ryur_t = loadTemplate('tmpl/ryu/ryur.png')
        sitl_t = loadTemplate('tmpl/ryu/sitl.png')
        sitr_t = loadTemplate('tmpl/ryu/sitr.png')

        defdl_t = loadTemplate('tmpl/ryu/defdl.png')
        deful_t = loadTemplate('tmpl/ryu/deful.png')
        defdr_t = loadTemplate('tmpl/ryu/defdr.png')
        defur_t = loadTemplate('tmpl/ryu/defur.png')

        blank1_t = loadTemplate('tmpl/ryu/blank1.png')
        blank2_t = loadTemplate('tmpl/ryu/blank2.png')

        wina_t = loadTemplate('tmpl/ryu/wina.png')
        winb_t = loadTemplate('tmpl/ryu/winb.png')
        winc_t = loadTemplate('tmpl/ryu/winc.png')
        wind_t = loadTemplate('tmpl/ryu/wind.png')

        champ_t = loadTemplate('tmpl/ryu/champ.png')

        ko_t = loadTemplate('tmpl/ko.png')

        select_t = loadTemplate('tmpl/select.png')
        continue_t = loadTemplate('tmpl/continue.png')

        bonus1a_t = loadTemplate('tmpl/bonus/1/a.png')
        bonus1b_t = loadTemplate('tmpl/bonus/1/b.png')
        bonus2a_t = loadTemplate('tmpl/bonus/2/a.png')
        bonus3a_t = loadTemplate('tmpl/bonus/3/a.png')

        while [ 1 ]:

            img = numpy.array(sct.grab(monitor))

            if findMatch(img, ryul_t, 0.8):
                print 'Idle L', time.time()
            elif findMatch(img, ryur_t, 0.8):
                print 'Idle R', time.time()
            elif findMatch(img, sitl_t, 0.8):
                print 'Sit L', time.time()
            elif findMatch(img, sitr_t, 0.8):
                print 'Sit R', time.time()

            elif findMatch(img, deful_t, 0.8):
                print 'Def U L', time.time()
            elif findMatch(img, defdl_t, 0.8):
                print 'Def D L', time.time()
            elif findMatch(img, defur_t, 0.8):
                print 'Def U R ', time.time()
            elif findMatch(img, defdr_t, 0.8):
                print 'Def D L', time.time()

            elif findMatch(img, wina_t, 0.8):
                print '[Win]', time.time()
                time.sleep(6)
            elif findMatch(img, winb_t, 0.8):
                print '[Win]', time.time()
                time.sleep(6)
            elif findMatch(img, winc_t, 0.8):
                print '[Win]', time.time()
                time.sleep(6)
            elif findMatch(img, wind_t, 0.8):
                print '[Win]', time.time()
                time.sleep(6)

            elif findMatch(img, champ_t, 0.8):
                print '[Champion Winner]', time.time()

            elif findMatch(img, ko_t, 0.9):
                print '[KO]', time.time()
                time.sleep(6)

            elif findMatch(img, blank1_t, 0.6):
                print '[Blank]', time.time()
            elif findMatch(img, blank2_t, 0.6):
                print '[Blank]', time.time()

            elif findMatch(img, bonus1a_t, 0.8):
                print '[Bonus 1a]', time.time()
            elif findMatch(img, bonus1b_t, 0.8):
                print '[Bonus 1b]', time.time()
            elif findMatch(img, bonus2a_t, 0.8):
                print '[Bonus 2a]', time.time()
            elif findMatch(img, bonus3a_t, 0.8):
                print '[Bonus 3a]', time.time()

            elif findMatch(img, continue_t, 0.8):
                print '[Continue]', time.time()
                os.system('xdotool windowfocus --sync ' + winid)
                time.sleep(0.2)
                os.system('xdotool windowfocus --sync ' + winid)
                os.system('xdotool key --window ' + winid + ' keydown 5')
                time.sleep(0.2)
                os.system('xdotool key --window ' + winid + ' keyup 5')
                time.sleep(0.2)
                os.system('xdotool key --window ' + winid + ' key 1')

            elif findMatch(img, select_t, 0.8):
                print '[Player Select]', time.time()
                os.system('xdotool windowfocus --sync ' + winid)
                time.sleep(0.2)
                os.system('xdotool key --window ' + winid + ' key A')
                time.sleep(4)

            '''
            cv2.imshow("debug", img)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
            '''

wid, width, height, left, top = query()
grab(wid, width, height, left, top)
