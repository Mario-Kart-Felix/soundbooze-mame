import sys
import numpy
import pickle
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

def show():

    HQ = pickle.load(open(sys.argv[1], 'rb'))

    print '[HQ]:', len(HQ)

    Q         = [] 
    HP, HR    = [], []
    Pts, Rts  = [], []

    for k, v in HQ.items():
        Q.append(v[0])
        p = v[1][0]
        r = v[1][1]
        if p == -1:
            HP.append(p)
        if r == 1:
            HR.append(r)

        Pts.append(p)
        Rts.append(r)

    Q = numpy.array(Q)
    sns.heatmap(Q)
    plt.show()

    plt.subplot(211)
    plt.title('[Penalty: ' + str(len(HP)) + ']')
    plt.bar(range(len(Pts)), Pts)

    plt.subplot(212)
    plt.title('[Reward: ' + str(len(HR)) + ']')
    plt.bar(range(len(Rts)), Rts)

    plt.show()

show()
