w = 1920/4
h = 1080/4

for i in range(16):
    if i != 0 and i % 4 == 0:
        print ''
    print '(', (i/4)*h, ',', (i%4)*w, ')',

