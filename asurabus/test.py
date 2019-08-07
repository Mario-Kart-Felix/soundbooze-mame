import mss
import numpy

from yashaou import *

if __name__ == '__main__':

    with mss.mss() as sct:

        yashaou  = YASHAOU('Left', 'Right', 'Up', 'Down', 'a', 's', 'd')

        while [ 1 ]:
            #yashaou.death(0)
            yashaou.extrememisfortune(0)
