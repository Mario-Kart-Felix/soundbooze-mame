import subprocess
import time
import os

class RYU:

    def __init__(self):
        cmd = "xdotool search --pid `pgrep mame`"
        r =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        v = r.read()
        self.winid = hex(int(v.decode()))
        os.system('xdotool windowfocus --sync ' + self.winid)

    def kick(self):
        for i in range(0,2):
            os.system('xdotool key --window ' + self.winid + ' key C')

    def defendup(self, pos):
        key = "Left"
        if pos == 0:
            key = "Left"
        elif pos == 1:
            key = "Right"

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        time.sleep(0.3)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)

    def defenddown(self, pos):
        key = "Left"
        if pos == 0:
            key = "Left"
        elif pos == 1:
            key = "Right"

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keydown Down')
        time.sleep(0.3)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup Down')

    def downkick(self):
        os.system('xdotool key --window ' + self.winid + ' keydown Down')
        for i in range(0,2):
            os.system('xdotool key --window ' + self.winid + ' key C')
        os.system('xdotool key --window ' + self.winid + ' keyup Down')

    def punch(self):
        for i in range(0,2):
            os.system('xdotool key --window ' + self.winid + ' key D')

    def left(self):
        os.system('xdotool key --window ' + self.winid + ' keydown Left')
        time.sleep(0.7)
        os.system('xdotool key --window ' + self.winid + ' keyup Left')

    def right(self):
        os.system('xdotool key --window ' + self.winid + ' keydown Right')
        time.sleep(0.7)
        os.system('xdotool key --window ' + self.winid + ' keyup Right')

    def jumpright(self, s):
        os.system('xdotool key --window ' + self.winid + ' keydown Right')
        os.system('xdotool key --window ' + self.winid + ' keydown Up')
        time.sleep(s)
        os.system('xdotool key --window ' + self.winid + ' keyup Right')
        os.system('xdotool key --window ' + self.winid + ' keyup Up')

    def jumpleft(self, s):
        os.system('xdotool key --window ' + self.winid + ' keydown Left')
        os.system('xdotool key --window ' + self.winid + ' keydown Up')
        time.sleep(s)
        os.system('xdotool key --window ' + self.winid + ' keyup Left')
        os.system('xdotool key --window ' + self.winid + ' keyup Up')

    def jumpup(self):
        os.system('xdotool key --window ' + self.winid + ' key Up')

    def fire(self, pos):
        z = "Right"
        if pos == 0:
            z = "Right"
        else:
            z = "Left"

        os.system('xdotool key --window ' + self.winid + ' keydown Down')
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup Down')
        os.system('xdotool key --window ' + self.winid + ' keydown D')
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup D')

    def superkick(self, pos):
        z = "Left"
        if pos == 0:
            z = "Left"
        else:
            z = "Right"

        os.system('xdotool key --window ' + self.winid + ' keydown Down')
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup Down')
        os.system('xdotool key --window ' + self.winid + ' keydown C')
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup C')

    def superpunch(self, pos):
        z = "Right"
        if pos == 0:
            z = "Right"
        else:
            z = "Left"

        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown Down')

        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup Down')

        os.system('xdotool key --window ' + self.winid + ' keydown Down')
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)

        os.system('xdotool key --window ' + self.winid + ' keyup Down')
        os.system('xdotool key --window ' + self.winid + ' keydown D')
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup D')

    def insertcoin(self):
        os.system('xdotool key --window ' + self.winid + ' keydown 5')
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' keyup 5')
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' key 1')

    def select(self):
        time.sleep(1)
        os.system('xdotool key --window ' + self.winid + ' key A')
        time.sleep(1)
