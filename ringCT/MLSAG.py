import random
from helper import double_and_add
from config import infinite, q

import hashlib

class Ring:
    def __init__(self, generator, l, q, m):
        self.l = l
        self.q_prime = q
        self.m = m # Això ho triem natres?
        self.generator = generator
        self.__priv = [random.randit(1,l-1) for _ in range(self.m)]
        self.Pub = [double_and_add(self.generator, x, infinite) for x in self.__priv]

    def sign(self, message, n):

        P = [[double_and_add(self.generator, random.randint(1,self.l-1), infinite) for _ in range(self.m)] for _ in range(n-1)]
        pi = random.randint(0, n-1)
        self.P.insert(pi, self.Pub)
        key_image = [double_and_add(pub, priv, infinite) for priv, pub in zip(self.__priv, self.Pub)]
        
        s = [[random.randint(1,self.l-1) for _ in range(self.m)] for _ in range(n-1)]
        alfa = [random.randint(1, self.l-1) for _ in range(self.m)]

        L_abs = []
        R_abs = []
        L = [self.__key_to_str(double_and_add(self.generator, a, infinite)) for a in alfa]
        R = [self.__key_to_str(double_and_add(pub, a, infinite)) for pub, a in zip(self.Pub, alfa)]
        temp = []
        [temp.extend([x]+[i]) for x,i in zip(L,R)]
        c = self.__Hs([message] + temp)

        for index in range(self.pi, n):
            L = [self.__key_to_str(double_and_add(self.generator, s_p, infinite) + double_and_add(pub, c)) for s_p, pub in zip(s[index], P[index])]
            R = [self.__key_to_str(double_and_add(pub, s_p, infinite) + double_and_add(key, c)) for pub, s_p, key in zip(P[index], s[index], key_image)]   
            temp = []
            [temp.extend([x]+[i]) for x,i in zip(L,R)]
            c = self.__Hs([message] + temp)  
        
        for index in range(0, self.pi):
            L = [self.__key_to_str(double_and_add(self.generator, s_p, infinite) + double_and_add(pub, c)) for s_p, pub in zip(s[index], P[index])]
            R = [self.__key_to_str(double_and_add(pub, s_p, infinite) + double_and_add(key, c)) for pub, s_p, key in zip(P[index], s[index], key_image)]   
            temp = []
            [temp.extend([x]+[i]) for x,i in zip(L,R)]
            c = self.__Hs([message] + temp)  

        temp = []
        [temp.extend([x]+[i]) for x,i in zip(L,R)]
        c_pi = self.__Hs([message] + temp)  

        alfa = [s_pi + c_pi*P[i] for s_pi, i in zip(s[pi], P[pi])]

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


