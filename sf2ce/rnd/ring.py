class RINGBUFFER:

    def __init__(self, size):
        self.data = [0 for i in xrange(size)] #

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data
