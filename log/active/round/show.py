import sys
import numpy
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

h = sys.argv[1]
H = numpy.load(h)

plt.title('H')
plt.plot(H)

resulta = seasonal_decompose(H, model='additive', freq=1)
resulta.plot()

resultm = seasonal_decompose(H, model='multiplicative', freq=1)
resultm.plot()

plt.show()
