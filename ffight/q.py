import numpy

class Q:

    def __init__(self):
        self.HQ         = {}
        self.lr         = .88
        self.y          = .99
        self.p          = [0.2, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1]

    def append(self, h):
        if not h in self.HQ:
            self.HQ[h] = [numpy.random.random(len(self.p)) / numpy.iinfo(numpy.int16).max, 0]

    def act(self, curr):
        try:
            return numpy.argmax(self.HQ[curr][0])
        except:
            return numpy.random.choice(len(self.p), 1, p=self.p)[0]

    def update(self, prev, curr, a, r):
        try:
            self.HQ[prev][0][a] = (self.HQ[prev][0][a] + self.lr * (r + self.y * numpy.max(self.HQ[curr][0]) - self.HQ[prev][0][a])) / numpy.iinfo(numpy.int16).max
        except:
            pass
