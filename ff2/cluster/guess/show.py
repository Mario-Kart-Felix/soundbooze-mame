import numpy
import matplotlib.pyplot as plt
import sys

ha, hz, ba, bz = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
HA, HZ = numpy.load(ha), numpy.load(hz)
BA, BZ = numpy.load(ba), numpy.load(bz)

plt.subplot(411)
plt.title('H Cont')
plt.plot(HA)

plt.subplot(412)
plt.title('H First')
plt.plot(HZ)

plt.subplot(413)
plt.title('B Cont')
plt.plot(BA)

plt.subplot(414)
plt.title('B First')
plt.plot(BZ)

plt.show()
