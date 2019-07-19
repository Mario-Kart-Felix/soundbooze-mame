import subprocess
import time
import os

class TERRY:

    def __init__(self, l, r, u, d, p, k):
        cmd = "xdotool search --pid `pgrep mame`"
        r =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        v = r.read()
        self.winid = hex(int(v.decode()))
        os.system('xdotool windowfocus --sync ' + self.winid)
        self.l = l
        self.r = r
        self.u = u
        self.d = d
        self.p = p
        self.k = k

    def punch(self):
        os.system('xdotool key --window ' + self.winid + ' key ' + self.p)

    def kick(self):
        os.system('xdotool key --window ' + self.winid + ' key ' + self.k)

    def downpunch(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' key ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)

    def downkick(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' key ' + self.k)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)

    def left(self, ts):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.l)
        time.sleep(ts)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.l)

    def right(self, ts):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.r)
        time.sleep(ts)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.r)

    def shift(self, pos):
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        for i in range(4):
            os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
            time.sleep(0.1)
            os.system('xdotool key --window ' + self.winid + ' keyup ' + key)

    def powerwave(self, pos):
        z = self.r
        if pos == 0:
            z = self.r
        else:
            z = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.p)

    def burnknuckle(self, pos):
        z = self.l
        if pos == 0:
            z = self.l
        else:
            z = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.p)

    def risingtackle(self, pos):
        z = self.l
        if pos == 0:
            z = self.l
        else:
            z = self.r
        for i in range(0,42):
            os.system('xdotool key --window ' + self.winid + ' keydown ' + z + ' ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.u)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.p)
        for i in range(0,42):
            os.system('xdotool key --window ' + self.winid + ' keyup ' + z + ' ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.u)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.p)

    def crackshoot(self, pos):
        z = self.l
        if pos == 0:
            z = self.l
        else:
            z = self.r

        for i in range(0,6):
            os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.u)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.k)
        for i in range(0,6):
            os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.u)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.k)

    def defendup(self, pos, ts):
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        time.sleep(ts)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)

    def defenddown(self, pos, ts):
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        time.sleep(ts)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup Down')

    def jumpright(self, ts):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.r)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.u)
        time.sleep(ts)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.r)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.u)

    def jumpleft(self, ts):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.l)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.u)
        time.sleep(ts)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.l)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.u)

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
