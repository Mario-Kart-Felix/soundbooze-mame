import numpy

n = numpy.random.choice(5, 3, p=[0.1, 0, 0.3, 0.6, 0])
print n

n = numpy.random.choice(5, 3, replace=False, p=[0.1, 0, 0.3, 0.6, 0])
print n

aa_milne_arr = ['pooh', 'rabbit', 'piglet', 'Christopher']
n = numpy.random.choice(aa_milne_arr, 5, p=[0.5, 0.1, 0.1, 0.3])

print n
