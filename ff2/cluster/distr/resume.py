import subprocess
import numpy
import cv2
import time
import mss
import os

INSERT = [1059132, 1055681]
SELECT = [831168, 764772]
INTRO  = [508206, 510494]

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600-border}
    scene = {"top": 260+border, "left": 100, "width": 800, "height":424-border}

    cmd = "xdotool search --pid `pgrep mame`"
    r =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    v = r.read()
    winid = hex(int(v.decode()))
    os.system('xdotool windowfocus --sync ' + winid)

    while [ 1 ]:

        p1 = numpy.array(sct.grab(blood))
        p2 = p1.copy()

        b1 = p1[48:56, 120:359]
        b2 = p2[48:56, 120+321:359+321]

        sumb1 = numpy.sum(b1)
        sumb2 = numpy.sum(b2)

        if sumb1 == INSERT[0] and sumb2 == INSERT[1]:
            print '[Insert]'
            time.sleep(1)
            os.system('xdotool key --window ' + winid + ' keydown 5')
            time.sleep(0.2)
            os.system('xdotool key --window ' + winid + ' keyup 5')
            time.sleep(0.2)
            os.system('xdotool key --window ' + winid + ' keydown 1')
            time.sleep(0.2)
            os.system('xdotool key --window ' + winid + ' keyup 1')

        elif sumb1 == SELECT[0] and sumb2 == SELECT[1]:
            print '[Select]'
            time.sleep(1)
            os.system('xdotool key --window ' + winid + ' keydown A')
            time.sleep(0.2)
            os.system('xdotool key --window ' + winid + ' keyup A')
            time.sleep(2)

        elif sumb1 == INTRO[0] and sumb2 == INTRO[1]:
            print '[Intro]'
            time.sleep(1)
            os.system('xdotool key --window ' + winid + ' keydown A')
            time.sleep(0.2)
            os.system('xdotool key --window ' + winid + ' keyup A')
            time.sleep(2)
