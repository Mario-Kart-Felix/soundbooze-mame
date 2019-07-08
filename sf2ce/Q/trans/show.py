import sys
import numpy
import pickle
import collections
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

def load(filename):
    fp = open(filename, 'rb') 
    T = pickle.load(fp)
    fp.close()
    print '[Length]:', len(T)
    return T

def zeroself(T):
    for i in range(len(T)):
        for j in range(len(T)):
            if i == j:
                T[i][j] = 0
    return T

TRANS = load(sys.argv[1])
H = load(sys.argv[2])

count = collections.Counter(H)

lbl = []
for h, c in count.items():
    lbl.append(h)

pos = [i for i, _ in enumerate(count.values())]

plt.subplot(311)
plt.xticks(pos, lbl)
plt.bar(range(len(count)), count.values())

plt.subplot(312)
plt.title('Transition')
sns.heatmap(TRANS)

plt.subplot(313)
plt.title('Zero')
sns.heatmap(zeroself(TRANS))

plt.show()
