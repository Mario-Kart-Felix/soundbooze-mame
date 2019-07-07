import subprocess
import numpy
import time
import mss
import cv2
import os

RESUME = [1358640, 2617406, 2264400, 2623509]

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600}
    scene = {"top": 240+border, "left": 100, "width": 800, "height":400}

    cmd             = "xdotool search --pid `pgrep mame`"
    r               =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    v               = r.read()
    winid           = hex(int(v.decode()))
    os.system('xdotool windowfocus --sync ' + winid)

    while [ 1 ]:

        p1 = numpy.array(sct.grab(blood))
        p2 = p1.copy()

        b1 = p1[60:78, 68:364]
        b2 = p2[60:78, 68+366:364+366]
        ko = p1[60:80, 378:424]

        sumb1, sumb2, kosum = numpy.sum(b1), numpy.sum(b2), numpy.sum(ko)

        if sumb1 == RESUME[0]:
            os.system('xdotool key --window ' + winid + ' keydown 5')
            time.sleep(0.2)
            os.system('xdotool key --window ' + winid + ' keyup 5')
            time.sleep(0.2)
            os.system('xdotool key --window ' + winid + ' key 1')
        
        elif sumb1 == RESUME[1] or sumb1 == RESUME[2] or sumb1 == RESUME[3]:
            time.sleep(0.2)
            os.system('xdotool key --window ' + winid + ' key A')

        time.sleep(0.3)
