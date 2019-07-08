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

TRANS = load(sys.argv[1])
H = load(sys.argv[2])

count = collections.Counter(H)

lbl = []
for h, c in count.items():
    lbl.append(h)

pos = [i for i, _ in enumerate(count.values())]

plt.subplot(211)
plt.xticks(pos, lbl)
plt.bar(range(len(count)), count.values())

plt.subplot(212)
plt.title('Transition')
sns.heatmap(TRANS)

plt.show()
