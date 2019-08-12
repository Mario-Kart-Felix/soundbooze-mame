import subprocess
import time
import os

# https://snk.fandom.com/wiki/Haohmaru/Move_list

class HAOHMARU:

    def __init__(self, l, r, up, down, slash, kick, a):
        cmd         = "xdotool search --pid `pgrep mame`"
        srp         =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        v           = srp.read()
        self.winid  = hex(int(v.decode()))
        os.system('xdotool windowfocus --sync ' + self.winid)
        self.l      = l
        self.r      = r
        self.up     = up
        self.down   = down
        self.slash  = slash
        self.kick   = kick
        self.a      = a

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
                
    def Roll(self, pos):
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        for i in range(2):
            os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
            os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
            os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
            os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
            time.sleep(0.05)
            os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)
            os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
            os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)
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
        elif pos == 1:
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
        elif pos == 1:
            z = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.kick)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.kick)

    def Hide(self, pos):
        z1 = self.r
        z2 = self.l
        if pos == 0:
            z1 = self.r
            z2 = self.l
        elif pos == 1:
            z1 = self.l
            z2 = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.slash)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.slash)
     
    def SakeKougeki(self, pos):
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + a)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + a)

    def TenhaSeiouZan(self, pos):
        z1 = self.r
        z2 = self.l
        if pos == 0:
            z1 = self.r
            z2 = self.l
        elif pos == 1:
            z1 = self.l
            z2 = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.a)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.a)

    def act(self, r):
        if r == 0:
            self.Walk(0)
        elif r == 1:
            self.Shift(0)
        elif r == 2:
            self.Roll(0)
        elif r == 3:
            self.DefendUp(0)
        elif r == 4:
            self.DefendDown(0)
        elif r == 5:
            self.StabSwingBack(0)
        elif r == 6:
            self.OugiSenpuuRetsuZan(0)
        elif r == 7:
            self.OugiKogetsuZan(0)
        elif r == 8:
            self.OugiResshinZan(0)
        elif r == 9:
            self.TenhaSeiouZan(0)
        elif r == 10:
            self.Hide(0)
        elif r == 11:
            self.SakeKougeki(0)
        elif r == 12:
            self.JumpLeftSlash()

        elif r == 13:
            self.JumpSlash()
        elif r == 14:
            self.DownSlash()
        elif r == 15:
            self.Slash()

        elif r == 16:
            self.Walk(1)
        elif r == 17:
            self.Shift(1)
        elif r == 18:
            self.Roll(1)
        elif r == 19:
            self.DefendUp(1)
        elif r == 20:
            self.DefendDown(1)
        elif r == 21:
            self.StabSwingBack(1)
        elif r == 22:
            self.OugiSenpuuRetsuZan(1)
        elif r == 23:
            self.OugiKogetsuZan(1)
        elif r == 24:
            self.OugiResshinZan(1)
        elif r == 25:
            self.TenhaSeiouZan(1)
        elif r == 26:
            self.Hide(1)
        elif r == 27:
            self.SakeKougeki(1)
        elif r == 28:
            self.JumpRightSlash()

    def cont(self):
        os.system('xdotool key --window ' + self.winid + ' keydown 5')
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' keyup 5')
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' key 1')

    def select(self):
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' key a')
