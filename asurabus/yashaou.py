import subprocess
import time
import os

# https://www.gamesdatabase.org/Media/SYSTEM/Arcade/commands/Commands_Asura_Buster_-_Eternal_Warriors_-_2000_-_Fuuki.htm_12.png

class YASHAOU:

    def __init__(self, l, r, up, down, a, b, c):
        cmd             = "xdotool search --pid `pgrep mame`"
        srp             =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        v               = srp.read()
        self.winid      = hex(int(v.decode()))
        os.system('xdotool windowfocus --sync ' + self.winid)
        self.l      = l
        self.r      = r
        self.up     = up
        self.down   = down
        self.a      = a
        self.b      = b
        self.c      = c

    def shift(self, pos):
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        for i in range(2):
            os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
            os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
            time.sleep(0.05)
            os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
            os.system('xdotool key --window ' + self.winid + ' keyup ' + key)

    def forwardkick(self, pos):
        key = self.r
        if pos == 0:
            key = self.r
        elif pos == 1:
            key = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.b)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.b)

    def jumpslash(self):
        os.system('xdotool key --window ' + self.winid + ' key ' + self.up + ' ' + self.c)

    def jumpforwardkick(self, pos):
        key = self.r
        if pos == 0:
            key = self.r
        elif pos == 1:
            key = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.up)
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.up)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.b)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.b)

    def bashkick(self, pos):
        key = self.r
        if pos == 0:
            key = self.r
        elif pos == 1:
            key = self.l

        for i in range(2):
            os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
            os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
            time.sleep(0.05)
            os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
            os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
            os.system('xdotool key --window ' + self.winid + ' key ' + self.b + ' ' + self.c)

        os.system('xdotool key --window ' + self.winid + ' key ' + self.b + ' ' + self.c)

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

    def downslash(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        for i in range(0,2):
            os.system('xdotool key --window ' + self.winid + ' key ' + self.c)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)

    def left(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.l)
        time.sleep(0.6)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.l)

    def right(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.r)
        time.sleep(0.6)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.r)

    def act(self, r):
        if r == 0:
            self.left()
        elif r == 1:
            self.shift(0)
        elif r == 2:
            self.forwardkick(0)
        elif r == 3:
            self.jumpforwardkick(0)
        elif r == 4:
            self.bashkick(0)
        elif r == 5:        
            self.defenddown(0)
        elif r == 6:
            self.defendup(0) 
        elif r == 7:
            self.jumpslash()
        elif r == 8:
            self.downslash()
        elif r == 9:
            self.right()
        elif r == 10:
            self.shift(1)
        elif r == 11:
            self.forwardkick(1)
        elif r == 12:
            self.jumpforwardkick(1)
        elif r == 13:
            self.bashkick(1)
        elif r == 14:
            self.defenddown(1)
        elif r == 15:
            self.defendup(1) 

    def cont(self):
        os.system('xdotool key --window ' + self.winid + ' keydown 5')
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' keyup 5')
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' key 1')

    def select(self):
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' key a')

    def intro(self):
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' key a')
