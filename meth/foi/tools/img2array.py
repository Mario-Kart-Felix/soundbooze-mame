import sys
import cv2
import numpy

'''
def zeropad(A):

    Z = numpy.zeros(131072)
    P = []

    for a in A:
        P.append(a)

    for i in range(len(A), len(Z)):
            P.append(0)

    return P

A = numpy.array([1, 2, 3, 4, 5, 6, 7, 8])
P = zeropad(A)
'''

I = cv2.imread(sys.argv[1], 0)
I = cv2.resize(I, (400,200))
h, w = I.shape

print '#include <stdint.h>'
print ''
print 'uint8_t img['+ str(h) + ']' + '[' + str(w) + '] = { '

for i in range(len(I)):
    print '\t\t\t\t\t\t\t\t{',
    for j in range(len(I[i])):
        if j != len(I[i]) - 1:
            print str(I[i][j]) + ',',
        else:
            print str(I[i][j]),
    if i != len(I)-1:
        print '},'
    else:
        print '}'

print '};'
