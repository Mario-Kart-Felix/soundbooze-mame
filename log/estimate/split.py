import numpy

split = 4

w = 1920/split
h = 1080/split

Z = numpy.array([27.6749997, 27.2944403, 31.98234394, 32, 6.12988511, 2.27884424, 4.07373464, 11.80582963, 4.62077117, 3.29168577,  5.77169966, 10.27127338, 10.61803817, 2.6645897, 5.16617458, 13.36175762])

def argmin(Z):
    return numpy.argmin(Z)

def idx(i):
    return i / split, i % split

def xy(r, c):
    return (i / split) * h, (i % split) * w

def show():
    for i in range(numpy.power(split, 2)):
        if i != 0 and i % split == 0:
            print ''
        print '(', (i/split)*h, ',', (i%split)*w, ')',

print numpy.matrix(Z.reshape(split,split))

i = argmin(Z)
r, c = idx(i)
x, y = xy(r, c)

print 'argmin', i
print 'RC', r, c
print 'XY', x, y

show()
