import random

from hash import H_s

class Ring:
    def __init__(self, generator, l, q) -> None:
        self.__priv = random.randint(1, l)
        self.pub = self.__priv * generator
        self.generator = generator
        self.key_image = self.__priv * self.pub
        self.l = l
        self.q_prime = q

    def sign(self, message, n):
        # Subset of random PubKeys. In the real world we wold take the PubKeys of real users.
        self.S = [random.randint(1, self.l) * self.generator for _ in range(n)]
        self.s = random.randint(0, n)
        self.S.insert(self.s, self.pub)

        self.q = [random.randint(1, self.l) for _ in range(n)]
        self.w = [random.randint(1, self.l) if i != self.s else 0 for i in range(n)]
        
        self.L = []
        self.R = []
        for i in range(n):
            if i != self.s:
                self.L.append(self.q[i]*self.generator+self.w[i]*self.S[i])
                self.R.append(self.q[i]*self.S[i]+self.w[i]*self.key_image)
            else:
                self.L.append(self.q[i]*self.generator)  # Hash shuold be applied here
                self.R.append(self.q[i]*self.S[self.s]) # Hash shuold be applied here

        c = tuple(self.L + self.R + [H_s(message, self.q_prime)]) # Hash shuold be applied here
        c_hashed = H_s(''.join([str(i) for i in c]), self.q_prime)
        # Remove from the tuple the element at the index s
        self.c = c[:self.s] + c[self.s+1:]

        self.c = []
        self.r = []
        for i in range(n):
            if i != self.s:
                self.c.append(self.w[i])
                self.r.append(self.q[i])
            else:
                self.c.append(c_hashed + sum(c) % self.l)
                self.r.append(self.q[self.s]-self.c[self.s]*self.pub%self.l)

        omega = tuple([self.key_image] + self.c + self.r)

        return omega
                

    def verification(self, omega, n):
        L = []
        R = []
        for i in range(n):
            L.append(omega[i+n]*self.generator+omega[n+1]*self.pub)
            R.append(omega[i+n]*self.pub+omega[n+1]*self.key_image)
        
        c_f = H_s(''.join([str(i) for i in L+R]), self.q_prime) % self.l
        return c_f == sum(self.c)


