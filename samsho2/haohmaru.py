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

    '''
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
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.slash)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.slash)

        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.down)

    '''

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
        if r == 19:
            self.hellsgate(1)
         
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
