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

        self.S = [double_and_add(self.generator, random.randint(1, self.l), infinite) for _ in range(n-1)]
        alfa = random.randint(1, self.l-1)
        self.j = random.randint(0, n-1)
        self.S.insert(self.j, self.pub)
        self.s = [random.randint(1, self.l-1) if x != self.j else 0 for x in range(n)]

        L_j = self.__key_to_str(double_and_add(self.generator, alfa, infinite))
        R_j = self.__key_to_str(double_and_add(self.pub, alfa, infinite))
        c = [0 for _ in range(n)]
        c[self.j+1] = self.__Hs([message, L_j, R_j])

        for i in range(self.j, n):
            L = self.__key_to_str(double_and_add(self.generator, self.s[i+1], infinite) + double_and_add(self.S[i+1], c[i+1], infinite))
            R = self.__key_to_str(double_and_add(self.S[i+1], self.s[i+1], infinite) + double_and_add(self.key_image, c[i+1], infinite))
            if i+2 > n: 
                c[i+2] = self.__Hs([message, L, R])
            else:
                c[0] = self.__Hs([message, L, R])

        for i in range(0, self.j):
            if i == 0:
                index = n-1
            else:
                index = i-1
            L = self.__key_to_str(double_and_add(self.generator, self.s[index], infinite) + double_and_add(self.S[index], c[index], infinite))
            R = self.__key_to_str(double_and_add(self.S[index], self.s[index], infinite) + double_and_add(self.key_image, c[index], infinite))
            c[i+1] = self.__Hs([message, L, R])

        omega = [self.key_image] + c[1] + self.s
        return omega
                
    def verification(self, omega, n, message):
        pass
    
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


