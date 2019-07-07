import numpy
import pickle
import Queue
import PIL
import imagehash

class PROCESS:

    def __init__(self):
        self.HQ         = {}
        self.lr         = .88
        self.y          = .99
        self.p          = [1.0-(0.058*16), 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058]
        self.que        = Queue.Queue()
        self.timeout    = 1.6
        self.hash       = ['','', 0]

    def _append(self, h):
        if not h in self.HQ:
            self.HQ[h] = [numpy.random.random(len(self.p)) / numpy.iinfo(numpy.int16).max, [0,0], numpy.zeros(len(self.p))]

    def _hash(self, frame):
        return imagehash.phash(frame)

    def lock(self, p, n, a):
        self.hash[0], self.hash[1], self.hash[2] = p, n, a

    def rminus(self, h, a):
        try:
            self.HQ[h][2][a] -= 0.01
        except:
            pass

    def rplus(self, h, a):
        try:
            self.HQ[h][2][a] += 0.01
        except:
            pass

    def act(self, curr):
        try:
            return numpy.argmax(self.HQ[curr][0] + self.HQ[curr][2])
        except:
            return numpy.random.choice(len(self.p), 1, p=self.p)[0]

    def hit(self, h, hit):
        try:
            self.HQ[h][1] = hit
        except:
            pass

    def update(self, prev, a, curr, hit):
        try:
            self.HQ[prev][0][a] = (self.HQ[prev][0][a] + self.lr * (numpy.sum(hit) + self.y * numpy.max(self.HQ[curr][0]) - self.HQ[prev][0][a])) / numpy.iinfo(numpy.int16).max
        except:
            pass

    def process(self, prev, curr, player):

        def _log(hcurr, a):
            try:
                print("HQ[%d] - [%s]%s [%d %d] (%s)" %(len(self.HQ), hcurr, '*' if hcurr in self.HQ else '', self.HQ[hcurr][1][0], self.HQ[hcurr][1][1], player.action[a]))
            except:
                pass

        pink = PIL.Image.fromarray(prev)
        red = PIL.Image.fromarray(curr)
        hprev = self._hash(pink)
        hcurr = self._hash(red)
        self._append(hcurr)
        a = self.act(hcurr)
        player.act(a)
        self.lock(hprev, hcurr, a)
        
        _log(hcurr, a)
        _q, _ = self.que.get(self.timeout), self.que.task_done()

    def reduce(self):
        for k, v in self.HQ.items():
            if numpy.sum(v[1]) == 0:
                del self.HQ[k]

    def load(self, filename):
        fp = open(filename, 'rb')
        self.HQ = pickle.load(fp)
        fp.close()

    def save(self, root):
        self.reduce()
        fp = open(root + 'HQ.pkl', 'wb')
        pickle.dump(self.HQ, fp)
        fp.close()
