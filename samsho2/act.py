import numpy
from haohmaru import *

class ACT:

    def __init__(self, l, r, u , d, slash, kick, a):
        self.haohmaru = HAOHMARU(l, r, u, d, slash, kick, a)
        self.action   = ['Walk(0)','Shift(0)','DefendUp(0)','DefendDown(0)','StabSwingBack(0)','OugiSenpuuRetsuZan(0)','OugiKogetsuZan(0)','OugiResshinZan(0)','TenhaSeiouZan(0)','Hide(0)','JumpLeftSlash()','JumpSlash()','DownSlash()','Slash()','Walk(1)','Shift(1)','DefendUp(1)','DefendDown(1)','StabSwingBack(1)','OugiSenpuuRetsuZan(1)','OugiKogetsuZan(1)','OugiResshinZan(1)','TenhaSeiouZan(1)','Hide(1)','JumpRightSlash()']

    def next(self):
        return numpy.random.randint(0, len(self.action))

    def act(self, r):
        self.haohmaru.act(r)
