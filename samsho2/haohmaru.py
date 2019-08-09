import subprocess
import time
import os

# https://snk.fandom.com/wiki/Haohmaru/Move_list

class HAOHMARU:

    def __init__(self, l, r, up, down, slash, kick):
        cmd             = "xdotool search --pid `pgrep mame`"
        srp             =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        v               = srp.read()
        self.winid      = hex(int(v.decode()))
        os.system('xdotool windowfocus --sync ' + self.winid)
        self.l      = l
        self.r      = r
        self.up     = up
        self.down   = down
        self.slash  = slash
        self.kick   = kick

    def Walk(self, pos):
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        time.sleep(0.3)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        
    def Shift(self, pos):
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
                
    def DefendUp(self, pos): 
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        time.sleep(0.3)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)

    def DefendDown(self, pos):
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        time.sleep(0.3)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)

    def Slash(self):
        os.system('xdotool key --window ' + self.winid + ' key ' + self.slash)

    def DownSlash(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        for i in range(0,2):
            os.system('xdotool key --window ' + self.winid + ' key ' + self.slash)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)

    def JumpSlash(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.up)
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.slash)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.up )
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.slash)

    def JumpLeftSlash(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.l)
        time.sleep(0.02)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.up)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.l)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.up)
        os.system('xdotool key --window ' + self.winid + ' key ' + self.slash)

    def JumpRightSlash(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.r)
        time.sleep(0.02)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.up)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.r)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.up)
        os.system('xdotool key --window ' + self.winid + ' key ' + self.slash)

    def OugiSenpuuRetsuZan(self, pos):
        key = self.r
        if pos == 0:
            key = self.r
        elif pos == 1:
            key = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.slash)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.slash)

    def StabSwingBack(self, pos):
        if pos == 0:
            self.OugiSenpuuRetsuZan(1)
        elif pos == 1:
            self.OugiSenpuuRetsuZan(0)

    def OugiKogetsuZan(self, pos):
        z = self.r
        if pos == 0:
            z = self.r
        else:
            z = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.slash)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.slash)

    def OugiResshinZan(self, pos):
        z = self.r
        if pos == 0:
            z = self.r
        else:
            z = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.kick)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.kick)

    def act(self, r):
        if r == 0:
            haohmaru.Walk(0)
        elif r == 1:
            haohmaru.Shift(0)
        elif r == 2:
            haohmaru.DefendUp(0)
        elif r == 3:
            haohmaru.DefendDown(0)
        elif r == 4:
            haohmaru.StabSwingBack(0)
        elif r == 5:
            haohmaru.OugiSenpuuRetsuZan(0)
        elif r == 6:
            haohmaru.OugiKogetsuZan(0)
        elif r == 7:
            haohmaru.OugiResshinZan(0)
        elif r == 8:
            haohmaru.JumpLeftSlash()

        elif r == 9:
            haohmaru.JumpSlash()
        elif r == 10:
            haohmaru.DownSlash()
        elif r == 11:
            haohmaru.Slash()

        elif r == 12:
            haohmaru.Walk(1)
        elif r == 13:
            haohmaru.Shift(1)
        elif r == 14:
            haohmaru.DefendUp(1)
        elif r == 15:
            haohmaru.DefendDown(1)
        elif r == 16:
            haohmaru.StabSwingBack(1)
        elif r == 17:
            haohmaru.OugiSenpuuRetsuZan(1)
        elif r == 18:
            haohmaru.OugiKogetsuZan(1)
        elif r == 19:
            haohmaru.OugiResshinZan(1)
        elif r == 20:
            haohmaru.JumpRightSlash()

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
