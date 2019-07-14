import subprocess
import random
import time
import os

class PLAYER:

    def __init__(self, l, r, up, down, jump, punch):
        cmd             = "xdotool search --pid `pgrep mame`"
        srp             =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        v               = srp.read()
        self.winid      = hex(int(v.decode()))
        os.system('xdotool windowfocus --sync ' + self.winid)

        self.l   = l
        self.r   = r
        self.u   = up
        self.d   = down
        self.j   = jump
        self.p   = punch

    def walk(self, s, d):

        key = self.r
        if d == 0:
            key = self.l
        elif d == 1:
            key = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)

        r = random.randint(0, 5)
        if r % 2 == 0:
            sl = random.randint(1, 2)
            self.up(float(sl/10.0))
        else:
            sl = random.randint(1, 2)
            self.down(float(sl/10.0))

        time.sleep(s)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)

    def up(self, s):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.u)
        time.sleep(s)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.u)

    def down(self, s):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        time.sleep(s)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)

    def jump(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.j)
        time.sleep(0.3)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.j)

    def jumpkick(self, pos):

        def _weight():
            numbers      = [0, 1]
            weightings   = [0.4, 0.6]
            choice = random.random()
            currentSum = 0.0
            for r in range(len(numbers)):
                currentSum += weightings[r]
                if (choice <= currentSum):
                    break
            return numbers[r]

        key = self.r 
        if pos == 0:
            key = self.r
        else:
            key = self.l

        r = _weight()

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.j)
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)

        if r % 2 == 0:
            os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)

        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.p)

        if r % 2 == 0:
            os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)

        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.j)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.p)

    def punch(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.p)
        time.sleep(0.3)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.p)

    def superkick(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.j)
        time.sleep(0.05)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.j)
        time.sleep(0.05)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.j)
        time.sleep(0.05)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.j)
        time.sleep(0.05)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.j)
        time.sleep(0.05)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.j)

    def resume(self):
        os.system('xdotool key --window ' + self.winid + ' keydown 5')
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' keyup 5')
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' key 1')
        os.system('xdotool key --window ' + self.winid + ' key 1')
        self.walk(0.1, 1)
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' key A')
