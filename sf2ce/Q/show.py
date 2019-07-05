import numpy
import pickle
import matplotlib.pyplot as plt

def show():

    Q = numpy.load(sys.argv[1])
    Z = pickle.load(open(sys.argv[2], 'rb'))

    print '[Q]:', len(Q), '[Z]:', len(Z)

    P, R     = [], []
    Pts, Rts = [], []

    for k, v in Z.items():
        p = v[1][0]
        r = v[1][1]
        if p == -1:
            P.append(p)
        if r == 1:
            R.append(r)

        Pts.append(p)
        Rts.append(r)

    plt.subplot(211)
    plt.title('[Penalty: ' + str(len(P)) + ']')
    plt.bar(range(len(Pts)), Pts)

    plt.subplot(212)
    plt.title('[Reward: ' + str(len(R)) + ']')
    plt.bar(range(len(Rts)), Rts)

    plt.show()

show()
