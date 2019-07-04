import subprocess
import time
import os

class TERRY:

    def __init__(self):
        cmd = "xdotool search --pid `pgrep mame`"
        r =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        v = r.read()
        self.winid = hex(int(v.decode()))
        os.system('xdotool windowfocus --sync ' + self.winid)

    def punch(self):
        os.system('xdotool key --window ' + self.winid + ' key D')

    def kick(self):
        os.system('xdotool key --window ' + self.winid + ' key F')

    def downpunch(self):
        os.system('xdotool key --window ' + self.winid + ' keydown Down')
        os.system('xdotool key --window ' + self.winid + ' key D')
        os.system('xdotool key --window ' + self.winid + ' keyup Down')

    def downkick(self):
        os.system('xdotool key --window ' + self.winid + ' keydown Down')
        os.system('xdotool key --window ' + self.winid + ' key F')
        os.system('xdotool key --window ' + self.winid + ' keyup Down')

    def left(self):
        os.system('xdotool key --window ' + self.winid + ' keydown Left')
        time.sleep(0.5)
        os.system('xdotool key --window ' + self.winid + ' keyup Left')

    def right(self):
        os.system('xdotool key --window ' + self.winid + ' keydown Right')
        time.sleep(0.5)
        os.system('xdotool key --window ' + self.winid + ' keyup Right')

    def shift(self, pos):
        key = "Left"
        if pos == 0:
            key = "Left"
        elif pos == 1:
            key = "Right"

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)

    def powerwave(self, pos):
        z = "Right"
        if pos == 0:
            z = "Right"
        else:
            z = "Left"

        os.system('xdotool key --window ' + self.winid + ' keydown Down')
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown D')
        os.system('xdotool key --window ' + self.winid + ' keyup Down')
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup D')

        time.sleep(0.1)

    def burnknuckle(self, pos):
        z = "Left"
        if pos == 0:
            z = "Left"
        else:
            z = "Right"

        os.system('xdotool key --window ' + self.winid + ' keydown Down')
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown D')
        os.system('xdotool key --window ' + self.winid + ' keyup Down')
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)

        time.sleep(0.1)

    def risingtackle(self, pos):
        z = "Left"
        if pos == 0:
            z = "Left"
        else:
            z = "Right"
        for i in range(0,42):
            os.system('xdotool key --window ' + self.winid + ' keydown ' + z + ' Down')
        os.system('xdotool key --window ' + self.winid + ' keydown Up')
        os.system('xdotool key --window ' + self.winid + ' keydown D')
        for i in range(0,42):
            os.system('xdotool key --window ' + self.winid + ' keyup ' + z + ' Down')
        os.system('xdotool key --window ' + self.winid + ' keyup Up')
        os.system('xdotool key --window ' + self.winid + ' keyup D')
        time.sleep(0.2)

    def crackshoot(self, pos):
        z = "Left"
        if pos == 0:
            z = "Left"
        else:
            z = "Right"

        for i in range(0,6):
            os.system('xdotool key --window ' + self.winid + ' keydown Down')
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown Up')
        os.system('xdotool key --window ' + self.winid + ' keydown F')
        for i in range(0,6):
            os.system('xdotool key --window ' + self.winid + ' keyup Down')
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup Up')
        os.system('xdotool key --window ' + self.winid + ' keyup F')

        time.sleep(0.1)

    def defendup(self, pos):
        key = "Left"
        if pos == 0:
            key = "Left"
        elif pos == 1:
            key = "Right"

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        time.sleep(0.6)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)

    def defenddown(self, pos):
        key = "Left"
        if pos == 0:
            key = "Left"
        elif pos == 1:
            key = "Right"

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keydown Down')
        time.sleep(0.6)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup Down')

    def jumpright(self):
        os.system('xdotool key --window ' + self.winid + ' keydown Right')
        os.system('xdotool key --window ' + self.winid + ' keydown Up F')
        time.sleep(0.5)
        os.system('xdotool key --window ' + self.winid + ' keyup Right')
        os.system('xdotool key --window ' + self.winid + ' keyup Up F')

    def jumpleft(self):
        os.system('xdotool key --window ' + self.winid + ' keydown Left')
        os.system('xdotool key --window ' + self.winid + ' keydown Up F')
        time.sleep(0.5)
        os.system('xdotool key --window ' + self.winid + ' keyup Left')
        os.system('xdotool key --window ' + self.winid + ' keyup Up F')

    def jumpup(self):
        os.system('xdotool key --window ' + self.winid + ' key Up')

    def insertcoin(self):
        time.sleep(1)
        os.system('xdotool key --window ' + self.winid + ' keydown 5')
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' keyup 5')
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' keydown 1')
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' keyup 1')

    def select(self):
        time.sleep(1)
        os.system('xdotool key --window ' + self.winid + ' keydown A')
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' keyup A')
        time.sleep(2)

    def intro(self):
        time.sleep(1)
        os.system('xdotool key --window ' + self.winid + ' keydown A')
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' keyup A')
        time.sleep(2)
