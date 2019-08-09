import mss
import numpy

from haohmaru import *

if __name__ == '__main__':

    with mss.mss() as sct:

        haohmaru  = HAOHMARU('Left', 'Right', 'Up', 'Down', 's', 'z')

        while [ 1 ]:

            r = numpy.random.randint(0,10)

            if r == 0:
                haohmaru.Shift(0)
            elif r == 1:
                haohmaru.DefendUp(0)
            elif r == 2:
                haohmaru.DefendDown(0)
            elif r == 3:
                haohmaru.StabSwingBack(0)
            elif r == 4:
                haohmaru.OugiSenpuuRetsuZan(0)
            elif r == 5:
                haohmaru.OugiKogetsuZan(0)
            elif r == 6:
                haohmaru.OugiResshinZan(0)
            elif r == 7:
                haohmaru.JumpSlash()
            elif r == 8:
                haohmaru.DownSlash()
            elif r == 9:
                haohmaru.Slash()

            time.sleep(0.06)
