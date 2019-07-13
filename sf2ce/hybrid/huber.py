# -*- coding: utf-8 -*-

#https://github.com/keon/deep-q-learning/blob/master/ddqn.py

import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

from ring import *

class DNH:

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.timestep = RINGBUFFER(16)
        self.gamma = 0.95 
        self.learning_rate = 0.001
        self.model = self._build()
        self.update()

    def _huber_loss(self, y_true, y_pred, clip_delta=1.0):
        error = y_true - y_pred
        cond  = K.abs(error) <= clip_delta
        squared_loss = 0.5 * K.square(error)
        quadratic_loss = 0.5 * K.square(clip_delta) + clip_delta * (K.abs(error) - clip_delta)
        return K.mean(tf.where(cond, squared_loss, quadratic_loss))

    def _build(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss=self._huber_loss, optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward):
        self.timestep.append((state, action, reward))

    def act(self, state):
        scaled = StandardScaler().fit_transform(state)
        a = self.model.predict(scaled)
        return np.argmax(a[0])

    def fit(self, ):
        '''
        scaled = StandardScaler().fit_transform(state)
        self.model.fit(scaled, target, epochs=1, verbose=0)
        '''

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)
