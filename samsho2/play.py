import mss
import numpy

from haohmaru import *

if __name__ == '__main__':

    with mss.mss() as sct:

        action = ['Walk(0)','Shift(0)','DefendUp(0)','DefendDown(0)','StabSwingBack(0)','OugiSenpuuRetsuZan(0)','OugiKogetsuZan(0)','OugiResshinZan(0)','JumpLeftSlash()','JumpSlash()','DownSlash()','Slash()','Walk(1)','Shift(1)','DefendUp(1)','DefendDown(1)','StabSwingBack(1)','OugiSenpuuRetsuZan(1)','OugiKogetsuZan(1)','OugiResshinZan(1)','JumpRightSlash()']
        haohmaru  = HAOHMARU('Left', 'Right', 'Up', 'Down', 's', 'z')

        while [ 1 ]:

            r = numpy.random.randint(0, len(action))
            print action[r]
            haohmaru.act(r)

    
