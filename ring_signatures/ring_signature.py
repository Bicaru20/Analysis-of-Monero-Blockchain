import random
from helper import double_and_add
from config import infinite, q

import hashlib

class Ring:
    def __init__(self, generator, l, q) -> None:
        self.__priv = random.randint(1, l-1)
        self.pub = double_and_add(generator, self.__priv, infinite)
        self.generator = generator
        self.key_image = double_and_add(self.__Hp(self.pub), self.__priv, infinite)
        self.l = l
        self.q_prime = q

    def sign(self, message, n):
        # Subset of random PubKeys. In the real world we wold take the PubKeys of real users.
        self.S = [double_and_add(self.generator, random.randint(1, self.l-1), infinite) for _ in range(n-1)]
        self.s = random.randint(0, n-1)
        self.S.insert(self.s, self.pub)
        print(self.s)

        self.q = [random.randint(1, self.l-1) for _ in range(n)]
        self.w = [random.randint(1, self.l-1) if i != self.s else 0 for i in range(n)]
        
        self.L = []
        self.R = []
        for i in range(n):
            # Com que self.w[self.s] = 0, no cal tractar el cas per separat:
            self.L.append(self.__key_to_str(double_and_add(self.generator, self.q[i], infinite)+double_and_add(self.S[i], self.w[i], infinite)))
            self.R.append(self.__key_to_str(double_and_add(self.__Hp(self.S[i]), self.q[i], infinite)+double_and_add(self.key_image, self.w[i], infinite)))
        #self.L.insert(self.s, (self.__key_to_str(double_and_add(self.generator, self.q[i], infinite))))
        #self.R.insert(self.s, (self.__key_to_str(double_and_add(self.__Hp(self.S[i]), self.q[i], infinite))))

        c = [message] + self.L + self.R

        c_hashed = self.__Hs(c)

        self.c = []
        self.r = []
        for i in range(n):
            if i != self.s:
                self.c.append(self.w[i])
                self.r.append(self.q[i])

        self.c.insert(self.s, (c_hashed - sum(self.w)) % self.l)
        self.r.insert(self.s, (self.q[self.s]-self.c[self.s]*self.__priv)%self.l)

        omega = [self.key_image] + self.c + self.r
        return omega
                
    def verification(self, omega, n, message):
        L = []
        R = []
        for i in range(n):
            L.append(self.__key_to_str(double_and_add(self.generator, omega[i+n+1], infinite)+double_and_add(self.S[i], omega[i+1], infinite)))
            R.append(self.__key_to_str(double_and_add(self.__Hp(self.S[i]), omega[i+n+1], infinite)+double_and_add(omega[0], omega[i+1], infinite)))
        ring = self.__Hs([message] + L + R)
        c_f =  ring
        print(c_f)
        print(sum(omega[1:n+1]) % self.l)
        return c_f == (sum(omega[1:n+1]) % self.l)
    
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
    
        return hash_value % self.l

    def __Hp(self, point):
        return point

    def __key_to_str(self, key):
        return hex(key.x())[2:] + hex(key.y())[2:]


