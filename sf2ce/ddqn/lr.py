# -*- coding: utf-8 -*-

import sys
import numpy

class LogisticRegression(object):

    def __init__(self, input, label, n_in, n_out):
        self.x = input
        self.y = label
        self.W = numpy.zeros((n_in, n_out))
        self.b = numpy.zeros(n_out)

    def _softmax(x):
        e = numpy.exp(x - numpy.max(x))
        if e.ndim == 1:
            return e / numpy.sum(e, axis=0)
        else:  
            return e / numpy.array([numpy.sum(e, axis=1)]).T

    def train(self, lr=0.1, input=None, L2_reg=0.00):        
        if input is not None:
            self.x = input
        p_y_given_x = self.output(self.x)
        d_y = self.y - p_y_given_x
        self.W += lr * numpy.dot(self.x.T, d_y) - lr * L2_reg * self.W
        self.b += lr * numpy.mean(d_y, axis=0)
        self.d_y = d_y
        
    def output(self, x):
        return _softmax(numpy.dot(x, self.W) + self.b)

    def predict(self, x):
        return self.output(x)

    def negative_log_likelihood(self):
        s_activation = _softmax(numpy.dot(self.x, self.W) + self.b)
        cross_entropy = - numpy.mean(
            numpy.sum(self.y * numpy.log(s_activation) +
            (1 - self.y) * numpy.log(1 - s_activation),
                      axis=1))
        return cross_entropy

def test_lr(learning_rate=0.1, n_epochs=500):

    #pre-transform[255, 1]
    x = numpy.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0]])

    y = numpy.array([[1, 0],
                     [1, 0],
                     [1, 0],
                     [1, 0],
                     [1, 0],
                     [0, 1],
                     [0, 1],
                     [0, 1],
                     [0, 1],
                     [0, 1]])

    # Attack/Defend | pre-SOM | totoKotak
    # [0, 0] 0 
    # [0, 1] 1 

    # [1, 0] 2
    # [1, 1] 3

    classifier = LogisticRegression(input=x, label=y, n_in=len(x[0]), n_out=2)

    # fork/mp - que-sync (get,put)
    for epoch in xrange(n_epochs):
        classifier.train(lr=learning_rate)
        cost = classifier.negative_log_likelihood()
        print >> sys.stderr, 'Training epoch %d, cost is ' % epoch, cost
        learning_rate *= 0.995

    #pre-transform[255, 1]
    test = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    z = classifier.predict(test)
    z[z >= 0.5] = 1
    z[z < 0.5] = 0
    print z

if __name__ == "__main__":
    test_lr()
