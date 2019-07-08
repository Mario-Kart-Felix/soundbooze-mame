import time
import numpy
import pickle
import collections
import PIL
import imagehash

class TRANSITION:

    def __init__(self):
        self.T = collections.Counter()
        self.H = []
        self.depth = 3

    def _chop(self, H):
        chop = ''
        for h in range(0, self.depth): 
            chop += H[h]
        return chop

    def _hash(self, frame):
        return self._chop(str(imagehash.phash(frame)))
        #return str(imagehash.phash(frame))

    def _count(self, hprev, hcurr):
        h = str(hprev) + ':' + str(hcurr)
        self.T[h] += 1

    def _matrix(self, T):

        def _index(H):
            idx = 0
            for h in H:
                H[h] = idx
                idx += 1

        def _split(T):
            S0 = {}
            S1 = {}
            for h, c in T.items():
                H = h.split(':')
                prev = H[0]
                curr = H[1]
                S0[prev] = prev
                S1[curr] = curr

            _index(S0)
            _index(S1)

            return S0, S1

        def _check(Z):
            for i in range(len(Z)):
                fsum = float(numpy.sum(Z[i]))
                if fsum != 1.0:
                    print '[!]'

            return Z

        def _fill(T, S0, S1):
            l0, l1 = len(S0), len(S1)
            l = l0 if l0 > l1 else l1
            S = S0 if l0 > l1 else S1

            O = numpy.zeros((l, l))
            R = numpy.zeros((l, l))

            for h, c in T.items():
                H = h.split(':')
                prev = H[0]
                curr = H[1]
                i, j = S[prev], S[curr]
                #O[i][j] = 0.5 if c else 0
                O[i][j] = c

            for i in range(len(O)):
                fsum = float(numpy.sum(O[i]))
                for j in range(len(O[i])):
                    if fsum != 0:
                        R[i][j] = O[i][j]/fsum

            T = _check(R)
            return O, R

        S0, S1 = _split(T)
        FREQ, TRANS = _fill(T, S0, S1)

        return FREQ, TRANS, S0

    def process(self, pink, red):

        def _save(hprev, hcurr, pink, red):
            pink.save('ram/public/' + str(hprev) + '.png')
            red.save('ram/public/' + str(hcurr) + '.png')

        def _log(hprev, hcurr):
            self.H.append([time.time(), hprev])
            print("T[%d] - [%s] [%s] %d" %(len(self.T), hprev, hcurr, self.T[hprev + ':' + hcurr]))

        pink = PIL.Image.fromarray(pink)
        red = PIL.Image.fromarray(red)
        hprev = self._hash(pink)
        hcurr = self._hash(red)

        self._count(hprev, hcurr)

        _save(hprev, hcurr, pink, red)
        _log(hprev, hcurr)

    def load(self, filename):
        fp = open(filename, 'rb')
        self.T = pickle.load(fp)
        fp.close()

    def save(self, root):
        fp = open(root + 'T.pkl', 'wb')
        _, T, S0 = self._matrix(self.T)
        pickle.dump(T, fp)
        fp.close()

        fp = open(root + 'S0.pkl', 'wb')
        pickle.dump(S0, fp)
        fp.close()

        fp = open(root + 'H.pkl', 'wb')
        pickle.dump(self.H, fp)
        fp.close()
