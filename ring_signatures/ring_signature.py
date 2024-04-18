import random
from helper import double_and_add
from config import infinite, q

import hashlib

class Ring:
    def __init__(self, generator, l, q) -> None:
        self.__priv = random.randint(1, l)
        self.pub = double_and_add(generator, self.__priv, infinite)
        self.generator = generator
        self.key_image = double_and_add(self.pub, self.__priv, infinite)
        self.l = l
        self.q_prime = q

    def sign(self, message, n):
        # Subset of random PubKeys. In the real world we wold take the PubKeys of real users.
        self.S = [double_and_add(self.generator, random.randint(1, self.l), infinite) for _ in range(n-1)]
        self.s = random.randint(0, n)
        self.S.insert(self.s, self.pub)

        self.q = [random.randint(1, self.l) for _ in range(n)]
        self.w = [random.randint(1, self.l) if i != self.s else 0 for i in range(n)]
        
        self.L = []
        self.R = []
        for i in range(n):
            if i != self.s:
                self.L.append(self.__key_to_str(double_and_add(self.generator, self.q[i], infinite)+double_and_add(self.S[i], self.w[i], infinite)))
                self.R.append(self.__key_to_str(double_and_add(self.S[i], self.q[i], infinite)+double_and_add(self.key_image, self.w[i], infinite)))
            else:
                self.L.append(self.__key_to_str(double_and_add(self.generator, self.q[i], infinite)))  # Hash shuold be applied here
                self.R.append(self.__key_to_str(double_and_add(self.S[i], self.q[i], infinite))) # Hash shuold be applied here

        c = [message] + self.L + self.R

        c_hashed = self.__Hs(c)

        # self.c_ind_hashed = c
        # self.c_ind_hashed = [self.__Hs([message]+[self.c_ind_hashed[i]]+[self.c_ind_hashed[i+n]]) for i in range(0, n)] # He de fer el hash de punts?

        self.c = []
        self.r = []
        for i in range(n):
            if i != self.s:
                self.c.append(self.w[i])
                self.r.append(self.q[i])
            else:
                self.c.append((c_hashed - sum(self.w)) % self.l) # Quan fem el mod?
                self.r.append((self.q[self.s]-self.c[self.s]*self.__priv)%self.l)

        omega = [self.key_image] + self.c + self.r
        return omega
                

    def verification(self, omega, n, message):
        L = []
        R = []
        for i in range(n):
            L.append(self.__key_to_str(double_and_add(self.generator, omega[i+n], infinite)+double_and_add(self.S[i], omega[i+1], infinite)))
            R.append(self.__key_to_str(double_and_add(self.S[i], omega[i+n], infinite)+double_and_add(omega[0], omega[i+1], infinite)))
        ring = self.__Hs([message] + L + R)
        c_f =  ring % self.l
        return c_f == sum(self.c) % self.l
    
    def __Hs(self, ll):

        # Initialize a hash object using SHA-256 (you can choose a different hash function if needed)
        hash_object = hashlib.sha256()
        
        # Update the hash object with each argument
        for arg in ll:
            msg = arg.encode("utf-8")
            hash_object.update(msg)
        
        # Obtain the hash value
        hash_bytes = hash_object.digest()

        hash_value = int.from_bytes(hash_bytes, byteorder='big')
    
        return hash_value % q
    
    def __key_to_str(self, key):
        return hex(key.x())[2:] + hex(key.y())[2:]


