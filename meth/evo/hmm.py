import numpy
from hmmlearn import hmm

def hmmmat(size):

    def _rndsumone(n):
        R = []
        while (numpy.sum(R)) != 1.0:
            R = numpy.random.multinomial(100.0, numpy.ones(n)/n, size=1)[0]/100.0
        return R

    HMM = hmm.GaussianHMM(n_components=size, covariance_type="full")
    sp = _rndsumone(size)
    HMM.startprob_ = numpy.array(sp)

    S = []
    for i in range(size):
        S.append(_rndsumone(size))

    HMM.transmat_ = numpy.array(S)

    M = []
    for i in range(size):
        M.append(_rndsumone(2))

    HMM.means_ = numpy.array(M)
    HMM.covars_ = numpy.tile(numpy.identity(2), (9, 1, 1))

    print sp
    print ''
    print numpy.matrix(S)
    print ''

    return HMM

HMM = hmmmat(4)
_, Z = HMM.sample(10)

print Z
