import subprocess
import time
import os

class RYU:

    def __init__(self, l, r, up, down, kick, punch):
        cmd             = "xdotool search --pid `pgrep mame`"
        srp             =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        v               = srp.read()
        self.winid      = hex(int(v.decode()))
        os.system('xdotool windowfocus --sync ' + self.winid)
        self.l       = l
        self.r       = r
        self.up      = up
        self.down    = down
        self.kk      = kick
        self.pp      = punch

    def kick(self):
        for i in range(0,2):
            os.system('xdotool key --window ' + self.winid + ' key ' + self.kk)

    def punch(self):
        for i in range(0,2):
            os.system('xdotool key --window ' + self.winid + ' key ' + self.pp)

    def defendup(self, pos):
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        time.sleep(0.3)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)

    def defenddown(self, pos):
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        time.sleep(0.3)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)

    def downkick(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        for i in range(0,2):
            os.system('xdotool key --window ' + self.winid + ' key ' + self.kk)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)

    def left(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.l)
        time.sleep(0.6)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.l)

    def right(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.r)
        time.sleep(0.6)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.r)

    def jumpright(self, s):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.r)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.up)
        time.sleep(s)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.r)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.up)

    def jumpleft(self, s):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.l)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.up)
        time.sleep(s)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.l)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.up)

    def jumpup(self):
        os.system('xdotool key --window ' + self.winid + ' key ' + self.up)

    def fire(self, pos):
        z = self.r
        if pos == 0:
            z = self.r
        else:
            z = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.pp)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.pp)

    def superkick(self, pos):
        z = self.l
        if pos == 0:
            z = self.l
        else:
            z = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.kk)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.kk)

    def superpunch(self, pos):
        z = self.r
        if pos == 0:
            z = self.r
        else:
            z = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)

        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)

        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)

        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.pp)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.pp)

    def insertcoin(self):
        os.system('xdotool key --window ' + self.winid + ' keydown 5')
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' keyup 5')
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' key 1')

    def select(self):
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' key A')

    def nav(self, r):
        if r == 0:
          self.left()
        elif r == 2:
          self.defendup(0)
        elif r == 3:
          self.defenddown(0)
        elif r == 4:
          self.right()
        elif r == 7:
          self.defendup(1)
        elif r == 8:
          self.defenddown(1)

    def act(self, r):
        if r == 0:
          self.kick()
          self.right()
          self.kick()
        elif r == 1:
          self.kick()
          self.left()
          self.kick()
        elif r == 2:
          self.jumpleft(0.6)
          self.kick()
        elif r == 3:
          self.fire(0)
        elif r == 4:
          self.superpunch(0)
        elif r == 5:
          self.superkick(0)
        elif r == 6:
          self.punch()
        elif r == 7:
          self.kick()
        elif r == 8:
          self.downkick()
        elif r == 9:
          self.kick()
          self.jumpup()
          self.kick()
        elif r == 10:
          self.jumpright(0.6)
          self.kick()
        elif r == 11:
          self.fire(1)
        elif r == 12:
          self.superpunch(1)
        elif r == 13:
          self.superkick(1)
