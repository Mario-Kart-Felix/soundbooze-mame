import numpy

from keras.models import Sequential
from keras.layers import Dense, Reshape, Flatten
from keras.optimizers import Adam
from keras.layers.convolutional import Convolution2D

class PolicyGradient:

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = 0.9917
        self.learning_rate = 0.001
        self.states = []
        self.gradients = []
        self.rewards = []
        self.probs = []
        self.model = self._build_model()
        self.model.summary()

    def _build_model(self):
        model = Sequential()
        model.add(Reshape((1, 100, 50), input_shape=(self.state_size,)))
        model.add(Convolution2D(50, 5, 5, subsample=(3, 3), border_mode='same',
                                activation='relu', init='he_uniform'))
        model.add(Flatten())
        model.add(Dense(50, activation='relu', init='glorot_uniform'))
        model.add(Dense(10, activation='relu', init='glorot_uniform'))
        model.add(Dense(self.action_size, activation='softmax'))
        opt = Adam(lr=self.learning_rate)
        model.compile(loss='categorical_crossentropy', optimizer=opt)
        return model

    def remember(self, state, action, prob, reward):
        y = numpy.zeros([self.action_size])
        y[action] = 1
        self.probs.append(prob)
        self.gradients.append(numpy.array(y).astype('float32') - prob)
        self.states.append(state)
        self.rewards.append(reward)

    def act(self, state):
        try :
            state = state.reshape([1, state.shape[0]])
            aprob = self.model.predict(state, batch_size=1).flatten()
            #self.probs.append(aprob)
            prob = aprob / numpy.sum(aprob)
            action = numpy.random.choice(self.action_size, 1, p=prob)[0]
            return action, prob
        except:
            prob[numpy.isnan(prob)] = 0
            prob[17] = 1
            action = numpy.random.choice(self.action_size, 1, p=prob)[0]
            return action, prob

    def discount_rewards(self, rewards):
        discounted_rewards = numpy.zeros_like(rewards)
        running_add = 0
        for t in reversed(range(0, rewards.size)):
            if rewards[t] != 0:
                running_add = 0
            running_add = running_add * self.gamma + rewards[t]
            discounted_rewards[t] = running_add
        return discounted_rewards

    def train(self):
        try:
            gradients = numpy.vstack(self.gradients)
            rewards = numpy.vstack(self.rewards)
            rewards = self.discount_rewards(rewards)
            rewards = rewards / numpy.std(rewards - numpy.mean(rewards))
            gradients *= rewards
            X = numpy.squeeze(numpy.vstack([self.states]))
            Y = numpy.array(self.probs) + (self.learning_rate * numpy.squeeze(numpy.vstack([gradients])))
            print X.shape, Y.shape
            self.model.train_on_batch(X, Y)
            self.states, self.probs, self.gradients, self.rewards = [], [], [], []
        except:
            pass

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)
