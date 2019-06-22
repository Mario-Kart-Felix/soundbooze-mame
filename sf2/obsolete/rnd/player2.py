import random
import time
import sys
import os

winid = sys.argv[1]

def focus(winid):
    os.system('xdotool windowfocus --sync ' + winid)

def kick(winid):
    for i in range(0,2):
        os.system('xdotool key --window ' + winid + ' key M')

def downKick(winid):
    os.system('xdotool key --window ' + winid + ' keydown K')
    for i in range(0,2):
        os.system('xdotool key --window ' + winid + ' key M')
    os.system('xdotool key --window ' + winid + ' keyup K')

def punch(winid):
    for i in range(0,2):
        os.system('xdotool key --window ' + winid + ' key N')

def left(winid):
    os.system('xdotool key --window ' + winid + ' keydown J')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' keyup J')

def right(winid):
    os.system('xdotool key --window ' + winid + ' keydown L')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' keyup L')

def fire(winid):
    os.system('xdotool key --window ' + winid + ' keydown K')
    os.system('xdotool key --window ' + winid + ' keydown L')
    os.system('xdotool key --window ' + winid + ' keydown N')

    time.sleep(0.1)

    os.system('xdotool key --window ' + winid + ' keydown K')
    os.system('xdotool key --window ' + winid + ' keydown L')
    os.system('xdotool key --window ' + winid + ' keydown N')

def jumpRight(winid):
    os.system('xdotool key --window ' + winid + ' keydown L')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' key I')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' keyup L')

def jumpLeft(winid):
    os.system('xdotool key --window ' + winid + ' keydown J')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' key I')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' keyup J')

def jumpUp(winid):
    os.system('xdotool key --window ' + winid + ' key I')

def down(winid):
    os.system('xdotool key --window ' + winid + ' keydown J keydown J')
    time.sleep(0.1)
    os.system('xdotool key --window ' + winid + ' keyup J keyup K')

focus(winid)

# opflow, orb, templateMatch
# distance
# attack, defense, relax, 
# check blood, check Position (tmplFace)

while [ 1 ]:

    r = random.choice([0, 1, 2])
    s = random.sample([0, 1, 2, 3], 3)

    if r == 0:
        for i in s:
            if i % 2 == 0:
                for z in range(0, i):
                    left(winid)
                    if z % 2 == 0:
                        kick(winid)
                    elif z % 3 == 0:
                        jumpLeft(winid)

                kick(winid)

            else:
                for z in range(0, i):
                    right(winid)
                    if z % 2 == 0:
                        punch(winid)       
                    elif z % 3 == 0:
                        jumpUp(winid)

                punch(winid)       

    elif r == 1:
        for i in s:
            if i % 2 == 0:
                for z in range(0, i):
                    punch(winid)

            else:
                for z in range(0, i):
                    kick(winid)

        jumpLeft(winid)

    elif r == 2: 
        fire(winid)

        for i in s:
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
