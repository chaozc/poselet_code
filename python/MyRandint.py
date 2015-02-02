import numpy as np
class MyRandint:
    def __init__(self):
        self.last = None

    def __call__(self, low, high):
        r = np.random.randint(low, high)
        while r == self.last:
            r = np.random.randint(low, high)
        self.last = r
        return r