import subprocess
import time
import os

class RYU:

    def __init__(self, l, r, up, down, kick, punch):
        self.action     = ['punch', 'kick', 'downkick', 'kick|right|kick', 'kick|jumpup|kick', 'jumpleft|kick', 'jumpright|kick', 'fire(0)', 'fire(1)', 'superpunch(0)', 'superpunch(1)', 'superkick(0)', 'superkick(1)', 'defendup(0)', 'defendup(1)', 'defenddown(0)', 'defenddown(1)'] 
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

    def act(self, r):
        if r == 0:
          self.left()
        elif r == 1:
          self.jumpleft(0.6)
          self.kick()
        elif r == 2:
          self.kick()
          self.left()
          self.kick()
        elif r == 3:
          self.defendup(0)
        elif r == 4:
          self.defenddown(0)
        elif r == 5:
          self.fire(0)
        elif r == 6:
          self.superpunch(0)
        elif r == 7:
          self.superkick(0)

        elif r == 8:
          self.punch()
        elif r == 9:
          self.kick()
        elif r == 10:
          self.downkick()
        elif r == 11:
          self.kick()
          self.jumpup()
          self.kick()

        elif r == 12:
          self.right()
        elif r == 13:
          self.jumpright(0.6)
          self.kick()
        elif r == 14:
          self.kick()
          self.right()
          self.kick()
        elif r == 15:
          self.defendup(1)
        elif r == 16:
          self.defenddown(1)
        elif r == 17:
          self.fire(1)
        elif r == 18:
          self.superpunch(1)
        elif r == 19:
          self.superkick(1)
