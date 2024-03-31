import random

class Ring:

    def __init__(self, S: set, KeyPair: tuple, I: str, q: set, w: set):
        self.S = S
        self.s = random.randint(1, len(S)-1)
        self.__private_key = KeyPair[0]
        self.public_key = KeyPair[1]
        self.I = I
        if len(S) != len(q) or len(S) != len(w):
            raise ValueError("The length of S, q and w must be the same")
        self.q = q
        self.w = w

    def transformations(self, G):
        self.Li = set()
        self.Ri = set()
        for  i in range(len(self.S)):
            if i == self.s:
                self.Li.add(self.q[i] * G)
                self.Ri.add(self.q[i] * self.S[i])
            else:
                self.Li.add(self.q[i] * G + self.w[i] * self.public_key)
                self.Ri.add(self.qa[i] * self.S[i] + self.w[i] * self.I)
        return self.Li, self.Ri

    def non_interactive(self):
        pass

    def response(self):
        pass