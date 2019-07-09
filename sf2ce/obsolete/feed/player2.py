import numpy
import random
import time

from bison import *

def skewone(V, LR, p):

    def _rndsumone(n):
        R = []
        while (numpy.sum(R)) != 1.0:
            R = numpy.random.multinomial(100.0, numpy.ones(n)/n, size=1)[0]/100.0
        return R

    prob = numpy.zeros(len(LR))
    if p == 0:
        for i in range(len(LR)/2):
            prob[i] += LR[i] * V[i]
    elif p == 1:
        for i in range(len(LR)/2, len(LR)):
            prob[i] += LR[i] * V[i]
    prob /= numpy.sum(prob)

    if numpy.sum(prob) != 1.0:
        return _rndsumone(len(LR))

    return prob

def lerp(V0, V1, t):
    l = []
    if len(V0) == len(V1):
        for x, y in zip(V0, V1):
            l.append((1 - t) * x + t * y)
    return l

prev = numpy.random.rand(20)
prev /= numpy.sum(prev)

curr = numpy.random.rand(20)
curr /= numpy.sum(prev)

bison = BISON('j', 'l', 'i', 'k', 'y', 'h')

while [ 1 ]:
    
    l = numpy.random.randint(0,2)
    curr = skewone(curr, lerp(prev, curr, numpy.random.rand()), l)
    r = numpy.random.choice(len(curr), 1, p=curr)[0]
    bison.act(r)

    prev = curr

    time.sleep(0.29)
