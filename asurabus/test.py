import mss
import numpy

from yashaou import *

if __name__ == '__main__':

    with mss.mss() as sct:

        yashaou  = YASHAOU('Left', 'Right', 'Up', 'Down', 'a', 's', 'd')

        while [ 1 ]:
            #yashaou.death(0)
            #yashaou.extrememisfortune(0)
            yashaou.hellsgate(1)
            #yashaou.bashkick(0)
            #yashaou.downwardstab(0)
            time.sleep(1)
