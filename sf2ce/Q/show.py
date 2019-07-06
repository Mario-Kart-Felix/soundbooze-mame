import sys
import numpy
import pickle
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

def show():

    HQ = pickle.load(open(sys.argv[1], 'rb'))

    print '[HQ]:', len(HQ)

    Q         = [] 
    R         = []
    LP, LR    = [], []
    Pts, Rts  = [], []

    for k, v in HQ.items():
        Q.append(v[0])
        R.append(v[2])

        p = v[1][0]
        r = v[1][1]
        if p == -1:
            LP.append(p)
        if r == 1:
            LR.append(r)

        Pts.append(p)
        Rts.append(r)

    plt.subplot(211)
    Q = numpy.array(Q)
    plt.title('Q')
    sns.heatmap(Q)

    plt.subplot(212)
    R = numpy.array(R)
    plt.title('R')
    sns.heatmap(R)

    plt.show()

    plt.subplot(211)
    plt.title('[Penalty: ' + str(len(LP)) + ']')
    plt.bar(range(len(Pts)), Pts)

    plt.subplot(212)
    plt.title('[Reward: ' + str(len(LR)) + ']')
    plt.bar(range(len(Rts)), Rts)

    plt.show()

show()
