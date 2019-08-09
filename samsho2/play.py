import mss
import numpy

from haohmaru import *

if __name__ == '__main__':

    with mss.mss() as sct:

        haohmaru  = HAOHMARU('Left', 'Right', 'Up', 'Down', 's', 'z')

        while [ 1 ]:

            r = numpy.random.randint(0, 21)
            haohmaru.act(r)

    
