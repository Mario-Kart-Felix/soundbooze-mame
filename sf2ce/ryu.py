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

    def act(self, r):
        if r == 0:
          self.punch()
        elif r == 1:
          self.kick()
        elif r == 2:
          self.downkick()
        elif r == 3:
          self.kick()
          self.right()
          self.kick()
        elif r == 4:
          self.kick()
          self.jumpup()
          self.kick()
        elif r == 5:
          self.jumpleft(0.6)
          self.kick()
        elif r == 6:
          self.jumpright(0.6)
          self.kick()
        elif r == 7:
          self.fire(0)
        elif r == 8:
          self.fire(1)
        elif r == 9:
          self.superpunch(0)
        elif r == 10:
          self.superpunch(1)
        elif r == 11:
          self.superkick(0)
        elif r == 12:
          self.superkick(1)
        elif r == 13:
          self.defendup(0)
        elif r == 14:
          self.defendup(1)
        elif r == 15:
          self.defenddown(0)
        elif r == 16:
          self.defenddown(1)

    def insertcoin(self):
        os.system('xdotool key --window ' + self.winid + ' keydown 5')
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' keyup 5')
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' key 1')

    def select(self):
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' key A')
