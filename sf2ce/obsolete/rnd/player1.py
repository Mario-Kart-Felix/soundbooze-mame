import random
import time
import sys
import os

winid = sys.argv[1]

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

def fire(winid):
    os.system('xdotool key --window ' + winid + ' keydown Down')
    os.system('xdotool key --window ' + winid + ' keydown Right')
    os.system('xdotool key --window ' + winid + ' keyup Down')
    os.system('xdotool key --window ' + winid + ' keydown D')
    os.system('xdotool key --window ' + winid + ' keyup Right')
    os.system('xdotool key --window ' + winid + ' keyup D')

def superkick(winid):
    os.system('xdotool key --window ' + winid + ' keydown Down')
    os.system('xdotool key --window ' + winid + ' keydown Left')
    os.system('xdotool key --window ' + winid + ' keyup Down')
    os.system('xdotool key --window ' + winid + ' keydown C')
    os.system('xdotool key --window ' + winid + ' keyup Left')
    os.system('xdotool key --window ' + winid + ' keyup C')

def superpunch(winid):
    os.system('xdotool key --window ' + winid + ' keydown Right')
    os.system('xdotool key --window ' + winid + ' keydown Down')

    os.system('xdotool key --window ' + winid + ' keyup Right')
    os.system('xdotool key --window ' + winid + ' keyup Down')

    os.system('xdotool key --window ' + winid + ' keydown Down')
    os.system('xdotool key --window ' + winid + ' keydown Right')

    os.system('xdotool key --window ' + winid + ' keyup Down')
    os.system('xdotool key --window ' + winid + ' keydown D')
    os.system('xdotool key --window ' + winid + ' keyup Right')
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

                superkick(winid)

            else:
                for z in range(0, i):
                    right(winid)
                    if z % 2 == 0:
                        punch(winid)       
                    elif z % 3 == 0:
                        jumpUp(winid)

                superpunch(winid)       

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
