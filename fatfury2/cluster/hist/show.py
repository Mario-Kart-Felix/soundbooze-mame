import numpy
import matplotlib.pyplot as plt
import sys

h = sys.argv[1]
H = numpy.load(h)

plt.title('H')
plt.plot(H)
plt.show()
