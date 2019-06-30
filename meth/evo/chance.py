import torch
from torch.distributions import Bernoulli, Categorical

m = Bernoulli(torch.Tensor([0.3])) # 30% chance 1; 70% chance 0
z = m.sample()
print z.numpy()[0]

m = Categorical(torch.Tensor([ 0.25, 0.25, 0.25, 0.25 ]))
z = m.sample()  # equal probability of 0, 1, 2, 3
print z.numpy()
