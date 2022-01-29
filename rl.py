import numpy as np
import pong as p

I = 6 # input variables
H = 1 # number of neurons in hidden-layer

# Matrix representations of models, using Xavier initialization
# https://prateekvjoshi.com/2016/03/29/understanding-xavier-initialization-in-deep-neural-networks/
M1 = np.random.randn(H,I) / np.sqrt(I)
M2 = np.random.randn(H) / np.sqrt(H)

# Activation function
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def forward(x):
    h = np.dot(M1, x)
    h[h < 0] = 0 # ReLU activation
    # print(h)
    logp = np.dot(M2, h)
    # print(logp)
    p = sigmoid(logp)
    return p, h

def backprop():
    pass

episode_number = 0

g = p.Pong()
state = g.get_state()

while episode_number < 100:

    # print(state)

    p, h = forward(state)
    # print(p)

    action = 'u' if np.random.uniform() < p else 'd'

    observation, reward, over = g.step(action)

    if over:
        episode_number += 1
        print(reward)
