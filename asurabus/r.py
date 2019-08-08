import mss
import numpy

from yashaou import *

if __name__ == '__main__':

    with mss.mss() as sct:

        yashaou  = YASHAOU('Left', 'Right', 'Up', 'Down', 'a', 's', 'd')

        while [ 1 ]:
            yashaou.death(numpy.random.randint(0,2))
            time.sleep(0.6)
            yashaou.downwardstab(numpy.random.randint(0,2))
            time.sleep(0.6)
            yashaou.hellsgate(numpy.random.randint(0,2))
            time.sleep(0.6)
            yashaou.bashkick(numpy.random.randint(0,2))
            time.sleep(0.6)
