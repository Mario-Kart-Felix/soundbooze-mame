import os
import sys
import numpy
import pickle
import collections
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import cv2
import glob

from hmmlearn import hmm
numpy.random.seed(505)

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

def _fix(T):
    for i in range(len(T)):
        fsum = float(numpy.sum(T[i]))
        if fsum != 1.0 and fsum != 0.0:
            print '[!]', fsum

    return T

def _video(directory):
    img_array = []
    size = (0,0)
    for filename in glob.glob(directory + '*.png'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

    out = cv2.VideoWriter('sample.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
     
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

def simulate(TRANS, S0):

    def _n(idx):
        for h, i in S0.items():
            if i == idx:
                return h

    model = hmm.GaussianHMM(n_components=len(TRANS[0]), covariance_type="full",  n_iter=100, init_params="mcs")
    model.startprob_ = numpy.array(TRANS[numpy.random.randint(0,len(TRANS[0]))])
    model.transmat_ = numpy.array(TRANS)

    M = []
    for i in range(len(TRANS[0])):
        M.append([numpy.random.random(), numpy.random.random()])

    model.means_ = numpy.array(M)
    model.covars_ = numpy.tile(numpy.identity(2), (len(TRANS[0]),1,1))

    X, Z = model.sample(50)

    for z in Z:
        h = _n(z)
        os.system('cp ram/public/' + h + '.png' + ' ' + 'ram/tmp/')
        #print h

    #_video('ram/tmp/')

TRANS = load(sys.argv[1])
S0    = load(sys.argv[2])
H     = load(sys.argv[3])

ts    = []
phash = []

for h in H:
    ts.append(h[0])
    phash.append(h[1])

count = collections.Counter(phash)

lbl = []
for h, c in count.items():
    lbl.append(h)

#TRANS = _fix(TRANS)
simulate(TRANS, S0)

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
