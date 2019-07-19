class RINGBUFFER:

    def __init__(self, size):
        self.data = [None for i in xrange(size)]
        for i in range(size):
            self.append('')

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data
